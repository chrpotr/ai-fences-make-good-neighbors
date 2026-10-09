# ai-fences-make-good-neighbors

DRAFT. Chris writes this file; the lines below are placeholders that say what each section holds, not his words.

[One line: what this repository is. An experiment on where the rules in an AI's plan come from, and a write-up.]

[One line: the headline numbers. 36 plans, 3 models, 2 tasks, 2 prompts; the approval gate in 36 of 36; one sentence
halved the rest.]

[One line: where the write-up is: https://chrpotr.github.io/articles/fences/ (the address the article's filename gives; change if the slug changes).]

[One line: how to run the experiment yourself: experiment/runner/README.md.]

[One line: licence, and that this repository carries no agent instruction file on purpose.]

## Contents

| Path | What it is |
|---|---|
| the article on chrpotr.github.io | the write-up, linked from the top of this file |
| `experiment/README.md` | the method and the four fixed prompts, verbatim |
| `experiment/RESULTS.md` | the results of the first run, with the same-evening corrections |
| `experiment/plans/` | the plans, one file per run, verbatim |
| `experiment/runs.csv` | tokens and seconds per run |
| `experiment/count_fences.py` | the counter; the pattern lists live here and nowhere else |
| `experiment/fence-lines.md` | every fence line the counter found, with its bucket |
| `experiment/runner/` | the runner for Claude Code and Codex, to run the cells yourself |
