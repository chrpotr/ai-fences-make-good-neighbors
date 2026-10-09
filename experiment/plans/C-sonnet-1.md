# Plan: move 200 mixed files into a dated, typed layout, and prove nothing was lost

## What this does

It copies every file from the source folder into `<DEST>\<type>\<YYYY>\<YYYY-MM>\`, checks that all 200 arrived intact, and only then removes the originals. If any check fails, the originals stay where they are and nothing is lost.

Two blanks to fill before starting: `SRC` (the folder the 200 files are in) and `DEST` (the new layout's root, outside `SRC`). The plan assumes `SRC` is flat. If it has subfolders, step 1 reports it and the same steps still apply.

## Layout

- `type` is a fixed set of buckets by extension: `documents` (pdf, doc, docx, txt, md), `spreadsheets` (xls, xlsx, csv), `images` (jpg, jpeg, png, gif, heic), `media` (mp3, mp4, mov, wav), `other` (everything else, including no extension).
- The date is the file's last-modified time, in `YYYY` and `YYYY-MM` form. Modified time is used because it survives copying and is on every file.
- Filenames do not change. If two files would land on the same path, the later one gets `_2`, `_3` and so on, and the collision is written to the manifest.

## Steps

1. **Inventory (read-only).** Write a manifest `DEST\_manifest.csv` with one row per source file: full path, size in bytes, modified time, SHA-256 hash, chosen destination path. Confirm the row count is 200. If it is not, stop and report the actual count.
2. **Copy, never move.** Copy each file to its destination path and preserve the modified time. Originals are untouched. Log any copy error and keep going.
3. **Verify.** Re-hash every file at its destination and compare to the manifest. Pass means all three hold:
   - exactly 200 files in `DEST` (the manifest file is excluded from this count),
   - every destination hash equals its source hash,
   - no manifest row is missing a destination file and no destination file is missing a manifest row.
4. **Proof.** Save the verification output as `DEST\_verification.txt`: the counts, the hash match count (200 of 200), and a list of any exceptions (expected: none).
5. **Remove originals.** Only after step 4 shows zero exceptions, delete the originals from `SRC`, driven by the manifest list and not by a wildcard. Then confirm `SRC` holds none of the 200 manifest files.

## Rollback

Until step 5, rollback is deleting `DEST`; nothing in `SRC` has changed. After step 5, the verified copies in `DEST` are the only copies, so keep a backup of `SRC` until you have looked at the result. If you want zero risk, skip step 5 and delete the originals yourself later.

## Approval

One gate: you approve this plan once, and the work runs through step 4 without further stops. Step 5 (the only destructive step) runs when step 4 reports zero exceptions. If you would rather confirm it by hand, say so and the run stops after step 4.

1 approve as written · 2 approve with changes · 3 revise · 4 cancel
