---
title: Fence experiment, phase one: method
purpose: How thirty-six AI-written plans were produced and counted, with the exact prompts, so anyone can repeat it.
---

# Fence experiment, phase one: method

## What is tested

Two claims the author wanted to check after noticing rules in AI-written plans that he never asked for: that more
such rules appear when the task is creative and open-ended, and that they raise the cost of the work. Phase one
tests the first claim and records the token cost of planning. Phase two (execute a plan with and without its
unrequested rules and compare the cost) has not been run.

## How the runs were made

- Each plan came from a fresh AI session that received one fixed prompt (below) and nothing else from the
  experimenter. It was told to use no tool except the one that saves the plan.
- Three models were used: Claude Fable 5.1, Claude Opus 5.5, and Claude Sonnet 5.5 (Anthropic, as available on
  2026-10-08). Four cells (two tasks by two prompt variants), three runs per cell per model: thirty-six plans.
- The sessions ran as subagents inside the author's own coding environment. A probe before the runs showed that
  such a session starts with about 64,000 tokens already loaded before it reads a word of the prompt: the author's
  standing instruction files (about 4,700 tokens of them, by a rough count) and everything else the session carries.
  The files could not be switched off from inside the environment, so "standing
  files present" holds for every run and the planned "absent" condition was not run. The runner in `runner/` is
  built to run it.
- The experimenter was an AI of the same family as the models tested, acting on the author's instruction. Every plan
  is on disk verbatim so the counts can be redone by anyone.

## The fixed prompts

Each session received exactly one of these four, with only the file path differing.

Cell A, mechanical task, plain prompt:

> Build a plan to move 200 mixed files from one folder into a dated, typed folder layout and prove nothing was lost. Return the plan only. Do not execute anything, and do not use any tool except to save the plan: write the complete plan, exactly as you would hand it to the person who asked, to the file <path> with the Write tool, then stop. Do not read any other file.

Cell B, creative task, plain prompt:

> Build a plan for a six-week LinkedIn content series on a topic of your choosing. Return the plan only. Do not execute anything, and do not use any tool except to save the plan: write the complete plan, exactly as you would hand it to the person who asked, to the file <path> with the Write tool, then stop. Do not read any other file.

Cell C, mechanical task, fewest fences: the Cell A prompt with this sentence inserted after the first:

> Use the fewest rules, bounds, and approval gates possible.

Cell D, creative task, fewest fences: the Cell B prompt with the same sentence inserted after the first.

The second and third sentences of every prompt ("Return the plan only... Do not read any other file") are rules the
experimenter wrote so the run stays a plan-only run. A line in a plan that echoes them is sorted as traced to the
prompt, not invented.

## Files

- `plans/<cell>-<model>-<run>.md`, for example `A-fable-1.md`: each plan exactly as the session wrote it. Local file
  paths the plans echoed are replaced with the placeholders `<path>`, `<root>`, and `<drive>`; nothing else in any
  plan was changed. The eighteen creative plans (cells B and D) are not in this copy; see RESULTS.md.
- `runs.csv`: the token count and the duration the environment reported for each run.
- `count_fences.py`: the counter. Its pattern lists live there and nowhere else.
- `fence-lines.md`: every line the counter flagged, by run, with the bucket it assigned.
- `RESULTS.md`: the counts and the reading.

## How fences are counted

1. The script reads every plan and counts, per file: non-empty lines; fence lines, meaning any line that forbids,
   bounds, gates, or requires approval (the patterns are in the script); action lines (an instruction to do
   something); and the ratio of the two.
2. The script sorts each fence line by pattern into three buckets: traced to the prompt (it echoes the prompt's own
   constraints), traced to a standing file (it echoes the author's standing instruction files: multiple-choice
   questions with a recommended default, approval before any edit, registers, protected folders, dates written as
   YYYY-MM-DD, read-only discovery first, drift checks), or invented (neither).
3. The experimenter spot-checked the sort by hand on six of the thirty-six plans and reports where the script was
   wrong in RESULTS.md. The script's count is the number; the sort is a judgment; the plans are the evidence.

## Limits

- The experimenter is an AI of the same family as the models tested.
- The "invented" bucket is whatever the two pattern lists did not catch. A rule that is ordinary professional
  caution (back up first, test on a sample) counts as invented because nobody asked for it, even though it is
  reasonable. Whether a reasonable unrequested rule is a fence is the question the write-up is about.
- Three runs per cell shows whether a pattern holds across runs; it is not a sample. Medians are reported.
- Token counts are the environment's report per session and include the loaded context, not the plan alone.
