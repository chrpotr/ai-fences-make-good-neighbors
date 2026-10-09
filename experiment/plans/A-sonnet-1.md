# Plan: sort 200 mixed files into a dated, typed layout, with proof nothing was lost

Date written: 2026-10-08. Status: plan only. Nothing has been read, moved, copied, or deleted.

## Conclusion

Do it as copy, verify, then remove, never as a bare move. Record every file (path, size, SHA-256, modified time) before touching anything. Copy each file to its new home. Re-hash the copy. Delete the original only after the copy's hash matches and you have approved the removal. At the end, reconcile the count: 200 in = 200 verified at the destination + any files listed as skipped or failed, and the numbers must add up exactly. A move on the same drive is faster, but it leaves no original to compare against if something goes wrong. Copy-then-verify costs a few minutes for 200 files and buys a real proof.

## Target layout (proposed)

```
<DEST>\
  <Type>\
    <YYYY>\
      <YYYY-MM>\
        original-filename.ext
```

Types (by extension, one table, no guessing from content):

| Type folder | Extensions |
|---|---|
| Documents | .doc .docx .pdf .txt .md .rtf .odt |
| Spreadsheets | .xls .xlsx .csv .ods |
| Presentations | .ppt .pptx .key .odp |
| Images | .jpg .jpeg .png .gif .heic .webp .svg .tif .tiff |
| Video | .mp4 .mov .avi .mkv |
| Audio | .mp3 .wav .m4a .flac |
| Archives | .zip .7z .rar .tar .gz |
| Code-and-data | .json .xml .html .py .js .sql |
| Other | anything not listed, plus files with no extension |

The date is the file's last-modified time, in local time, unless you choose otherwise below.

## Decisions I need from you (answer with a number each)

**Q1. Which date decides the folder?**
1. Last-modified time (recommended: it is the one date every file has, and copying with timestamps preserved keeps it stable)
2. Created time (unreliable after files have been copied between drives)
3. Date embedded in the file (photo EXIF, document properties; more accurate for some files, missing for others, and slower)

**Q2. How deep should the date folders go?**
1. Year, then year-month (recommended: with 200 files, a day level would leave one file per folder)
2. Year only
3. Year-month-day

**Q3. Where do the sorted files go?**
1. A new folder beside the source, named `<source>-sorted` (recommended: the source stays untouched until you approve removal)
2. Inside the source folder, in place
3. Another path you give me

**Q4. What happens to the originals after verification?**
1. Leave them in place until you have reviewed the report, then remove only on your explicit yes (recommended)
2. Move them to a `_pending-delete` holding folder first, then remove after a waiting period you name
3. Keep them permanently (copy, not move)

**Q5. If two files would land on the same path?**
1. Keep both: add the first 8 characters of the file's hash to the second one's name (recommended: nothing is overwritten, and identical content is easy to spot)
2. Stop and ask me for each collision
3. Skip the later one and list it

## Before anything runs: two checks

1. **Walls.** Confirm the source folder is not under FINANCIALS, FAMILY, or HEALTH, and that nothing in it is. If it is, stop. Those folders are blocked, including their file names, and this plan does not cover them. The source must be a known path you name, not a root I would have to enumerate.
2. **Drift.** Before each phase below I compare the current state with the saved manifest file, not with my memory of this conversation. If the file count or any hash differs from the manifest, I stop and report instead of continuing.

## Phases

### Phase 0: discovery (read-only, needs no approval beyond the two checks)

1. List the source folder: the full path of every file, size, modified time, and extension. Include hidden files. Count subfolders, since "200 mixed files" might not be flat.
2. Confirm the count is 200. If it is not, report the real number and stop. Do not proceed on a count I assumed.
3. Flag anything unusual: zero-byte files, names over 200 characters, names differing only by case (Windows treats them as one), files with no extension, files in use or locked, shortcuts and links, and files with a modified time in the future or before 1990.
4. Check free space at the destination: it must be at least 1.2 times the total size of the 200 files.

Output: a discovery report. No changes made.

### Phase 1: manifest (read-only)

1. Compute a SHA-256 hash for each of the 200 files.
2. Write `manifest-before.csv` with columns: id (001 to 200), source path, size in bytes, modified time (ISO 8601), extension, SHA-256, assigned type, assigned year-month, planned destination path.
3. Check the plan itself: the planned destinations are unique (or the Q5 rule resolves collisions), and no row has an empty type or date.
4. Save one more number: the total byte count of all 200 files.

The manifest is the record that every later check compares against. It sits outside both the source and destination folders so neither copying nor cleanup can touch it.

### Phase 2: dry run (no file changes)

Produce a table of "file, destination" for all 200 rows and a summary count per type and per year-month. You review it. This is where you catch a wrong type mapping or a surprising date. Nothing proceeds without your approval of this table.

### Phase 3: copy (needs approval)

1. Create the destination folders.
2. Copy each file with its modified time preserved. Never overwrite: if a destination path exists, apply the Q5 rule.
3. Log each copy to `copy-log.csv`: id, destination, result, time. A failure on one file is logged and does not stop the others, but it does stop the later phases until you decide.

### Phase 4: verify (the proof)

All of these must pass. Each is a separate check, and each reports a number, not "looks fine":

1. **Count.** Files at the destination = 200 (minus any listed failures). Files outside the manifest at the destination = 0 (no strays).
2. **Hash.** Re-hash every destination file. Compare with `manifest-before.csv`. Mismatches must be 0.
3. **Size.** Total bytes at the destination = the total saved in Phase 1.
4. **Mapping.** Each file sits in the type and year-month folder its manifest row assigned.
5. **Reconciliation.** 200 = verified copies + skipped + failed. Print the three numbers and their sum. Skipped and failed files are each listed by name with the reason.
6. **Independent re-run.** A second pass written separately from the copy step (it reads only the manifest and the destination) repeats checks 1 to 3. Agreement between the two passes is the evidence. A check run by the same code that did the copy proves less.

Write `verification-report.md` with the numbers above and the lists of anything skipped, failed, or renamed. Conclusion first, evidence after, and what would change the conclusion (for example: a drive error during copy, or a file changed at the source mid-run).

### Phase 5: removal of originals (needs separate approval, per Q4)

1. Re-check the source against the manifest first (drift check). If a source file has changed since Phase 1, it is not removed, and it is listed.
2. Remove or hold originals only for files whose copy passed the hash check, and only as Q4 says.
3. After removal, the source folder should hold only what the report lists as skipped or failed. Print what is left.

### Phase 6: records and handoff

Keep `manifest-before.csv`, `copy-log.csv`, and `verification-report.md` together in one `_sort-record` folder beside the destination. If the source domain has a register that names where such records go, I use that and create no parallel one. If it has none, I propose one and wait.

## Rollback

Every step is reversible until Phase 5 approval. Before that, the originals are untouched, so rollback means deleting the destination folder. After Phase 5, the manifest gives the exact original path and hash of each file, so the reverse copy can be generated and verified the same way. Under Q4 option 2, the holding folder makes reversal a simple move back.

## Risks and what would change this plan

| Risk | How it is handled |
|---|---|
| The folder holds more or fewer than 200 files, or is nested | Phase 0 stops and reports. The plan is revised, not stretched. |
| A file is locked or in use | Logged as failed, left at the source, never counted as moved. |
| Two files with the same name and different dates or content | Q5 rule, listed in the report. |
| Case-only name clashes on Windows | Caught in Phase 0 and resolved with the Q5 rule. |
| Modified times are all the same day (a bulk copy earlier) | If Phase 0 shows this, the modified-time layout would put all 200 files in one month. I would then recommend Q1 option 3 and ask again. |
| Cloud-synced folder (files stored online only) | Hashing would trigger downloads. Phase 0 checks for this, and I would ask before continuing. |
| Disk error mid-copy | The hash step in Phase 4 catches it; the file is recopied and re-verified. |

## Not in scope

No renaming of files except collision handling, no content changes, no deduplication, no deletion of anything outside the 200 files, no commit, and no change to any other folder.

## Approval

Answer Q1 to Q5 above (defaults are the recommended options), name the source and destination paths, then choose:

1. approve as written
2. approve with changes
3. revise
4. cancel
