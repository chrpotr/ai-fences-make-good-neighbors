# Plan: move 200 mixed files into a dated, typed layout and prove nothing was lost

Written 2026-10-08. Status: PROPOSED, nothing executed. No folder was read to write this; the source path, the destination root, and the type list are placeholders you fill in at step 0.

## Conclusion first

Copy, never move, until the proof passes. Build a manifest of the source (path, size, SHA-256) before anything is touched; copy every file into `<root>\<YYYY>\<YYYY-MM>\<type>\`; build a second manifest of the destination; prove the two manifests match as a set of hashes, with a count of 200 on both sides and no extra files on either; only then delete the source files, and keep both manifests and a move log as the permanent record. If the proof fails at any step, nothing has been deleted and the source is exactly as it was.

The plan has eight steps, two of which need your answer before I start (step 0), and one of which (step 6, delete the originals) needs a separate yes on the day.

## What "dated, typed" means here

- Date comes from the file's **last-modified time** by default. Creation time on Windows is unreliable after copies and downloads, and nothing in a filename can be trusted to be a date. If a file carries a date in its name that you would rather use, that is a per-file ruling, not a default.
- Type comes from the **extension**, grouped into named buckets. Proposed buckets, to be confirmed:

| Bucket | Extensions |
|---|---|
| `documents` | .docx .doc .pdf .md .txt .rtf .odt |
| `spreadsheets` | .xlsx .xls .csv .tsv |
| `slides` | .pptx .ppt .key |
| `images` | .png .jpg .jpeg .gif .webp .svg .heic |
| `audio-video` | .mp3 .wav .m4a .mp4 .mov .mkv |
| `archives` | .zip .7z .rar .tar .gz |
| `code-data` | .json .xml .yaml .yml .py .ps1 .js .html .css |
| `other` | anything not above, including files with no extension |

- Final shape: `<root>\2026\2026-10\documents\report.docx`. Year then year-month so a year folder stays browsable, and the type sits inside the month so "what did I touch in October" is one folder.

## Steps

### Step 0: your answers (before anything runs)

Two questions, each multiple-choice, one recommended default.

**Q1. Which date drives the folder?**
1. Last-modified time (recommended: it survives copies, it is what Explorer shows by default)
2. Creation time
3. A date parsed from the filename, falling back to last-modified

**Q2. What happens to the originals after the proof passes?**
1. Delete them, leaving an empty source folder plus the three record files (recommended)
2. Leave them in place and treat the new tree as a second copy
3. Move them to a single `_moved-2026-10-08` folder beside the source, as a belt-and-braces copy you delete yourself later

I also need the two paths: source folder and destination root. The destination root must be empty or not yet exist, so the "no extras" check is meaningful.

### Step 1: freeze and record the source (read-only)

- Count the files, top-level only. Confirm the count is 200. If it is not 200, stop and report the real number before going on, because every later check is against that number.
- Check for subfolders. The brief says "one folder"; if subfolders exist, stop and ask whether they are in scope.
- Write `MANIFEST-source.csv`: one row per file with relative path, byte size, last-modified (ISO 8601), SHA-256.
- Record the total bytes.
- Check for duplicate hashes inside the source. Two files with the same content but different names are both kept; the manifest records them so the destination count can still reach 200.
- Check for name collisions in the destination layout: two files that would land at the same `<year>\<month>\<type>\<name>`. Expected to be rare since names were unique in one folder, but the check runs anyway. A collision gets the suffix ` (2)` before the extension and is listed in the move log.

Nothing is written inside the source folder. The manifest goes next to the destination root, in a `_records` folder.

### Step 2: dry run

- Compute the full mapping, source path to destination path, and write it as `MOVE-LOG.csv` with a status column set to `planned`.
- Print a summary table: files per bucket, files per month, any `other` entries by name, any collisions, any files with no extension.
- You look at the summary. If a bucket looks wrong (say, `.md` should be `code-data` not `documents`), the table changes and the dry run reruns. No files have moved.

### Step 3: copy (not move)

- Create the destination folders from the mapping.
- Copy each file with its timestamps preserved (`Copy-Item` keeps content; a second pass sets `LastWriteTime` and `CreationTime` from the source so the folders and the metadata agree).
- After each copy, hash the destination file immediately and compare to the source hash. Mismatch marks the row `failed` and the run continues to the end so you see all failures at once, not one at a time.
- Update `MOVE-LOG.csv` row status to `copied` or `failed`.

### Step 4: build the destination manifest

- Walk the destination root recursively (excluding `_records`) and write `MANIFEST-destination.csv` in the same format as the source manifest.

### Step 5: the proof

All five checks must pass. Any failure stops the plan before step 6.

| # | Check | Pass condition |
|---|---|---|
| P1 | Count | destination file count = source file count = 200 |
| P2 | Bytes | total bytes identical |
| P3 | Hash set | sorted list of SHA-256 from source equals sorted list from destination, as a multiset (duplicates counted) |
| P4 | No extras | every destination file appears in `MOVE-LOG.csv`; nothing in the destination tree that was not planned |
| P5 | No failures | zero `failed` rows in `MOVE-LOG.csv` |

A short `PROOF.md` is written with the five lines, each PASS or FAIL with the two numbers compared, the run date, and the paths of the three CSV files. This is the thing you can read in a year without rerunning anything.

### Step 6: dispose of the originals (separate yes)

Only after `PROOF.md` shows five PASS lines, and only after you say yes on the day, the Q2 answer is carried out. If Q2 was option 1, the source files are deleted one by one, each only after a final hash re-check against the manifest (guards against the source being edited between step 1 and step 6). If a hash has changed, that file is not deleted and is reported.

### Step 7: final verification and hand-off

- Re-count the destination: still 200.
- Re-count the source: 0 files (or 200 if Q2 was option 2).
- Open `PROOF.md` and the move log one last time; the report to you is the five proof lines plus the per-bucket table, not a narrative.

## What would change this plan

- Source has subfolders: scope question before step 1.
- Source count is not 200: report the real number; the rest of the plan is unchanged except the target count.
- Files are on a cloud-synced drive (OneDrive, a cloud sync client): copy first then pause for sync to settle before step 4, and hash from the local copy only.
- Any file is open or locked: it is skipped with status `locked`, P5 fails, and you close it before a rerun.
- You want the type to come from content, not extension (a `.pdf` that is really a scanned receipt, say): that is a classification job, not a move job, and it belongs in a separate order.

## What this plan does not do

- It does not rename files beyond the ` (2)` collision suffix.
- It does not look inside files or sort by subject.
- It does not touch anything outside the two paths you give.
- It does not delete anything until the proof has passed and you have said yes a second time.

## Tooling

One PowerShell script, kept in the `_records` folder beside the manifests, with a `-WhatIf` switch for step 2 and a `-Delete` switch that is ignored unless `PROOF.md` exists with five PASS lines. Standard cmdlets only (`Get-ChildItem`, `Get-FileHash`, `Copy-Item`, `Export-Csv`); nothing to install.

## Your call

1. Approve as written (with Q1 = 1, Q2 = 1, and the two paths)
2. Approve with changes (name the bucket, date rule, or disposal change)
3. Revise (tell me what is missing or wrong)
4. Cancel
