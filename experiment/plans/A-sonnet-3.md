# Plan: move 200 mixed files into a dated, typed layout, with proof nothing was lost

Date: 2026-10-08. Status: plan only. Nothing has been read, moved, copied, or changed.

## Conclusion

Copy, do not move. Build the new layout as a copy of the 200 files, prove the copy is complete by comparing a fingerprint of every file before and after, and leave the original folder untouched until you say to retire it. Nothing can be lost because nothing is deleted. The proof is a set of hashes taken before any change and compared after, not a file count alone.

## What I am assuming (and what would change it)

- Source: one folder you will name, containing exactly 200 files, with no walled folders ([walled], [walled], [walled]) inside or above it. If the folder is walled, I stop and tell you.
- Same drive for source and destination. If not, copy-then-verify still works unchanged.
- "Dated" means the file's last-modified date, because creation dates reset when files are copied between drives.
- "Typed" means a category derived from the file extension.
- If the count is not 200 when I first measure it, I stop and report. I do not proceed on a different number.

## The one question I need answered

Layout for the destination (recommended: 1):

1. `Destination\YYYY\YYYY-MM\Type\filename` (date first, then type). Recommended: it sorts chronologically and keeps each month's types together.
2. `Destination\Type\YYYY\YYYY-MM\filename` (type first, then date).
3. Something else you describe.

Everything below uses option 1. Option 2 only swaps the folder order in the mapping step.

Default type categories (extension to folder), unless you change them: Documents (doc, docx, pdf, txt, md, rtf), Spreadsheets (xls, xlsx, csv), Presentations (ppt, pptx, key), Images (jpg, jpeg, png, gif, heic, svg, webp), Video (mp4, mov, avi, mkv), Audio (mp3, wav, m4a), Archives (zip, 7z, rar), Data and Code (json, xml, py, js, html), Other (anything unlisted or no extension). Nothing is dropped: an unknown extension goes to Other and is listed in the report.

## Phases

### Phase 0: Discover (read-only, no approval needed)

- List the source folder only: name, size, last-modified, extension. No file contents are opened.
- Confirm the count is 200, the folder is not walled, and whether it has subfolders, hidden files, shortcuts, or zero-byte files.
- Check free space on the destination drive is at least 1.2 times the source size.
- Output: a short discovery note with the real count, total size, and the extensions found.

### Phase 1: Baseline manifest (the proof starts here)

- For every file, record: full source path, size in bytes, last-modified timestamp, extension, and SHA-256 hash.
- Save as `manifest-before.csv` in a work folder outside the source and destination.
- Record the SHA-256 of the manifest file itself, so it cannot be quietly edited later.
- Gate: manifest has exactly 200 rows. If not, stop.

### Phase 2: Dry run of the mapping (still no file changes)

- Compute each file's destination path from its last-modified date and its type.
- Save `mapping.csv`: source path, destination path, hash.
- Checks before anything runs:
  - 200 rows in, 200 distinct destination paths out (no two files land on the same path).
  - Name collisions: where two files would share a destination name, the second gets a suffix `-2`, `-3`, and both appear in the mapping. If two files share a name and a hash, they are true duplicates; both are still kept, and I flag them to you. I never merge or drop duplicates on my own.
  - Windows is case-insensitive: compare destination paths with case ignored.
  - Any destination path over 240 characters is flagged.
  - Any file with an unreadable date goes to `Destination\undated\Type\` and is listed.
- Summary table for you: files per year-month and per type, plus the count of collisions, undated files, and Other.

### Gate: your approval

You review the mapping summary before any file is touched. Silence is not approval.

### Phase 3: Execute (copy only)

- Create the destination tree.
- Copy each file to its mapped path, preserving the last-modified timestamp. The source folder is read-only in practice: no writes, renames, or deletes there.
- Log each copy (source, destination, time, result) to `copy-log.csv`. Copy in a single pass; if any copy errors, record it and continue, then report all errors at the end.
- Do not retry silently. A failed copy is a finding.

### Phase 4: Verify (prove nothing was lost)

Run all of these against the disk, not against the log. All must pass.

1. Count: destination contains exactly 200 files, and the source still contains exactly 200.
2. Hash match: compute SHA-256 of every destination file into `manifest-after.csv`. For every row in `manifest-before.csv`, the mapped destination file exists and its hash and size are equal. Zero mismatches.
3. Set equality both ways: the set of hashes before equals the set of hashes after. No missing, no extras. Duplicates are compared as counts (the same hash appearing twice before must appear twice after).
4. No stray files: nothing in the destination tree that is not in the mapping (no temp files, no leftovers).
5. Source unchanged: re-hash the source and compare to the baseline, to show the copy did not alter it.
6. Layout check: every destination file sits in the right year-month folder for its timestamp and the right type folder for its extension (recomputed independently from the destination file's own timestamp and extension).
7. Spot check: open 5 files of different types (chosen by random draw, seed recorded) to confirm they are readable. This supports, but does not replace, the hash proof.

Pass criterion: every check passes, with 0 missing, 0 mismatched, 0 extra. Any failure means I stop, report it, and do not proceed to retirement.

### Phase 5: Report

A control report, not a narrative: conclusion first (pass or fail), then the numbers (200 in, 200 out, 0 mismatches, collisions renamed, undated, errors), then the evidence file names and the SHA-256 of the manifests, then what would change the conclusion. All evidence files are kept in the work folder.

### Phase 6: Retire the original (separate decision, yours)

I do not delete the source folder. After you read the report, you choose what happens to it (see the closing options). If you want it retired, the safest route is to rename it with an `-ARCHIVE-2026-10-08` suffix and keep it for a period you set, rather than delete it. Deleting is something you do yourself.

## Rollback

Because the source is never modified, rollback is: delete the new destination tree (you do this) and nothing else is affected. No state needs reversing.

## What could go wrong, and the guard

- Count is not 200: caught in Phase 0 and Phase 1; stop.
- Two files overwrite each other: caught by the distinct-destination check in Phase 2.
- A file is changed or corrupted in copy: caught by hash comparison in Phase 4.
- A file is locked or unreadable: logged as an error, reported, never skipped silently.
- The date is wrong because the modified date is misleading: the layout reflects last-modified by design; undated and odd cases are listed for your review.
- Something else is writing into the source folder during the run: caught by the Phase 4 source re-hash and count.

## What this plan does not do

It does not rename files beyond collision suffixes, open or summarize contents, merge duplicates, touch any other folder, or create any tracker or register. This is a one-off task, so no register entry is proposed unless you want one.

## Decision

1. Approve as written (layout option 1, last-modified date, default type categories, copy only).
2. Approve with changes (tell me which: layout option, date source, categories).
3. Revise.
4. Cancel.

Recommended: 1. To start, I also need the source folder path and the destination path.
