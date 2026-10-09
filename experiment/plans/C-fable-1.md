# Plan: move 200 mixed files into a dated, typed layout and prove nothing was lost

Written 2026-10-08. Status: proposed, not executed. Nothing has been read or touched.

## What this does and why

One folder holds 200 files of mixed kinds. After this runs, every file sits at
`<dest>\YYYY-MM\<type>\<filename>`, the source folder is empty, and a manifest shows
that the 200 files that went in are byte-for-byte the 200 files that came out.
Nothing is renamed except to break a name collision, and nothing is deleted from the
source until the copy has been verified by hash.

## The three rules

1. **Date** = the file's last-modified date, formatted `YYYY-MM`. (Creation dates are
   unreliable after copies; modified dates survive.)
2. **Type** = by extension, into one of six folders:
   `documents` (pdf docx doc txt md rtf odt), `spreadsheets` (xlsx xls csv ods),
   `slides` (pptx ppt key odp), `images` (jpg jpeg png gif heic webp svg),
   `media` (mp3 mp4 mov wav m4a), `other` (everything else, including no extension).
3. **Collision** = if the target path already exists, append `~<first 8 hex of SHA-256>`
   before the extension. Nothing is ever overwritten.

## The one bound

Only two folders are written to: the destination tree, and the source (deletes only,
after verification). Nothing else on disk is touched.

## The one gate

Your approval of this plan. After that it runs end to end with no further questions,
unless the verification in step 4 fails, in which case it stops and reports.

## Steps

1. **Inventory (read-only).** Walk the source. Record for each file: relative path,
   size, SHA-256, modified date, computed target path. Write this as
   `<dest>\_manifest\before.csv`. Assert the count is 200. If it is not 200, stop and
   report the real count before anything moves.
2. **Copy.** For each row, create the target folder if needed and copy the file to its
   target path. Preserve timestamps. Append the actual target path to the row.
3. **Verify.** Hash every copied file. Write `<dest>\_manifest\after.csv`. Compare to
   `before.csv`: same count, every source hash present exactly once in the destination,
   every destination file traceable to one source row.
4. **Delete source files** only if step 3 passed with zero mismatches. Then assert the
   source folder is empty of files. If step 3 failed, delete nothing and report the
   mismatching rows.
5. **Report.** One table: files found, files copied, hashes matched, collisions renamed,
   source files deleted, source files remaining. All six numbers, plus the path to the
   two manifests.

## What proves nothing was lost

- `before.csv` has 200 rows; `after.csv` has 200 rows.
- The multiset of SHA-256 values is identical in both.
- Total bytes are identical in both.
- The source folder contains zero files at the end.
- The manifests stay on disk so the proof can be re-run at any later date.

## What would change this plan

- The source folder does not hold 200 files (step 1 catches this and stops).
- You want a different date basis (creation date, or a date parsed from the filename).
- You want different or fewer type buckets.
- You want the source files kept rather than deleted (then step 4 is dropped and the
  plan is a copy with proof, not a move).

## Decision

1. Approve as written (recommended)
2. Approve with changes — name the rule or step to change
3. Revise — send it back
4. Cancel
