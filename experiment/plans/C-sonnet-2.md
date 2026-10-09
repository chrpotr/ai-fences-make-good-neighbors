# Plan: move 200 mixed files into a dated, typed layout, and prove nothing was lost

## Conclusion

Copy all 200 files into the new layout, compare a before-and-after list of fingerprints, and delete the originals only if the lists match. One approval starts it. There is no other gate. Nothing is touched until you approve.

## The layout

`<destination>\YYYY-MM\<type>\<original filename>`

- Date is the file's last-modified date. It is one number per file and it is already on disk.
- Type is the file extension, grouped into: documents, images, spreadsheets, audio-video, archives, other. Anything unrecognized goes to `other`, so no file is ever left behind.
- If two files would land on the same name, the second gets `-2` before the extension. Nothing is overwritten.

## Steps

1. **List.** Record every file in the source folder: full path, size in bytes, last-modified date, and SHA-256 hash. Save this as `before.csv`. Stop and report if the count is not 200.
2. **Copy.** Copy each file to its new location. The originals stay where they are. Preserve modified dates.
3. **List again.** Record the same four fields for every file in the destination. Save as `after.csv`.
4. **Prove.** Pass only if all three hold:
   - `after.csv` has exactly 200 rows.
   - The sorted list of hashes in `after.csv` is identical to the sorted list in `before.csv`.
   - No file is in the destination outside a `YYYY-MM\<type>` folder.
5. **Remove originals.** Only after step 4 passes, delete the 200 source files. If step 4 fails, delete nothing and report the mismatched rows.
6. **Hand off.** Give you the two CSVs and one line: "200 in, 200 out, hashes match, originals removed" or the failure.

## Why only this much

- Copying first means the move can fail at any point and you still have every original. That is the whole safety net, so there is no separate backup step and no extra approval before deleting.
- Comparing hashes proves content survived, not just that filenames exist. A count alone could pass with a corrupted or duplicated file.
- Duplicates in the source (same content, different name) are fine: the hash list is compared as a whole, so two identical files must appear twice on both sides.

## What would change this

- If source and destination are on the same drive, a plain move is faster, but it removes the original-as-safety-net. I recommend copying anyway at 200 files.
- If any file is open or locked, it will fail to copy. The run stops and reports it rather than skipping it.
- If you want the date from the filename or from photo metadata instead of last-modified, say so before approving, because it changes where files land.

## Needed from you

The source folder path and the destination path. I will not guess either.

## Decision

1 approve as written (recommended) · 2 approve with changes · 3 revise · 4 cancel
