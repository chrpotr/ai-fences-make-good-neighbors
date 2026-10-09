# Plan: move 200 mixed files into a dated, typed layout and prove nothing was lost

**Conclusion.** Fingerprint every file, move them, fingerprint them again, and compare the two lists. If all 200 fingerprints are present after the move, nothing was lost. You approve once, before anything moves. After that the plan runs to the end unless the check fails.

## The layout

```
<DEST>\<type>\<YYYY-MM>\<original file name>
```

- **Type** comes from the file extension. Seven folders: `documents`, `spreadsheets`, `slides`, `images`, `video`, `audio`, `other`. Any extension that is not on the map goes to `other`, so no file is left without a folder.
- **Date** is the file's last-modified date. Every file has one, and reading dates from inside files (photo EXIF, PDF properties) would add a rule for each format.

## Steps

1. **Fingerprint (read-only).** List every file in `<SOURCE>` with its full path, size, and SHA-256 hash. Save the list as `before.csv`, outside both folders.
2. **Dry run (read-only).** Work out each file's new path and save it as `moves.csv` (old path, new path). Count the files per folder and count the name clashes. This step shows the result. It is not a second approval.
3. **Move.** Move each file to its new path. Do not overwrite: if a name is already taken, add ` (2)` before the extension. Add each move to `moves.csv` as it happens.
4. **Prove.** Fingerprint `<DEST>` into `after.csv`. Pass means all three of these are true:
   - `after.csv` has 200 rows, the same count as `before.csv`
   - every hash in `before.csv` appears in `after.csv` the same number of times
   - `<SOURCE>` holds no files
5. **Report.** Give the pass or fail result, the count per folder, and any clashes that were renamed. Keep the three CSV files.

## The rules, and why each one is needed

| Rule | Why |
|---|---|
| Never overwrite a file | Overwriting is the only way a move can destroy a file. |
| Touch only `<SOURCE>`, `<DEST>`, and the three CSV files | Keeps the work inside the job. |
| Stop if any check in step 4 fails | The fingerprints say which file is missing. `moves.csv` shows where it went, and every move can be reversed from it. |

That is the whole rule set. There is no per-file approval and no second gate, and nothing is deleted. Moving a file is not a delete, and the source folder itself stays.

## What you need to supply

- `<SOURCE>`: the folder that holds the 200 files.
- `<DEST>`: where the new layout goes. **Default:** a new folder beside `<SOURCE>`.

## What would change this plan

- If the files are spread across more than one drive, the move becomes a copy and then a delete. The delete happens only after step 4 passes.
- If "dated" should mean the date a photo was taken or a document was written, rather than the last-modified date, add one rule for each format that carries that date.

**Approve?**
1 approve as written · 2 approve with changes · 3 revise · 4 cancel
