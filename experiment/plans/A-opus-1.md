# Plan: move 200 mixed files into a dated, typed layout and prove nothing was lost

Plan date: 2026-10-08. Status: proposed, not executed. Nothing has been read, copied, or moved.

## Conclusion first

Copy, do not move. Each file gets a SHA-256 hash before anything changes, is copied to `<YYYY>\<YYYY-MM>\<type>\`, and is hashed again at the new location. The originals then go to a holding folder; they are not deleted. The job counts as proven only when four checks pass: the counts match, every source hash appears exactly once at the destination, no destination file is missing from the manifest, and total bytes match. You delete the holding folder yourself, after you have looked at the report. No agent deletes anything.

## What this plan needs from you before it runs

One question, with a recommended answer (A). Changing any of it changes only the parameters in Step 0; the steps stay the same.

**Q1. What decides a file's date and type?**
- **A (recommended).** Date: a `YYYY-MM-DD` in the filename if there is one, otherwise the file's last-modified time. Type: decided by extension, using the table in Step 2. Unknown extensions go to `_other\`.
- B. Date from last-modified time only; type by extension.
- C. Date from the photo's taken date (EXIF) where it exists, otherwise as in A; type by extension.
- D. Something else. Name it and I revise the plan.

I also need two paths, which are facts and not choices: the **source folder** and the **destination root**. If either is inside a [walled], [walled], or [walled] tree, the plan stops there and I do not open it.

## Step 0. Parameters (filled in from your answer)

| Parameter | Value |
|---|---|
| Source | `<source folder>`, top level only unless you say subfolders count |
| Destination root | `<destination root>` |
| Date rule | Q1 answer |
| Type rule | Step 2 table |
| Holding folder | `<source folder>\_moved-originals-2026-10-08\` |
| Run record | `<destination root>\_move-record-2026-10-08\` (manifest, logs, report) |

## Step 1. Read-only inventory (no approval needed beyond this plan)

1. List every file in the source, including hidden and system files. Record for each one: relative path, name, extension, size in bytes, last-modified time, attributes, and SHA-256 hash.
2. Write this to `manifest-before.csv` in the run record.
3. Report: total count (expected about 200; the measured number is what counts), total bytes, counts by extension, and any files that are zero bytes, locked, longer than 260 characters in path, or online-only placeholders that have not been downloaded from the sync service.
4. **Stop condition.** If the count is far from 200, if a file cannot be hashed, or if any name suggests a walled domain, I stop and report. I do not guess.

Because `<drive>` is a synced drive, I check that the sync client shows the source as fully synced before hashing, and again before Step 5.

## Step 2. Type table (proposed, adjustable)

| Folder | Extensions |
|---|---|
| `documents` | .docx .doc .pdf .txt .md .rtf .odt |
| `spreadsheets` | .xlsx .xls .csv .ods |
| `presentations` | .pptx .ppt .key .odp |
| `images` | .jpg .jpeg .png .gif .heic .webp .svg .tif .tiff |
| `video` | .mp4 .mov .avi .mkv .webm |
| `audio` | .mp3 .wav .m4a .aac .flac |
| `archives` | .zip .7z .rar .tar .gz |
| `_other` | anything not listed, and files with no extension |

Matching ignores case. The inventory in Step 1 shows every extension present, so any surprise is visible before anything moves.

## Step 3. Dry run: the move map (no files touched)

1. For each manifest row, compute the target path: `<destination root>\<YYYY>\<YYYY-MM>\<type>\<original name>`.
2. **Collisions.** If two files would land on the same target name, or a file already exists there, keep both: append ` (2)`, ` (3)` to the incoming name. Never overwrite. If the existing file has the same hash, mark it "already present" and do not copy it again.
3. Write `move-map.csv` (source path, hash, date used, which rule produced the date, type, target path, collision note).
4. Show you a summary: files per year-month-type folder, the collision list, the files that fell to `_other`, and the files whose date came from the fallback rule.

**Gate: you approve the move map** (1 approve · 2 approve with changes · 3 revise · 4 cancel) before Step 4.

## Step 4. Copy

1. Create only the folders the map needs.
2. Copy each file to its target, keeping its timestamps and attributes (for example `robocopy` with `/COPY:DAT /DCOPY:T`, one file at a time from the map, or `Copy-Item` followed by restoring the timestamps).
3. Log every copy with its result to `copy-log.csv`. A failure does not stop the others; it is listed and retried once, and then reported.
4. The source is not changed in this step.

## Step 5. Prove nothing was lost

Hash every file under the destination folders the map created and write `manifest-after.csv`. Then check:

| # | Check | Passes when |
|---|---|---|
| 1 | Count | files in `manifest-after` = rows in `move-map` (less any "already present") |
| 2 | Every source arrived intact | each source hash appears at its mapped target path |
| 3 | Nothing extra | no file in the destination folders is absent from the map |
| 4 | Bytes | total bytes before = total bytes after |
| 5 | Timestamps | last-modified time at the target = time at the source, to the second |
| 6 | Source untouched | rehash of the source matches `manifest-before` exactly |

Results go to `verification-report.md` in the run record, with every failing row named. **If any check fails, the plan stops here.** The originals are still in place and nothing is lost; I report the failures and propose a fix.

## Step 6. Retire the originals (only after all six checks pass)

1. Move the originals into the holding folder, keeping their names. This is a move within the same drive, not a delete.
2. Hash the holding folder and confirm it matches `manifest-before` (the originals are still whole).
3. The source folder is now empty apart from the holding folder. Report that.

**You** delete the holding folder when you are satisfied, or keep it. I recommend keeping it for at least one sync cycle and one look at the new layout.

## Step 7. Records and hand-off

- The run record holds: `manifest-before.csv`, `move-map.csv`, `copy-log.csv`, `manifest-after.csv`, `verification-report.md`.
- If this folder belongs to a domain with a plan record or register, I add one entry there that says what was moved and why, and links to the run record. I do not create a new register.
- Control report to you: counts, the six check results, the collision list, the `_other` list, and where the holding folder is.

## Rollback

Before Step 6: delete nothing, and if you want, remove the copies; the source never changed. After Step 6: move the files from the holding folder back to the source; `manifest-before.csv` proves the result matches the original.

## What would change this plan

- The source has subfolders whose structure matters. Then the target keeps the relative path under the type folder.
- The files are in a walled domain. Then the plan stops.
- The sync client cannot confirm that the files are fully local. Then Step 1 waits until it can.
- You want true moves instead of copy-then-retire. This is faster but loses the untouched-source safety net; I would not recommend it.

## Decision

1 approve as written · 2 approve with changes · 3 revise · 4 cancel
