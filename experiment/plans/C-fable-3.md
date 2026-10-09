# Plan: move 200 mixed files into a dated, typed layout and prove nothing was lost

Written 2026-10-08. Nothing has been run. Nothing is touched until you answer the one question at the end.

## What this does

Copies every file in one folder into `<destination>\<YYYY-MM>\<type>\`, proves the copy is byte-for-byte complete, then renames the old folder out of the way. One approval, one bound, three rules.

## The bound

Only two paths are touched: the source folder you name, and the destination root you name. Nothing else is read, written, or listed.

## The rules

1. **Date** = the file's last-modified date, as `YYYY-MM`. (Creation dates are unreliable after copies; modified is the one every file carries.)
2. **Type** = by extension, five buckets: `documents` (pdf, doc, docx, txt, md, rtf), `images` (jpg, jpeg, png, gif, heic, webp, svg), `spreadsheets` (xls, xlsx, csv), `archives` (zip, 7z, rar, tar, gz), `other` (everything else, including no extension). Nothing is left out: `other` is the catch-all.
3. **Collision** = two files mapped to the same destination path get `-2`, `-3` appended before the extension. Original filenames are never otherwise changed.

## Steps

**1. Inventory (read-only).**
Walk the source folder. For each file record: path, size in bytes, SHA-256, last-modified date. Save as `manifest-before.csv` in the destination root. The row count is the baseline. If it is not 200, the real count is reported and becomes the baseline; the plan does not change.

**2. Mapping (read-only).**
Apply the three rules to the inventory. Save `mapping.csv` (source path → destination path). Produce a one-screen summary: files per month, files per type, number of collisions, number landing in `other`.

**3. The one approval gate.**
You see the summary and answer the question below. Yes means steps 4 to 6 run without stopping.

**4. Copy.**
Copy (not move) every file per `mapping.csv`, creating folders as needed. Sources are untouched until step 6.

**5. Prove it.**
Walk the destination. Record the same four fields for every file as `manifest-after.csv`. Pass means all three hold:
- row count equals the baseline;
- every source hash appears exactly once, at exactly the destination `mapping.csv` says;
- no file exists in the destination that is not in `mapping.csv`.
Any failure stops here. Sources are still intact, so the fix is to rerun the failed copy and re-verify. Nothing can be lost at this point because nothing has been removed.

**6. Retire the source.**
Rename the source folder to `<source>-moved-2026-10-08`. It is not deleted. You delete it when you are satisfied, on your own time. This keeps "move" semantics (the old folder name is gone) and a full recovery path, without a second approval.

## What you get

- `manifest-before.csv`, `manifest-after.csv`, `mapping.csv` in the destination root.
- One line: `N files, N matched, 0 missing, 0 extra, 0 hash mismatches`.
- The renamed source folder, intact, for you to delete.

## What would change the plan

- You want the date from a date inside the filename rather than modified time: rule 1 changes, nothing else does.
- You want fewer or different type buckets: rule 2 changes, nothing else does.
- The source contains subfolders: the plan flattens them (step 1 walks recursively). If you want subfolder names preserved, say so and the destination path gains one segment.

## Your call

1. **Approve as written** (recommended)
2. Approve with changes (name the rule to change)
3. Revise
4. Cancel
