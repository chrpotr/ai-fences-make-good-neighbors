---
title: Fence experiment, phase one, results
purpose: What thirty-six AI-written plans show about where fences come from, run on 2026-10-08 for issue 80. The table, the sort, and the reading. Raw plans are in plans/; the method and the fixed prompts are in README.md beside this file.
kind: record
status: run and counted 2026-10-08 by the strategy session on Chris's instruction; findings 1 and 2 reworded the same evening to state the per-model margins. Phase two (execute plans with and without their invented fences) not run.
sources:
  - README.md (method, prompts, departures from the approved design)
  - runs.csv (token count and duration per run, from the harness)
  - count_fences.py and fence-lines.md (the script's count and every fence line with its bucket)
  - plans/*.md (the thirty-six plans, verbatim)
read_by: Chris; the room when it outlines the demo post; anyone who recounts
---

# Fence experiment, phase one: results

## In plain words

Thirty-six fresh AI sessions were each handed one sentence of task and asked for a plan. Half the tasks were
mechanical (move 200 files, prove nothing was lost); half were creative (a six-week LinkedIn series). Half the
prompts added one sentence: "Use the fewest rules, bounds, and approval gates possible." Three models, three runs
each.

Four things came out.

1. **The mechanical task drew more fences than the creative one, not fewer.** Median 13 fence lines for the file
   move against 7 for the content series. Chris's hypothesis (more fences where the work is creative) is not what
   this grid shows. The direction held for all three models, but the margin differed: Opus 11 against 7, Sonnet 14
   against 6, Fable 11 against 10, one line. Read it as "not more fences in creative work," not as "far fewer."
2. **One sentence cut the fences by more than half and the plan by more than half.** Asking for the fewest rules
   took the file-move plan from 13 fence lines to 5 and from about 1,500 words to about 570; the series plan from 7
   to 3 and from about 1,200 words to 600. Plan length halved in every model and cell. Fence lines halved in five
   of six model-and-task pairs; Sonnet's creative plans fell by a third (6 to 4), not a half.
3. **Every one of the thirty-six plans ended with the same approval gate**, "1 approve as written · 2 approve with
   changes · 3 revise · 4 cancel", including all eighteen plans that were told to use the fewest gates possible.
   The prompt never asked for it. It comes from the Layer A rules file every session had loaded before it read the
   prompt: "Close every plan with: 1 approve as written..." That is a fence from a standing file, present in 100%
   of plans, immune to the instruction to use fewer.
4. **The creative plans imported Chris's whole operation without being told who was asking.** The prompt named no
   person. Nine of nine creative plans in the plain cell built the series on his Writers' Room pipeline, and six of
   nine addressed him by name; eight of nine fewest-fences creative plans picked "technical product marketing," the
   term his memory index holds from a test of two days earlier. The mechanical plans did none of that; instead seven
   of nine added a check that the folders were not in his walled domains. The standing files shaped what the plan was
   about, not only what it forbade.

The token cost was flat: every run cost 65,600 to 76,400 tokens, because about 64,000 of that is the context a
fresh session carries before it reads a word. The plan itself is a few thousand tokens. Fewer fences saved about 3%.

## The grid

Medians across the three runs of each cell and model. Fence lines are the script's count (a lower bound; see
"What the script missed"). Invented means neither echoed from the prompt nor from a standing file, by pattern.

| Cell | Task | Prompt | Fence lines | Invented | Words | Tokens per run | Seconds |
|---|---|---|---|---|---|---|---|
| A | mechanical | plain | 13 | 11 | 1,491 | 74,040 | 69 |
| B | creative | plain | 7 | 6 | 1,213 | 74,164 | 65 |
| C | mechanical | fewest fences | 5 | 5 | 569 | 71,899 | 47 |
| D | creative | fewest fences | 3 | 3 | 601 | 71,765 | 38 |

By model, fence lines (median of 3 runs):

| Cell | Fable 5.1 | Opus 5.5 | Sonnet 5.5 |
|---|---|---|---|
| A | 11 | 11 | 14 |
| B | 10 | 7 | 6 |
| C | 5 | 5 | 7 |
| D | 2 | 3 | 4 |

The three models move together. Sonnet was fastest in every cell (21 to 44 seconds against 38 to 107). No model
stood out on fence count beyond run-to-run noise.

## Where the fences came from

Markers from Chris's standing files, counted as plans containing each, out of 9 per cell:

| Marker | What it echoes | A | B | C | D | All 36 |
|---|---|---|---|---|---|---|
| "1 approve as written · 2 approve with changes · 3 revise · 4 cancel" | Layer A, "Close every plan with" | 9 | 9 | 9 | 9 | 36 |
| His pipeline by name (/interview, /outline, /polish, Writers' Room) | the memory index | 0 | 9 | 0 | 3 | 12 |
| "technical product marketing" as the series topic | the 2026-10-06 term test in memory | 0 | 9 | 0 | 8 | 17 |
| "Chris" named | the memory index | 0 | 6 | 0 | 4 | 10 |
| a check that the folders are not walled (FINANCIALS, FAMILY, HEALTH) | Layer A hard walls | 7 | 3 | 0 | 1 | 11 |
| "read-only" discovery first | Layer A work-order sequence | 9 | 2 | 6 | 0 | 17 |
| "design freeze" | the memory index, this week's decision | 0 | 6 | 0 | 1 | 7 |
| "multiple-choice" questions with a recommended default | Layer A interaction rule | 1 | 3 | 0 | 0 | 4 |

Two readings. The "fewest fences" sentence did suppress standing-file fences in the mechanical task (walled-domain
checks 7 to 0, read-only steps 9 to 6) but could not touch the approval gate (9 to 9). And the creative task pulled
in far more of his standing material than the mechanical one: the model, asked for a content series by nobody in
particular, reached for the one person whose content operation was in its context.

What the script sorted as "invented" is, on the hand check, almost entirely professional caution nobody asked for:
copy before you delete, stop if the count is not 200, never overwrite, hash everything twice, hold the originals,
one approval before any write. Reasonable, every one. Also unrequested, every one. Whether a reasonable unrequested
rule is a fence is the question the post is about.

## What the script missed (the count is a lower bound)

- Rules phrased as positives carry no fence word: "You write the words." "Every story comes from your own
  experience." The two plans the script scored at zero fences (D-opus-1, D-sonnet-1) each hold two or three such
  rules plus the approval gate.
- The approval gate itself is not counted as a fence line by the script, because its line has no forbidding word.
  Counted by hand above: 36 of 36.
- The do-versus-don't ratio only counts lines that open with an action verb, so table rows and prose steps are
  missed. It is not reported as a result.
- The "standing" bucket is small by pattern (0 to 3 per plan) because the pattern list is short. The marker table
  above is the better measure of standing-file influence.

Everything the script did and did not catch is in `fence-lines.md`, one line per fence with its bucket, so the sort
can be redone by anyone.

## What this does and does not establish

| Claim | Status after phase one |
|---|---|
| More fences appear when the task is creative (A10) | Not supported here. The mechanical task drew nearly twice as many fence lines. Three models, three runs each |
| Fences raise token spend (A18) | Not tested. Phase one measured planning cost only; planning with fewer fences cost about 3% less. Phase two (execution) is where the claim lives |
| Rules a user never asked for appear in AI plans | Supported, two ways: invented caution in every plan, and standing-file rules in every plan (the approval gate in 36 of 36) |
| One sentence in the prompt removes most of them | Supported for invented fences and for most standing-file fences; not for the one the user's own law demands |
| The standing files shape the plan's subject, not just its rules | Supported in the creative cells (his pipeline in 9 of 9 plain plans; his search term in 8 of 9 fewest-fences plans), absent in the mechanical cells |

## Limits

- The experimenter is an AI of the same family as the three models; the design said it should not be, and Chris
  overrode that for this run.
- Standing files were present on every run. The "absent" cell could not be run from inside this session.
- Three runs per cell. The patterns are consistent across models and runs, which is why they are reported; they are
  not statistics.
- The tasks were shapes, not real work. A real folder and a real series would carry their own constraints.
- Token counts include the loaded context; the plan's own share is a few thousand tokens per run and was not
  separated.

## Files

| File | What it is |
|---|---|
| `README.md` | method, the four fixed prompts verbatim, departures from the approved design |
| `plans/<cell>-<model>-<n>.md` | the thirty-six plans, verbatim, as each subagent wrote them |
| `runs.csv` | token count and seconds per run, as the harness reported them |
| `count_fences.py` | the counter; the pattern lists are in it and nowhere else |
| `fence-lines.md` | every fence line the script found, by run, with its bucket |
| `RESULTS.md` | this file |

Total spend for the thirty-six runs: 2,628,530 tokens as reported by the harness, about 64,000 of each run being
loaded context.
