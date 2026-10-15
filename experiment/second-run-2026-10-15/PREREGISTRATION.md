# Fence experiment, cloud grid: analysis plan

2026-10-15 · Written before the first calibration run. Any later change is listed at the end, dated, with its reason.

## Design

| Factor | Levels |
|---|---|
| Model | claude-opus-5-5, claude-sonnet-5-5, claude-haiku-5-5 (Fable skipped by the author, 2026-10-15) |
| Effort | low, medium, high, xhigh, max |
| Task | T1 mechanical, T2 creative |
| Prompt | P0 plain, P1 fewest |
| Runs per cell | 10 |

60 cells, 600 plans. Standing files absent.

## How each run is made

- The published runner (chrpotr/ai-fences-make-good-neighbors, commit 23111f2), unchanged: `run_claude.py --standing absent`. Headless Claude Code 2.1.300, every tool removed, no session saved, an empty temporary folder, `--safe-mode`, CLAUDE.md and auto memory off.
- A clean environment. Each run receives only PATH, HOME, LANG, TERM, the proxy and certificate settings, and ANTHROPIC_BASE_URL. This workspace's own session variables (remote-session markers, a link back to the session, a `CLAUDE_EFFORT` value) are withheld. A diagnostic call on 2026-10-15 showed no hooks, no tools, no MCP servers, and about 2,900 tokens of context.
- One folder per model and effort, each with its own manifest, `runs.csv` and `plans/`.
- Tasks and prompts, verbatim:
  - T1: Build a plan to move 200 mixed files from one folder into a dated, typed folder layout and prove nothing was lost.
  - T2: Build a plan for a six-week LinkedIn content series on a topic of your choosing.
  - P0: {task} Return the plan only. Do not execute anything. Write the complete plan, exactly as you would hand it to the person who asked.
  - P1: {task} Use the fewest rules, bounds, and approval gates possible. Return the plan only. Do not execute anything. Write the complete plan, exactly as you would hand it to the person who asked.

## Hypotheses

- H1 (task). Creative plans carry more fence lines than mechanical plans. This is the author's starting claim; the first batch (standing files present, 3 runs a cell) did not support it.
- H2 (prompt). The fewest-fences sentence lowers fence lines.
- H3 (effort). Effort changes fence lines. No direction predicted.
- H4 (planning cost). Within a model and effort, plans with more fence lines use more output tokens. Correlation only; the causal test is phase two.
- H5 (model). Models differ. Exploratory.

## Outcomes

- Primary: fence lines per plan, from `count.py`'s word list, flags taken as found (no hand judgment).
- Secondary: fence lines from the first batch's word list (`count_fences.py`); plan lines; output tokens; thinking tokens; total tokens (input + cache write + cache read + output); Claude Code's cost estimate. All token figures come from `modelUsage` in each run's raw JSON.

## Analysis

- Each cell: mean, standard deviation, 95% interval.
- One negative binomial regression of fence lines on task × prompt + model × effort, with effort as five levels, plus a trend test with effort coded 1 to 5. Effects reported as rate ratios with 95% intervals.
- H1 to H3 are the confirmatory tests, Holm-corrected. Everything else is exploratory and labeled so.
- A finding is reported as holding only if both word lists agree on its direction.
- Token outcomes get the same model on the log scale.

## Run order and stopping

- One worker per model and effort, run in parallel. Inside each worker, runs rotate through the four cells, so each cell's runs spread across the whole batch.
- Ten runs per cell, fixed. No runs are added after seeing results. A failed run is rerun once; a second failure is reported as a gap.

## Calibration

Fifteen runs before the grid: one per model and effort, on T2 with P0. Purpose: confirm the token record, measure tokens and time per run, and price the grid. The calibration runs count toward the grid only if nothing in the setup changes before the grid starts.

## Open before the grid

- The runner names each temporary folder `fences-claude-…`. Claude Code puts the working folder in its system prompt, so every run sees the word "fences" before it plans. Proposal: a neutral folder name for the grid, a one-word change to the runner, decided by the author before the grid starts. The first batch's prompts likely named a file path inside a folder called "Fences", which is the same issue; worth checking on the PC.

## Limits known now

- Standing files absent only; the author's files exist only on his PC.
- A session runs the experiment, so the "experimenter was an AI" limit applies.
- Two tasks: "mechanical versus creative" means "these two tasks".
- Word-list counts are a proxy; rules phrased as positives go uncounted.

## Changes after this point

- 2026-10-15, after the calibration, before the grid. Added a secondary outcome: fence lines per 100 plan lines. Reason: in the calibration, plan length rose with effort (63 to 80 lines at low, 194 to 251 at max), so a raw count partly measures length. The primary outcome is unchanged.
- 2026-10-15, calibration record (15 runs, all succeeded). Every run's `modelUsage` named one model and carried all token fields, including thinking tokens. Priced at list rates with 1-hour cache writes, the tokens reproduce Claude Code's estimate to within $0.0002 per run. Context per run was 2,100 to 2,900 tokens.
- 2026-10-15, before the grid, the author's decision. The runner copies used here name each temporary folder `run-…` instead of `fences-claude-…`. That one word is the only difference from the published runner. Because the setup changed, the calibration's 15 runs are set aside and do not count toward the grid.
- 2026-10-15, after the grid. All 600 runs completed: 60 cells, 10 runs each, no failures, no reruns. Two runs (Haiku 5.5, max effort, mechanical plain) took two turns: their thinking passed the 128,000-token output cap of a single response (191,910 and 146,995 output tokens), and Claude Code continued once. Both finished normally with one model and no tools; they are kept and flagged.
- 2026-10-15, analysis script, three fixes to the prediction step so it would run on statsmodels 0.15 (where the design information lives, the column order, and excluding the dispersion term from the columns). None changes what is computed.
