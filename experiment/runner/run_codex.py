#!/usr/bin/env python3
"""Run one cell of the fences experiment on Codex (`codex exec --json`).

    python run_codex.py --task T1 --prompt P0 --standing absent [--n 3]

Each run is a fresh session. The plan goes to plans/<run_id>.md, the full event stream to plans/<run_id>.raw.jsonl,
and one row to runs.csv. The script adds nothing to the prompt. a person runs this; an agent does not.

Standing files absent: CODEX_HOME is pointed at an empty directory so no global AGENTS.md loads. That also moves the
saved sign-in, so set CODEX_API_KEY in the environment before running the absent cell.
"""
import argparse
import csv
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
PLANS = HERE / "plans"
RUNS = HERE / "runs.csv"
COLUMNS = [
    "run_id", "tool", "cli_version", "model_reported", "model_requested", "effort", "task_id", "task_type",
    "prompt_variant", "standing_files", "run_n", "started_at", "duration_ms", "input_tokens", "cached_tokens",
    "output_tokens", "reasoning_tokens", "cost_usd_estimate", "tool_calls", "plan_path", "lines_total",
    "fence_lines", "fence_prompt", "fence_standing", "fence_invented", "do_lines", "dont_lines",
]
TOOL_ITEM_TYPES = {"command_execution", "mcp_tool_call", "web_search", "file_change"}


def abort(msg):
    print("ABORT: " + msg)
    sys.exit(1)


def load_manifest():
    m = json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))
    if not m["tools"]["codex"]["model"]:
        abort("manifest.json: tools.codex.model is blank")
    return m


def find_cli():
    exe = shutil.which("codex")
    if not exe:
        abort("codex is not on PATH")
    return exe


def cli_version(exe):
    try:
        out = subprocess.run([exe, "--version"], capture_output=True, text=True, timeout=60)
        return (out.stdout or out.stderr).strip().splitlines()[0]
    except Exception as e:  # noqa: BLE001
        return "unknown (" + str(e) + ")"


def append_row(row):
    new = not RUNS.exists()
    with RUNS.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        if new:
            w.writeheader()
        w.writerow({c: row.get(c, "") for c in COLUMNS})


def parse_stream(stdout):
    """Documented events: thread.started, turn.started, item.*, turn.completed (with usage), turn.failed, error."""
    messages, usage, tool_calls, failed, model = [], {}, 0, None, ""
    for line in stdout.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        t = ev.get("type", "")
        if t == "turn.completed":
            usage = ev.get("usage", {}) or {}
        elif t in ("turn.failed", "error"):
            failed = ev
        elif t == "item.completed":
            item = ev.get("item", {}) or {}
            if item.get("type") == "agent_message":
                messages.append(item.get("text", ""))
            elif item.get("type") in TOOL_ITEM_TYPES:
                tool_calls += 1
        if not model and isinstance(ev.get("model"), str):
            model = ev["model"]
    return messages, usage, tool_calls, failed, model


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True)
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--standing", choices=["absent", "present"], required=True)
    ap.add_argument("--n", type=int)
    a = ap.parse_args()

    m = load_manifest()
    tool = m["tools"]["codex"]
    task = next((t for t in m["tasks"] if t["id"] == a.task), None)
    if not task or not task["text"]:
        abort("task " + a.task + " missing or blank in manifest.json")
    template = m["prompts"].get(a.prompt)
    if not template:
        abort("prompt variant " + a.prompt + " not in manifest.json")
    prompt = template.replace("{task}", task["text"])
    n = a.n or m["n"]
    exe = find_cli()
    version = cli_version(exe)
    PLANS.mkdir(exist_ok=True)

    env = dict(os.environ)
    tmp_home = None
    if a.standing == "present":
        cwd = tool["standing_dir"]
        if not cwd or not Path(cwd).is_dir():
            abort("tools.codex.standing_dir is blank or not a directory")
        extra = []
    else:
        if not env.get("CODEX_API_KEY"):
            abort("set CODEX_API_KEY for the standing-files-absent cell (CODEX_HOME is moved, so the saved sign-in is not used)")
        cwd = tempfile.mkdtemp(prefix="fences-codex-")
        tmp_home = tempfile.mkdtemp(prefix="fences-codex-home-")
        env["CODEX_HOME"] = tmp_home
        extra = ["--ignore-user-config"]

    cmd = [exe, "exec", "--json", "--ephemeral", "--skip-git-repo-check", "--sandbox", "read-only",
           "-C", cwd, "-m", tool["model"],
           "-c", "features.shell_tool=false", "-c", 'web_search="disabled"'] + extra
    if tool.get("effort"):
        cmd += ["-c", 'model_reasoning_effort="' + tool["effort"] + '"']
    cmd.append(prompt)

    for i in range(1, n + 1):
        started = datetime.now(timezone.utc)
        run_id = started.strftime("%Y%m%dT%H%M%S") + "-codex-" + a.task + "-" + a.prompt + "-" + a.standing + "-" + str(i)
        t0 = time.time()
        proc = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, encoding="utf-8")
        wall_ms = int((time.time() - t0) * 1000)
        (PLANS / (run_id + ".raw.jsonl")).write_text(proc.stdout + "\n--- stderr ---\n" + proc.stderr, encoding="utf-8")
        messages, usage, tool_calls, failed, model = parse_stream(proc.stdout)
        if proc.returncode != 0 or failed or not messages:
            print(run_id + ": FAILED exit " + str(proc.returncode) + "; " + (json.dumps(failed) if failed else proc.stderr.strip()[:500]))
            continue
        plan = messages[-1]
        plan_path = PLANS / (run_id + ".md")
        plan_path.write_text(plan, encoding="utf-8")
        row = {
            "run_id": run_id, "tool": "codex", "cli_version": version,
            "model_reported": model, "model_requested": tool["model"],
            "effort": tool.get("effort", ""), "task_id": task["id"], "task_type": task["type"],
            "prompt_variant": a.prompt, "standing_files": a.standing, "run_n": i,
            "started_at": started.isoformat(timespec="seconds"), "duration_ms": wall_ms,
            "input_tokens": usage.get("input_tokens", ""),
            "cached_tokens": usage.get("cached_input_tokens", ""),
            "output_tokens": usage.get("output_tokens", ""),
            "reasoning_tokens": usage.get("reasoning_output_tokens", ""),
            "cost_usd_estimate": "", "tool_calls": tool_calls,
            "plan_path": str(plan_path.relative_to(HERE)).replace("\\", "/"),
        }
        append_row(row)
        note = " (used " + str(tool_calls) + " tool calls)" if tool_calls else ""
        print(run_id + ": ok, " + str(len(plan.splitlines())) + " lines, out " + str(row["output_tokens"]) + " tokens" + note)

    if a.standing == "absent":
        shutil.rmtree(cwd, ignore_errors=True)
        if tmp_home:
            shutil.rmtree(tmp_home, ignore_errors=True)


if __name__ == "__main__":
    main()
