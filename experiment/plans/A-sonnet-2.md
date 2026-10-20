# Plan: move 200 mixed files into a dated, typed layout, and prove nothing was lost

Date: 2026-10-08. Status: PLAN ONLY. Nothing has been read, moved, or changed. No folder named in this plan has been inspected.

## Conclusion

Copy first, verify by content hash, and only then remove the originals, in three gated stages. A move on the same drive would be quicker, but it leaves no second copy to check against until it is too late. Copy-then-verify costs one extra pass over 200 files and makes "nothing was lost" a measured result instead of a belief.

"Nothing lost" means four things, each checked separately in Stage 4:

1. Count: 200 files in, 200 files out, 200 rows in the manifest.
2. Content: every file's SHA-256 at the destination equals its SHA-256 at the source.
3. Coverage: no source file is unmapped, and no destination file is unexplained.
4. Reversibility: the manifest alone can put every file back where it was.

## What this plan does not know yet

I have not seen the source folder, so these are unknown until Stage 0: the actual file count (the 200 is your number, not a measurement), whether there are subfolders, which file types are present, whether dates are trustworthy, and whether the folder sits inside a blocked area. The layout below is a default. Stage 0 can change it.

## Decisions I need from you (answer once, before Stage 1)

**D1. How are files sorted into folders?**
1. Type, then year, then month: `Type\2026\2026-03\file` (recommended)
2. Year-month first, then type: `2026-03\Type\file`
3. Type only, with the date in the filename

**D2. Which date counts as "the" date?**
1. Last-modified time (recommended: every file has one, and a copy that preserves it does not change it)
2. Created time
3. Date embedded in the file (photo capture date, document properties), falling back to modified time. More accurate, but slower and less predictable.

**D3. What are the types?** Default (recommended): Documents (doc, docx, pdf, txt, md, rtf), Spreadsheets (xls, xlsx, csv), Presentations (ppt, pptx, key), Images (jpg, png, gif, heic, svg), Audio, Video, Archives (zip, 7z), Other. Stage 0 replaces this with the real extension list and shows you the proposed mapping before anything is copied.
1. Use the default and add types only for extensions found in Stage 0 (recommended)
2. Use a type per extension (`pdf\`, `docx\`, ...)
3. You supply the type list

**D4. Where does the new layout live?**
1. A new sibling folder beside the source, never inside it (recommended)
2. Inside the source folder
3. A path you name

**D5. When may the originals be removed?**
1. After Stage 4 passes and you approve separately, in a fresh message (recommended)
2. Never. Leave the originals in place and you delete them yourself.
3. Automatically after verification passes

## Before anything: boundary check

The source and destination must not be, or sit inside, [walled], [walled], or [walled], in any casing. If the source path is one of those, or Stage 0 shows one in its filenames or location, the work stops and I report that. I will not list, hash, or summarize it. I will also not enumerate the root of `<root>`. I navigate only to the exact source path you give me.

## Stages

### Stage 0. Read-only discovery (no approval needed; changes nothing)

- Confirm the exact source path with you if it is not already unambiguous.
- Count files, recursively, and separately note subfolders, hidden files, zero-byte files, and files with no extension. Compare to 200. If the count is not 200, stop and report the difference before going further.
- List extensions with counts, to ground D3.
- Find hazards: filenames that differ only by case, paths longer than 240 characters, files in use or locked, read-only files, shortcuts or links, and identical content under different names.
- Check free space at the destination. It must be at least the source size plus 10%.
- Output: a short discovery report. Nothing is written except a manifest draft in the scratch area, outside both folders.

### Stage 1. Manifest (the "before" picture)

For every source file, one row: source path, name, extension, size in bytes, modified time, created time, SHA-256, assigned type, assigned date, proposed destination path.

- Save it as CSV plus a plain-text copy of the SHA-256 list, in a `_migration-log` folder created next to the new layout, not inside it.
- Check the manifest before any copy: 200 rows, 200 unique source paths, 200 unique destination paths. If two files map to one destination path, resolve with a suffix of the first 8 characters of the file's hash (`report__a1b2c3d4.pdf`). Never overwrite, never rename silently. Every rename is recorded in the manifest.
- Identical files (same hash) are both kept. No deduplication in this job: it would break the 200-in, 200-out count.
- Dry run: print the full source-to-destination mapping and show you a sample of 20 rows plus every row that has a collision, an unusual type, or a missing date. **Gate: your approval of the mapping.**

### Stage 2. Copy (originals untouched)

- Copy each file to its destination, preserving modified time. Create folders as needed.
- Copy only; use no move command. Refuse to overwrite: if a destination already exists, stop and report.
- Log each copy as it happens (row id, result, time). If a copy fails, record the failure and continue, so you see all failures together, not just the first.
- Drift check after copy: confirm the source folder still has 200 files with the same hashes as the manifest. If anything in the source changed during the copy, stop and report.

### Stage 3. Verify (the "after" picture)

Done by a separate, fresh pass that does not reuse the copy step's results:

1. Re-hash every destination file. Compare to the manifest's source hash: 200 of 200 must match.
2. Count destination files: exactly 200, and no extras or empty folders left over from mistakes.
3. Reverse check: every file found at the destination appears in the manifest. The sets match in both directions.
4. Size and modified-time match for each row (a supporting check; the hash is the real proof).
5. Re-hash the source files once more. Originals must still match the manifest, so a bad copy is never confused with a changed original.
6. Spot-open 10 files across types (at least one of each type) to confirm they are readable, since a hash proves identical bytes but not that the file was good to begin with.

Pass condition: all six checks clean. If any check fails, nothing is removed. I report the exact rows, fix only those, and re-run Stage 3 in full.

### Stage 4. Proof report

A one-page control report, conclusion first:

- Verdict: PASS or FAIL.
- The reconciliation table: source count, manifest rows, destination count, hash matches, mismatches, missing, extra, renamed-for-collision (each with the number and, if not zero, the rows).
- Counts per type and per year, which must sum to 200.
- Evidence: location of the manifest, the hash lists, the copy log, and the verification log.
- What would change the verdict: any non-zero in mismatches, missing, or extra; a source count other than 200; a changed original.

### Stage 5. Remove originals (only if D5 = option 1; separate approval)

- Re-run the Stage 3 hash comparison immediately before deleting, because the world may have changed since.
- Send originals to the Recycle Bin, not permanent deletion, and keep the manifest. Permanent deletion is yours to do.
- Final check: source folder is empty (or holds only what the manifest says it should), destination still holds 200 verified files.
- Rollback: the manifest maps every destination path back to its source path, so a restore script can be generated from it. Keep the manifest and the Recycle Bin contents until you say you are satisfied.

## Risks and how each is handled

| Risk | Handling |
|---|---|
| Wrong count (not 200) | Stage 0 stops and reports before any copy |
| Name collisions overwrite a file | Collision suffix from hash; destination existence is a hard stop |
| Same-name files differing only by case (Windows) | Found in Stage 0; resolved by the collision rule |
| Dates wrong or missing | Fallback to modified time, flagged in the manifest and shown at the dry-run gate |
| A file changes during the job | Source re-hashed after Stage 2 and again before Stage 5 |
| Partial or interrupted copy | Hash check catches it; copy log shows where it stopped; re-run only the failed rows |
| Files locked or unreadable | Logged as failures, reported together, never skipped silently |
| Disk fills up | Space check in Stage 0 |
| Verification code has the same bug as the copy code | Stage 3 is a fresh pass with an independent hash, plus the reverse check and a manual spot-open |
| Blocked folder involved | Boundary check; stop and report |

## What I will not do without a new approval

Change the layout after the Stage 1 gate, deduplicate, rename for tidiness, convert file formats, delete anything permanently, or touch any folder other than the source and the new layout. The `_migration-log` is a verification artifact for this job only. It is not a tracker or a register of your action items.

## Effort

Stages 0 to 4 are scripted and take minutes for 200 files; the real time is your review at the two gates (the Stage 1 mapping and the Stage 5 removal).

## Choose

Reply with answers to D1 to D5, or accept the recommended defaults (D1=1, D2=1, D3=1, D4=1, D5=1), then:

1. approve as written
2. approve with changes
3. revise
4. cancel
