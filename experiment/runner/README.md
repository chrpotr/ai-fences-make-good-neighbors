# The runner: do AI planners add rules nobody asked for?

```
owner:    the author. He runs every cell himself; an AI agent does not run this, because the rules an agent would
          add are the subject.
design:   written 2026-10-08 in two rounds: the protocol, then this runnable form.
sources:  Claude Code flags and JSON fields from code.claude.com (cli-reference, headless, env-vars, model-config,
          agent-sdk/cost-tracking). Codex flags, event stream, and config keys from learn.chatgpt.com
          (developer-commands, non-interactive-mode, config-reference, agent-configuration/agents-md). Read 2026-10-08.
          Items marked VERIFY are not in the docs; one real run settles each.
```

## What is being tested

Two claims the author made before any data existed:

1. More fences appear when the task is creative and non-deterministic.
2. Fences raise token spend: the AI pays to satisfy rules it invented.

Phase one, run by hand on 2026-10-08 with the standing files on, is in `../RESULTS.md`. This runner exists to run
the cells that phase one could not, standing files off, on two tools, with the counting done by a person.

## What counts as a fence

The author's definition: a rule or control that seeks to limit where the AI can go, do, or say. In a plan, a fence
is any line that forbids, bounds, gates, or requires approval. Each fence is sorted into one of three buckets:

| Bucket | Meaning |
|---|---|
| `prompt` | traced to a phrase in the prompt |
| `standing` | traced to a standing file the tool read (CLAUDE.md, AGENTS.md, memory) |
| `invented` | nothing behind it |

The `invented` bucket is the one the write-up is about. The author is the judge of record on every line. `count.py`
flags candidates by a fixed pattern list; it never decides.

## The files

| File | What it does |
|---|---|
| `manifest.json` | The two tasks, the prompt variants verbatim, the model IDs, the standing-file directories, n per cell. Fill the blanks before the first run |
| `run_claude.py` | Runs one cell on Claude Code headless: n fresh sessions, saves each plan and the raw JSON, appends a row to `runs.csv` |
| `run_codex.py` | Same on Codex `exec` |
| `count.py` | `flag` writes a per-plan sheet with candidate fence lines marked for a person to judge; `tally` reads the judged sheet and writes the seven count columns into `runs.csv` |
| `runs.csv` | One row per run. The table the write-up rests on |
| `plans/` | Created on the first run: `<run_id>.md` (the plan), `<run_id>.raw.json` or `.raw.jsonl` (the tool's full output), `<run_id>.count.md` (the judged sheet) |

## How each tool is called

**Claude Code, standing files absent, no tools.** Run from an empty directory with
`CLAUDE_CODE_DISABLE_CLAUDE_MDS=1`, which skips user, project, and auto-memory CLAUDE.md files (documented, env-vars).

```
claude -p "<prompt>" --model <full id> --safe-mode --tools "" --disallowedTools "*" --output-format json --no-session-persistence
```

`--safe-mode` also skips skills, plugins, hooks, and MCP and keeps the subscription sign-in (documented,
cli-reference). The two tool flags remove every tool from the model's context (documented semantics). The JSON
result carries the plan text, usage (input, output, cache read, cache creation), an estimated cost, and the model
that ran under `modelUsage` (documented, cost-tracking; the full schema is not published: VERIFY key names on run 1).
Claude Code's own default system prompt is not published and stays in every cell. It is a fence source nobody can
read.

**Claude Code, standing files present.** Same command without `--safe-mode` and without the env var, run from the
directory named in the manifest, so its CLAUDE.md tree loads as it would for real work.

**Codex, standing files absent, no tools.** Run from an empty directory outside any repository, with `CODEX_HOME`
pointed at an empty directory so no global AGENTS.md loads, and `CODEX_API_KEY` set for the run, because the home
change moves the saved sign-in (documented: `codex exec` honours `CODEX_API_KEY`; VERIFY that nothing else breaks).

```
codex exec --json --ephemeral --skip-git-repo-check --ignore-user-config --sandbox read-only -C <empty dir> -m <model> -c model_reasoning_effort="<level>" -c features.shell_tool=false -c web_search="disabled" "<prompt>"
```

The stream's `turn.completed` event carries `input_tokens`, `cached_input_tokens`, `output_tokens`, and
`reasoning_output_tokens` (documented, non-interactive-mode). No cost figure and no model name in the stream: the
script records the model requested and `codex --version`. `features.shell_tool` and `web_search` are documented
config keys; whether a plan-only run then makes zero tool calls is VERIFY. The raw stream is saved, and the script
counts `command_execution`, `mcp_tool_call`, and `web_search` items, so a run that used a tool is visible.

**Codex, standing files present.** Same without `--ignore-user-config`, with the real `CODEX_HOME`, run from the
directory named in the manifest, so its AGENTS.md tree loads.

## The row

```
run_id, tool, cli_version, model_reported, model_requested, effort, task_id, task_type, prompt_variant,
standing_files, run_n, started_at, duration_ms, input_tokens, cached_tokens, output_tokens, reasoning_tokens,
cost_usd_estimate, tool_calls, plan_path, lines_total, fence_lines, fence_prompt, fence_standing, fence_invented,
do_lines, dont_lines
```

The first twenty columns come from the tool and the script. The last seven come from the person judging, through
`count.py`.

## Run order, one variable at a time

1. **Task type.** Two tasks, prompt `P0`, standing files absent, both tools, three runs each. Twelve runs.
2. **Prompt wording.** On the task that showed more invented fences: `P0` against `P1`, same tool, three runs each.
3. **Standing files.** Same task and prompt, standing files present. Whether the fences come from the task or from
   what the tool reads.
4. **Phase two, the token claim.** One plan with its fences in, and the same plan with the `invented` bucket
   stripped by hand. Hand each to a fresh session with tools on (`--permission-mode` or `--sandbox workspace-write`)
   on a throwaway copy of the task. Compare tokens to completion. Three runs each. Not scripted here; the rows go
   into `runs.csv` by hand with `prompt_variant` set to `EXEC-fenced` or `EXEC-stripped`.

Three runs per cell is a floor to see variance, not a rule. One run is enough when the difference is plain.

## Running a cell

```
python run_claude.py --task T1 --prompt P0 --standing absent
python run_codex.py  --task T1 --prompt P0 --standing absent
python count.py flag plans/<run_id>.md        # writes plans/<run_id>.count.md for a person to judge
python count.py tally plans/<run_id>.count.md # writes the seven counts into runs.csv
```

`--n` overrides the manifest's n for one call. Every run is a fresh session; nothing resumes.

## What would change the design

- Zero invented fences in both tools at step 1: step 3 moves first.
- Codex refuses a plan-only run outside a repository even with the skip flag: the empty directory becomes an empty
  git repository with no AGENTS.md.
- The Claude JSON lacks a usage field: switch to `--output-format stream-json --verbose` and read the final
  `result` line, which carries the same fields.
