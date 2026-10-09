# Plan: move 200 mixed files into a dated, typed layout, with proof nothing was lost

Plan date: 2026-10-08. Status: proposed, not approved. Nothing has been run.

## What this is and why

You have one folder holding about 200 files of mixed types. You want them sorted into folders by date and by type. You also want proof that every file arrived whole and nothing went missing.

The approach: **copy first, check, and only then retire the originals.** Before anything changes, the run writes down every file with its size and its fingerprint (a SHA-256 hash). After the copy, it fingerprints the copies again and compares them line by line. The originals are not touched until that comparison shows 200 out of 200 matched. Then it checks once more after a cloud sync client finishes syncing. Nothing is permanently deleted by an agent at any point.

## Inputs I need from you

- **Source folder:** the full path of the folder with the 200 files.
- **Destination folder:** the full path where the new layout should go. It can be empty or new.

Three choices, each with a recommended default:

**Q1. Folder order**
- A. `<destination>\<YYYY>\<YYYY-MM>\<type>\` (date first, then type) **(recommended: you usually look for things by when they happened)**
- B. `<destination>\<type>\<YYYY>\<YYYY-MM>\` (type first, then date)
- C. `<destination>\<YYYY-MM>_<type>\` (one flat level)

**Q2. Which date decides the folder**
- A. Use the date in the file itself where there is one (photo capture date, or a YYYY-MM-DD in the filename). Otherwise use the last-modified date. The manifest records which rule set each file's date. **(recommended)**
- B. Last-modified date for every file
- C. Filename date only. Files with no date in the name go to `_undated\`

**Q3. What happens to the originals once the proof passes**
- A. They are moved to a holding folder beside the source, `_originals-<run date>\`, and you delete it yourself when you are satisfied. **(recommended)**
- B. They are left exactly where they are
- C. They are sent to the Recycle Bin (recoverable, but no longer in place)

## Phases

### Phase 0. Read-only discovery (needs no approval; changes nothing)

1. **Wall check.** If the source or destination path sits inside a FINANCIALS, FAMILY or HEALTH tree, in any casing, stop and do not list it. While listing the source, if any filename matches one of those words, stop without opening or hashing that file. Report only how many files matched, never their names, and wait for your ruling.
2. **Inventory.** Count the files. Note any subfolders, hidden or system files (`desktop.ini`, `Thumbs.db`), zero-byte files, files with no extension, and full paths longer than 260 characters. If the count is not 200, report the real number and use it from here on.
3. **a cloud sync client placeholders.** Confirm each file is fully on disk and not an online-only placeholder. Hashing a placeholder forces a download, and a failed download looks like a lost file.
4. **Space.** Confirm the destination drive has at least 2 times the source's total size free. During the run, the copies and the originals exist side by side.
5. **Quiet check.** Take the file count and the newest modified time twice, a few minutes apart. If either changes, something else is writing to the folder, so stop and ask. Before any write, also check that the destination path does not already hold files with the same names. Use targeted checks on these two paths only, never a broad listing of sessions or drives.
6. **Where the record goes.** Find the plan record or register that the domain owning the source folder designates. If it has none, propose one and wait. No new tracker gets created on the side.

### Phase 1. Dry run (writes only into a run folder; touches no user file)

The run folder is `<destination>\_move-run-<YYYY-MM-DD>\`, or a location you name. It holds the script, the manifests and the report, apart from both the source and the new layout.

1. **Before-manifest** (`manifest-before.csv`): one row per file. Columns: source path, size in bytes, created time, modified time, SHA-256, file type, date used, date rule used (Q2), planned destination path.
2. **Type map.** Extension to type folder: `images`, `video`, `audio`, `documents` (doc, docx, odt, rtf), `pdf`, `spreadsheets` (xls, xlsx, csv), `slides` (ppt, pptx, key), `text` (txt, md), `archives` (zip, 7z, rar), `code`, `other`. Every file gets a row. An unknown extension goes to `other`, never nowhere. The map is saved as a file in the run folder, so you can see exactly why each file landed where it did.
3. **Collisions.** If two files would land at the same destination path, the second one gets ` (2)` added to its name, and the manifest records the rename. If two files have the same hash (exact duplicates), both are kept and flagged in the report. Nothing is merged or dropped silently.
4. **Dry-run summary for you:** the count per type, the count per month, the count in `other`, the undated count, collisions renamed, duplicates flagged, and anything skipped with the reason. That is one screen, not 200 rows.

**Gate 1:** you review the summary and approve the copy. Nothing in Phase 2 runs without that approval.

### Phase 2. Copy (the destination changes; the source does not)

1. Before each copy, re-hash the source file and compare it with the before-manifest. If the file changed since the manifest was written, skip it, log it, and stop at the end of the batch.
2. Copy the file to its planned path. Never overwrite: if the target already exists, stop.
3. Set the copy's created and modified times from the manifest, so the dates survive the move.
4. Log every action to `copy-log.csv`: time, source, destination, result.

Stop conditions: a locked file, an access error, a path that is too long, a sync-conflict file appearing, or any skip. On a stop, nothing is undone automatically. You get a report of what was copied and what was not.

### Phase 3. Proof (read-only)

A separate verification pass reads the destination fresh. It does not trust the copy log.

1. **After-manifest** (`manifest-after.csv`): every file under the new layout, excluding the run folder, with size, times and SHA-256.
2. **Reconcile** the before-manifest against the after-manifest:
   - Count: source 200 = destination 200
   - Every source hash is found at exactly its planned destination path: 200 of 200
   - Missing (in the source, not at the destination): 0
   - Extra (at the destination, not from the source): 0
   - Changed (same path, different hash or size): 0
   - Total bytes: equal
   - Modified times: equal to the manifest
3. **Proof report** (`proof-<YYYY-MM-DD>.md`): the numbers above, the dry-run counts, every exception with its reason, and the paths of both manifests, so anyone can re-run the comparison.

**Pass** means every line above is exact. Anything less is a fail, the originals stay where they are, and you get the exceptions list.

### Phase 4. Retire the originals (only after a pass, as chosen in Q3)

1. Carry out your Q3 choice. For A, this is a same-drive move into `_originals-<date>\`, which rewrites no data. Hash a sample of 10 originals in the holding folder against the manifest to confirm the move.
2. No agent empties the Recycle Bin or permanently deletes anything. That step stays yours.

### Phase 5. Re-verify after sync

When a cloud sync client shows the folder fully synced, run Phase 3 again on the destination. The proof only counts as final when it passes a second time after sync. If anything differs, stop, and keep the originals in holding.

### Phase 6. Records and handoff

1. Add one entry to the plan record designated in Phase 0. It opens with a plain-English line on what moved, where and why, then links the proof report and both manifests.
2. Before writing it, drift check: compare what ran against this plan file, not against memory, and list any differences.
3. Hand off: the proof report and the record entry, plus a note on where the originals are and that deleting them is your step.

## Rollback

The before-manifest maps every original path to its new path. Until the originals are deleted, rollback is a simple reverse: remove the copies, or move the originals back from holding using the same manifest, then re-run the reconciliation in the other direction.

## What would change this plan

- The source has subfolders. They would be flattened into the layout, and each file's original subfolder would be kept in the manifest. A rule that keeps them as subfolders would need your call.
- Many files are online-only in a cloud sync client. Phase 0 would add a download-and-confirm step first.
- Any file hits a wall word. Everything stops at Phase 0 until you rule on it.
- Fewer or more than 200 files. The plan runs unchanged against the real count.

---

1 approve as written · 2 approve with changes · 3 revise · 4 cancel
