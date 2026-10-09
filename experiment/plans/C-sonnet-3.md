# Plan: move 200 mixed files into a dated, typed layout, and prove nothing was lost

## Conclusion

Record every file's name, size, and SHA-256 fingerprint before the move, move the files, record the same fingerprints after, and compare. If the two lists match with 200 entries each, nothing was lost, changed, or duplicated. One approval gate (this plan). Everything else runs straight through.

## What I need from you (defaults apply if you say nothing beyond approve)

Two facts are not in the request. They are the only things the plan depends on:

- Source folder: the folder that holds the 200 files.
- Destination root: where the new layout goes. Default: a new folder named `sorted` created next to the source folder, never inside it.

If you approve without naming them, I stop and ask. I will not guess a path.

## The layout

`<destination>\YYYY-MM\<type>\<original file name>`

- Date: the file's last-modified date, as YYYY-MM.
- Type, by extension, in six buckets: `documents` (doc, docx, pdf, txt, md, rtf, odt), `sheets` (xls, xlsx, csv), `slides` (ppt, pptx, key), `images` (jpg, jpeg, png, gif, heic, svg, webp), `media` (mp3, mp4, mov, wav), `other` (everything else, including files with no extension).
- Names are kept exactly. If two files would land on the same path, the second gets `-2` before the extension. Nothing is ever overwritten.

## Steps

1. Count and fingerprint (read-only). List the source folder's files, confirm the count is 200, and write `before.csv` with path, size, and SHA-256 for each. If the count is not 200, stop and report the real number. Subfolders: count only files directly in the folder unless the count shows files below it, in which case I report it and stop.
2. Dry run (read-only). From `before.csv`, write `plan-moves.csv` with each file's source path and target path. Check that there are 200 rows and no two rows share a target. You can look at it; you do not need to.
3. Move. Create the folders, then move each file per `plan-moves.csv`. Moves, not copies, so no leftovers are created. The log is `plan-moves.csv` itself, so every move can be reversed from it.
4. Fingerprint again. Write `after.csv` with the same columns from the destination.
5. Compare. Proof of no loss requires all four to hold:
   - `after.csv` has 200 rows.
   - Every SHA-256 in `before.csv` appears in `after.csv` the same number of times (so no file was lost, changed, or duplicated).
   - Each file's size is unchanged.
   - The source folder has 0 files left.
6. Report. One short control report: counts before and after, the four checks as pass or fail, and the three CSV paths. The CSVs sit in the destination root as the permanent receipt.

## If something fails

Any check that fails halts the run at that step. If the failure is after step 3, I reverse the moves from `plan-moves.csv`, re-run the fingerprint, and report. I do not retry or improvise.

## What this plan deliberately does not have

No per-bucket approvals, no sampling, no second reviewer, no extra register. The fingerprint comparison is the proof, and it covers all 200 files rather than a sample. The only gate is your approval below.

## Decision

Approve or change this plan:

1. approve as written (recommended, once you have given me the source folder and destination root, or accepted the `sorted` default)
2. approve with changes
3. revise
4. cancel
