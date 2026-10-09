#!/usr/bin/env python3
"""Run one cell of the fences experiment on Claude Code headless.

    python run_claude.py --task T1 --prompt P0 --standing absent [--n 3]

Each run is a fresh session. The plan goes to plans/<run_id>.md, the tool's full JSON to plans/<run_id>.raw.json,
and one row to runs.csv. The script adds nothing to the prompt. a person runs this; an agent does not.
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


def abort(msg):
    print("ABORT: " + msg)
    sys.exit(1)


def load_manifest():
    m = json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))
    t = m["tools"]["claude"]
    if not t["model"]:
        abort("manifest.json: tools.claude.model is blank")
    return m


def find_cli():
    exe = shutil.which("claude")
    if not exe:
        abort("claude is not on PATH")
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


def parse_result(stdout):
    """The documented `json` output is one result object. Some versions print a list; take the result item."""
    data = json.loads(stdout)
    if isinstance(data, list):
        data = next((d for d in data if isinstance(d, dict) and d.get("type") == "result"), data[-1])
    return data


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True)
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--standing", choices=["absent", "present"], required=True)
    ap.add_argument("--n", type=int)
    a = ap.parse_args()

    m = load_manifest()
    tool = m["tools"]["claude"]
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

    if a.standing == "present":
        cwd = tool["standing_dir"]
        if not cwd or not Path(cwd).is_dir():
            abort("tools.claude.standing_dir is blank or not a directory")
        env = dict(os.environ)
        extra = []
    else:
        cwd = tempfile.mkdtemp(prefix="fences-claude-")
        env = dict(os.environ, CLAUDE_CODE_DISABLE_CLAUDE_MDS="1", CLAUDE_CODE_DISABLE_AUTO_MEMORY="1")
        extra = ["--safe-mode"]

    cmd = [exe, "-p", prompt, "--model", tool["model"], "--tools", "", "--disallowedTools", "*",
           "--output-format", "json", "--no-session-persistence"] + extra
    if tool.get("effort"):
        cmd += ["--effort", tool["effort"]]

    for i in range(1, n + 1):
        started = datetime.now(timezone.utc)
        run_id = started.strftime("%Y%m%dT%H%M%S") + "-claude-" + a.task + "-" + a.prompt + "-" + a.standing + "-" + str(i)
        t0 = time.time()
        proc = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, encoding="utf-8")
        wall_ms = int((time.time() - t0) * 1000)
        (PLANS / (run_id + ".raw.json")).write_text(proc.stdout, encoding="utf-8")
        if proc.returncode != 0 or not proc.stdout.strip():
            print(run_id + ": FAILED exit " + str(proc.returncode) + "; stderr: " + proc.stderr.strip()[:500])
            continue
        try:
            r = parse_result(proc.stdout)
        except json.JSONDecodeError:
            print(run_id + ": output was not JSON; saved raw. First 200 chars: " + proc.stdout[:200])
            continue
        if r.get("is_error"):
            print(run_id + ": tool reported an error: " + str(r.get("errors") or r.get("result"))[:500])
            continue
        plan = r.get("result", "")
        plan_path = PLANS / (run_id + ".md")
        plan_path.write_text(plan, encoding="utf-8")
        usage = r.get("usage", {}) or {}
        mu = r.get("modelUsage", {}) or {}
        row = {
            "run_id": run_id, "tool": "claude", "cli_version": version,
            "model_reported": ";".join(mu.keys()) if mu else "", "model_requested": tool["model"],
            "effort": tool.get("effort", ""), "task_id": task["id"], "task_type": task["type"],
            "prompt_variant": a.prompt, "standing_files": a.standing, "run_n": i,
            "started_at": started.isoformat(timespec="seconds"), "duration_ms": r.get("duration_ms", wall_ms),
            "input_tokens": usage.get("input_tokens", ""),
            "cached_tokens": usage.get("cache_read_input_tokens", ""),
            "output_tokens": usage.get("output_tokens", ""), "reasoning_tokens": "",
            "cost_usd_estimate": r.get("total_cost_usd", ""), "tool_calls": r.get("num_turns", ""),
            "plan_path": str(plan_path.relative_to(HERE)).replace("\\", "/"),
        }
        append_row(row)
        print(run_id + ": ok, " + str(len(plan.splitlines())) + " lines, out " + str(row["output_tokens"]) + " tokens")

    if a.standing == "absent":
        shutil.rmtree(cwd, ignore_errors=True)


if __name__ == "__main__":
    main()
