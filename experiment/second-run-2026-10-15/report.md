# Fence experiment, cloud grid: results

Runs analyzed: 600. CLI: 2.1.300 (Claude Code). Runs naming more than one model: 0. Runs with more than one turn: 2.
Total tokens: 9,743,801. Claude Code's list-price estimate: $76.76.

Cells with other than 10 runs: none.

## Confirmatory tests (fence lines, runner's word list; negative binomial, all 600 runs)

| Hypothesis | Effect | Ratio | 95% interval | p | Holm p | Same direction on batch 1's list |
|---|---|---|---|---|---|---|
| H1 task | creative / mechanical | 0.54 | 0.50 to 0.58 | 6.47e-62 | 1.29e-61 | yes |
| H2 prompt | fewest / plain | 0.37 | 0.34 to 0.39 | 2.15e-163 | 6.46e-163 | yes |
| H3 effort | joint test, 4 df (chi-square 236.0) | | | 6.64e-50 | 6.64e-50 | |
| H3 trend | per effort step | 1.20 | 1.17 to 1.23 | 4.9e-50 | | yes |

H5 (exploratory) models differ: chi-square 136.8, 2 df, p 1.94e-30.

## Predicted fence lines by model and effort (average of the four cells, 95% interval)

| Model | low | medium | high | xhigh | max |
|---|---|---|---|---|---|
| claude-opus-5-5 | 5.4 (4.6 to 6.4) | 6.6 (5.8 to 7.6) | 8.3 (7.2 to 9.5) | 8.6 (7.5 to 9.9) | 14.6 (12.9 to 16.4) |
| claude-sonnet-5-5 | 6.3 (5.5 to 7.3) | 6.5 (5.6 to 7.5) | 8.4 (7.4 to 9.7) | 9.7 (8.5 to 11.0) | 10.8 (9.6 to 12.2) |
| claude-haiku-5-5 | 9.1 (8.0 to 10.4) | 11.0 (9.7 to 12.5) | 11.4 (10.1 to 12.9) | 13.6 (12.1 to 15.3) | 18.4 (16.5 to 20.5) |

## Mean fence lines per cell (runner's word list, 10 runs, 95% interval)

| Model | Effort | A mechanical, plain | B creative, plain | C mechanical, fewest | D creative, fewest |
|---|---|---|---|---|---|
| claude-opus-5-5 | low | 8.6 (6.9 to 10.3) | 5.5 (3.7 to 7.3) | 4.9 (3.8 to 6.0) | 2.5 (1.5 to 3.5) |
| claude-opus-5-5 | medium | 12.6 (9.4 to 15.8) | 8.0 (5.6 to 10.4) | 5.0 (3.5 to 6.5) | 1.3 (0.4 to 2.2) |
| claude-opus-5-5 | high | 16.1 (13.3 to 18.9) | 8.2 (6.0 to 10.4) | 6.8 (5.0 to 8.6) | 2.4 (1.8 to 3.0) |
| claude-opus-5-5 | xhigh | 14.6 (12.3 to 16.9) | 11.1 (8.1 to 14.1) | 6.5 (4.7 to 8.3) | 2.5 (1.8 to 3.2) |
| claude-opus-5-5 | max | 19.0 (14.6 to 23.4) | 25.7 (22.1 to 29.3) | 6.5 (4.9 to 8.1) | 6.4 (3.3 to 9.5) |
| claude-sonnet-5-5 | low | 11.6 (10.6 to 12.6) | 7.4 (5.8 to 9.0) | 4.9 (4.1 to 5.7) | 1.7 (0.8 to 2.6) |
| claude-sonnet-5-5 | medium | 11.7 (9.9 to 13.5) | 6.9 (5.0 to 8.8) | 5.1 (4.2 to 6.0) | 2.2 (1.5 to 2.9) |
| claude-sonnet-5-5 | high | 13.9 (10.7 to 17.1) | 9.9 (7.2 to 12.6) | 6.4 (4.2 to 8.6) | 3.4 (2.4 to 4.4) |
| claude-sonnet-5-5 | xhigh | 16.5 (13.8 to 19.2) | 13.5 (10.7 to 16.3) | 5.8 (4.3 to 7.3) | 3.2 (2.3 to 4.1) |
| claude-sonnet-5-5 | max | 18.4 (15.8 to 21.0) | 18.6 (14.0 to 23.2) | 4.5 (3.8 to 5.2) | 2.9 (1.9 to 3.9) |
| claude-haiku-5-5 | low | 17.1 (14.6 to 19.6) | 6.5 (4.4 to 8.6) | 10.4 (8.8 to 12.0) | 2.4 (1.1 to 3.7) |
| claude-haiku-5-5 | medium | 19.9 (15.7 to 24.1) | 8.4 (5.1 to 11.7) | 12.5 (9.8 to 15.2) | 3.1 (1.6 to 4.6) |
| claude-haiku-5-5 | high | 17.7 (14.9 to 20.5) | 9.7 (7.5 to 11.9) | 13.4 (10.9 to 15.9) | 3.9 (2.3 to 5.5) |
| claude-haiku-5-5 | xhigh | 19.7 (14.8 to 24.6) | 17.2 (13.5 to 20.9) | 13.1 (9.9 to 16.3) | 3.9 (2.9 to 4.9) |
| claude-haiku-5-5 | max | 24.3 (17.8 to 30.8) | 25.3 (20.8 to 29.8) | 15.2 (11.7 to 18.7) | 7.1 (5.5 to 8.7) |

## Mean fence lines per cell, batch 1's word list

| Model | Effort | A | B | C | D |
|---|---|---|---|---|---|
| claude-opus-5-5 | low | 6.7 | 3.0 | 3.8 | 1.2 |
| claude-opus-5-5 | medium | 8.5 | 4.8 | 4.0 | 0.9 |
| claude-opus-5-5 | high | 10.9 | 6.5 | 4.4 | 1.2 |
| claude-opus-5-5 | xhigh | 8.6 | 7.2 | 4.7 | 1.9 |
| claude-opus-5-5 | max | 11.4 | 19.4 | 5.5 | 5.5 |
| claude-sonnet-5-5 | low | 10.6 | 4.7 | 5.9 | 1.0 |
| claude-sonnet-5-5 | medium | 9.5 | 4.0 | 4.8 | 1.2 |
| claude-sonnet-5-5 | high | 10.0 | 6.6 | 5.3 | 2.0 |
| claude-sonnet-5-5 | xhigh | 11.6 | 8.1 | 4.5 | 1.8 |
| claude-sonnet-5-5 | max | 12.8 | 13.4 | 3.6 | 2.2 |
| claude-haiku-5-5 | low | 14.3 | 4.2 | 9.8 | 1.6 |
| claude-haiku-5-5 | medium | 17.9 | 5.3 | 11.0 | 2.5 |
| claude-haiku-5-5 | high | 14.1 | 7.9 | 11.0 | 2.4 |
| claude-haiku-5-5 | xhigh | 15.3 | 12.9 | 10.0 | 3.1 |
| claude-haiku-5-5 | max | 17.3 | 17.6 | 10.8 | 4.7 |

## Secondary: fence lines per plan line (rate model, log of plan lines as offset)

- Task, creative / mechanical: 0.61 (0.57 to 0.65), p 2.03e-46
- Prompt, fewest / plain: 0.89 (0.83 to 0.95), p 0.000458
- Effort, joint: chi-square 2.9, 4 df, p 0.581; per step 1.02 (0.99 to 1.04)

| Model | Effort | A per 100 lines | B per 100 lines | C per 100 lines | D per 100 lines |
|---|---|---|---|---|---|
| claude-opus-5-5 | low | 9.3 | 5.7 | 10.2 | 6.0 |
| claude-opus-5-5 | medium | 9.7 | 6.5 | 7.4 | 3.1 |
| claude-opus-5-5 | high | 10.6 | 6.2 | 8.9 | 4.2 |
| claude-opus-5-5 | xhigh | 8.6 | 6.6 | 7.2 | 5.3 |
| claude-opus-5-5 | max | 9.1 | 8.4 | 7.2 | 7.4 |
| claude-sonnet-5-5 | low | 15.5 | 8.5 | 17.1 | 4.8 |
| claude-sonnet-5-5 | medium | 15.0 | 7.9 | 14.9 | 5.4 |
| claude-sonnet-5-5 | high | 15.8 | 9.5 | 14.9 | 7.5 |
| claude-sonnet-5-5 | xhigh | 17.6 | 12.0 | 12.3 | 7.2 |
| claude-sonnet-5-5 | max | 14.0 | 10.5 | 10.3 | 6.6 |
| claude-haiku-5-5 | low | 17.2 | 7.5 | 25.3 | 6.3 |
| claude-haiku-5-5 | medium | 17.4 | 8.6 | 23.1 | 8.1 |
| claude-haiku-5-5 | high | 17.0 | 11.1 | 21.9 | 9.5 |
| claude-haiku-5-5 | xhigh | 16.0 | 12.7 | 21.9 | 9.5 |
| claude-haiku-5-5 | max | 13.2 | 13.7 | 16.7 | 15.8 |

## Tokens and cost per run, by model and effort (mean of 40 runs)

| Model | Effort | Output | Thinking | Plan text | Total | Cost | Seconds |
|---|---|---|---|---|---|---|---|
| claude-opus-5-5 | low | 1,913 | 0 | 1,913 | 4,070 | $0.0413 | 22 |
| claude-opus-5-5 | medium | 3,058 | 561 | 2,498 | 5,215 | $0.0642 | 34 |
| claude-opus-5-5 | high | 4,113 | 1,146 | 2,967 | 6,270 | $0.0853 | 44 |
| claude-opus-5-5 | xhigh | 8,058 | 4,777 | 3,281 | 10,268 | $0.1642 | 83 |
| claude-opus-5-5 | max | 54,679 | 49,792 | 4,887 | 56,836 | $1.0947 | 534 |
| claude-sonnet-5-5 | low | 1,887 | 76 | 1,811 | 4,048 | $0.0205 | 18 |
| claude-sonnet-5-5 | medium | 2,056 | 164 | 1,892 | 4,216 | $0.0221 | 19 |
| claude-sonnet-5-5 | high | 3,176 | 860 | 2,315 | 5,336 | $0.0334 | 28 |
| claude-sonnet-5-5 | xhigh | 4,739 | 2,257 | 2,482 | 6,900 | $0.0489 | 41 |
| claude-sonnet-5-5 | max | 29,380 | 25,928 | 3,453 | 31,542 | $0.2943 | 221 |
| claude-haiku-5-5 | low | 2,039 | 40 | 1,999 | 4,978 | $0.0011 | 12 |
| claude-haiku-5-5 | medium | 2,870 | 595 | 2,275 | 5,809 | $0.0015 | 16 |
| claude-haiku-5-5 | high | 5,020 | 2,691 | 2,329 | 7,958 | $0.0026 | 27 |
| claude-haiku-5-5 | xhigh | 11,728 | 8,863 | 2,865 | 14,667 | $0.0060 | 56 |
| claude-haiku-5-5 | max | 69,194 | 64,671 | 4,522 | 75,481 | $0.0388 | 298 |

## Token outcomes (log scale, same terms; ratios)

- output_tokens: creative / mechanical 0.73; fewest / plain 0.49; per effort step 2.10
- plan_tokens: creative / mechanical 0.97; fewest / plain 0.39; per effort step 1.18
- thinking_tokens: creative / mechanical 0.25; fewest / plain 0.52; per effort step 11.05
- total_tokens: creative / mechanical 0.80; fewest / plain 0.64; per effort step 1.72

## H4: within a cell, do plans with more fence lines use more tokens? (pooled within-cell correlation)

- fences vs output_tokens: r = 0.03 (-0.06 to 0.11) (pre-registered)
- fences vs plan_tokens: r = 0.39 (0.32 to 0.46) (exploratory)
- fences vs thinking_tokens: r = -0.00 (-0.09 to 0.08) (exploratory)

Word-list counts are a proxy: rules phrased as positives go uncounted, and some flagged lines are not rules.
Standing files were absent in every run. A session ran the experiment.
