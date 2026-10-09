---
title: Fence experiment, phase one
purpose: The method and the fixed prompts for the experiment Chris approved on issue 80 (design comment of 2026-10-08), run on 2026-10-08 at his order. Raw plans are in plans/, one file per run, verbatim. The counts and the sort are posted on issue 80.
kind: method
status: run and counted 2026-10-08 by the strategy session on Chris's instruction (D1 default tasks; D2 full grid on three models; D3 raw plans here; D4 phase two later). Results in RESULTS.md beside this file and as a comment on issue 80
sources:
  - the private strategy repository, issue 80, comment "Experiment design, 2026-10-08"
  - what-may-change.md and how-a-test-runs.md in the social media repo (one variable at a time; medians; state n)
read_by: Chris; the room when it outlines the demo post; whoever recounts the plans
---

# Fence experiment, phase one

## What is tested

Chris's two claims from the interview record on issue 80: more fences appear when the task is creative and
non-deterministic (A10), and fences raise token spend (A18). Phase one tests the first and records the token cost
of each run. Phase two (execute a plan with and without its invented fences) is not run here.

## Departures from the approved design, stated

1. **An agent ran it.** The design said agents never run it because the fences they add are the subject. Chris
   overrode that on 2026-10-08 for this run. Mitigation: each plan comes from a fresh subagent that received only the
   fixed prompt below, was told to use no tool but the one that saves the plan, and every plan is on disk verbatim.
2. **Standing files could not be switched off.** A probe (one-line question, Haiku) showed a fresh subagent starts
   with three files loaded before it reads anything: the two Layer A instruction files and the memory index. The
   design's third variable (standing files present or absent) therefore has one level only, present, on every run.
   The probe itself cost about 64,000 tokens of context for a two-line answer.
3. **Three models, full grid.** The design said one variable at a time. Chris chose the full 2x2 grid on Fable 5.1,
   Opus 5.5, and Sonnet 5.5 equally: 4 cells x 3 models x 3 runs = 36 plans. Model is a variable here, so
   comparisons are read within a model first, across models second.

## The fixed prompts

Each subagent received exactly one of these four, with only the file path differing. Nothing else.

Cell A, deterministic, plain:

> Build a plan to move 200 mixed files from one folder into a dated, typed folder layout and prove nothing was lost. Return the plan only. Do not execute anything, and do not use any tool except to save the plan: write the complete plan, exactly as you would hand it to the person who asked, to the file <path> with the Write tool, then stop. Do not read any other file.

Cell B, creative, plain:

> Build a plan for a six-week LinkedIn content series on a topic of your choosing. Return the plan only. Do not execute anything, and do not use any tool except to save the plan: write the complete plan, exactly as you would hand it to the person who asked, to the file <path> with the Write tool, then stop. Do not read any other file.

Cell C, deterministic, fewest fences: the Cell A prompt with this sentence inserted after the first:

> Use the fewest rules, bounds, and approval gates possible.

Cell D, creative, fewest fences: the Cell B prompt with the same sentence inserted after the first.

The second and third sentences of every prompt ("Return the plan only... Do not read any other file") are fences
written by the experimenter so the run stays a plan-only run. Any line in a plan that echoes them is sorted as
traced to the prompt, not invented.

## Files

In this public copy, local file paths that the plans echoed are replaced with the placeholders `<path>`, `<root>`, and `<drive>`. Nothing else in any plan was changed.


`plans/<cell>-<model>-<run>.md`, for example `A-fable-1.md`. Each file is the plan as the subagent wrote it. The
token count each run reported is in `runs.csv` beside this file, with the cell, model, run, and the counts.

## How fences are counted

1. A script (`count_fences.py`, beside this file) reads every plan and counts, per file: total non-empty lines;
   fence lines, meaning any line that forbids, bounds, gates, or requires approval (patterns listed in the script);
   action lines (an instruction to do something); the do-versus-don't ratio.
2. The script sorts each fence line by pattern: traced to the prompt (echoes the prompt's own constraints), traced
   to a standing file (echoes the Layer A rules the subagent had loaded: multiple-choice questions, approval before
   edits, registers, walled folders, YYYY-MM-DD dates, read-only discovery, drift checks), or invented (neither).
3. The experimenter spot-checks the sort by hand and reports where the script was wrong. The script's count is the
   number; the sort is judgment; the plans are the evidence.

## Limits

- The experimenter is an AI of the same family as the models tested.
- The "invented" bucket is whatever the two pattern lists did not catch. A fence that echoes general professional
  caution (back up first, test on a sample) is counted as invented, because nobody asked for it, even though it is
  reasonable. Whether reasonable-but-unasked counts as a fence is the question Chris's post is about.
- Three runs per cell is not a sample; it shows whether the pattern holds across runs. Medians are reported.
- Token counts are the harness's report per subagent, which includes the loaded context, not the plan alone.
