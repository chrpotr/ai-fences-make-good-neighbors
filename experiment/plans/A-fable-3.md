# Plan: move 200 mixed files into a dated, typed layout, with proof nothing was lost

Written 2026-10-08. Plan only. Nothing has been read, touched, or run.

## What this does and why

One folder holds about 200 files of mixed kinds. The plan sorts them into
folders by type and by month, so a file can be found by "what is it" and
"when is it from" without opening anything. The move is done as copy, verify,
then delete, never as a bare move, so at every point there is a complete copy
of every file somewhere and a written record proving it.

The proof is a manifest: before anything moves, every file's path, size, and
SHA-256 hash are recorded. After the copy, every destination file is hashed
again and matched to its source. Only when every row matches is the source
removed. The two manifests and a comparison report are the evidence.

## The layout

```
<destination root>\
  <type>\
    <YYYY-MM>\
      <original filename>
```

Example: `documents\2026-03\quarterly-notes.docx`.

Type is the outer level because the question "where are my spreadsheets" is
asked more often than "what happened in March", and because a month folder
under each type stays small enough to read at a glance. If you prefer month
outermost, that is a one-line change in the mapping step and nothing else in
the plan moves.

### Type buckets, by extension

| Bucket | Extensions |
|---|---|
| documents | doc docx odt rtf txt md pages |
| spreadsheets | xls xlsx csv tsv numbers ods |
| presentations | ppt pptx key odp |
| pdf | pdf |
| images | jpg jpeg png gif heic webp tif tiff bmp svg |
| audio | mp3 m4a wav aac flac ogg |
| video | mp4 mov m4v avi mkv webm |
| archives | zip rar 7z tar gz |
| code-and-data | json xml yaml yml html css js py ps1 sh sql |
| other | anything not listed, including files with no extension |

Matching is case-insensitive. The bucket list is printed in the dry-run
report so you can rename or merge buckets before anything is created.

### Date source, in order

1. A date in the filename, if it is unambiguous (`2026-03-14`, `20260314`,
   `2026-03`). Filenames are the author's statement of when the thing is from.
2. Otherwise the file's last-write time. Creation time is not used: on
   Windows it is reset by copies and downloads and is the least trustworthy
   stamp on the file.

The report shows, for every file, which rule chose the month, so a wrong
guess is visible before the move.

## Steps

### 0. Freeze the source

- Confirm nothing else writes to the source folder during the run (no sync
  client mid-upload, no open documents). If it is inside a synced tree, pause
  the sync for the duration.
- Confirm free space at the destination is at least the total size of the
  source, because the copy step holds two full copies at once.

### 1. Manifest the source (read-only)

For every file in the source folder, including hidden and system files and
any subfolders, record one row:

```
relative path | size in bytes | last-write time | SHA-256
```

Save as `MANIFEST-before.csv` next to the plan, not in the source or
destination. Also record the totals: file count and byte total. Expect 200
files; if the count differs, stop and report the real number before going on.

### 2. Dry run: build the mapping (read-only)

Produce `MAPPING.csv` with one row per file:

```
source path | bucket | month | date rule used | destination path | note
```

Rules applied here, with the result written in the `note` column:

- **Name collision.** Two files that would land at the same destination path
  are not renamed silently. If their hashes match they are byte-identical:
  keep one, record the other as `duplicate of <path>`, and it is still
  copied, into `_duplicates\` under the destination root, so nothing is
  discarded. If their hashes differ, the second gets the suffix
  `~2`, `~3`, and the note says so.
- **Unknown extension or no extension.** Bucket `other`, note `unknown type`.
- **No usable date.** This cannot happen (last-write always exists), but a
  last-write time before 1990 or after today is flagged `suspect date` and
  the file goes to `<bucket>\undated\`.
- **Zero-byte files.** Moved like any other, noted `empty`.

Deliverable of this step: the mapping and a summary (files per bucket, files
per month, count of collisions, duplicates, unknowns, suspect dates). You
review this before anything is written to disk. Fix the bucket list or the
layout here, rerun the dry run, repeat until the mapping is right.

### 3. Copy

- Create the destination folders from the mapping.
- Copy, do not move, each file to its destination path, preserving
  timestamps (`robocopy` with `/COPY:DAT`, or `Copy-Item` followed by
  setting `LastWriteTime` from the manifest).
- Copy errors are logged to `COPY-ERRORS.txt` and the run continues; one
  locked file must not leave the other 199 half-done.

### 4. Verify (the proof)

For every destination file in the mapping, compute size and SHA-256 and write
`MANIFEST-after.csv` in the same shape as the before manifest.

Then compare, and write `PROOF.md` with these checks, each PASS or FAIL:

1. **Count.** Rows in after = rows in before = destination files on disk.
   No file was skipped and nothing extra appeared.
2. **Hash match.** Every source hash appears at its mapped destination path.
   Content is byte-identical.
3. **Byte total.** Sum of sizes before = sum after.
4. **No orphans.** Every file under the destination root is in the mapping.
   Nothing landed in an unplanned place.
5. **Source unchanged.** Rehash the source folder; it still equals
   `MANIFEST-before.csv`. Nothing was modified or removed during the copy.

Any FAIL stops the plan at this point. The source is still intact, the
destination is a partial or full copy, and the report says which rows failed.
Nothing is deleted.

### 5. Remove the source, only after a clean PROOF

- With all five checks at PASS, delete the source files. Prefer moving the
  source folder to a holding folder (`_source-verified-2026-10-08\`) and
  deleting that after a day or two, rather than deleting on the spot. The
  holding folder costs disk space for a short time and buys a free undo.
- Append to `PROOF.md`: time of removal, what was removed, and the final
  destination file count read from disk.

### 6. Hand back

Deliverables, all in one folder beside this plan:

- `MANIFEST-before.csv`, `MANIFEST-after.csv`, `MAPPING.csv`
- `PROOF.md` with the five checks and the removal record
- `COPY-ERRORS.txt` (empty on a clean run)
- A short readme at the destination root naming the bucket rules and the
  date rules, so the next person who adds a file follows the same scheme.

## What would go wrong, and what catches it

| Risk | Caught by |
|---|---|
| A file is skipped | Check 1 (count) and check 4 (orphans) |
| A file is corrupted in copy | Check 2 (hash) |
| Two files collide and one overwrites the other | Collision rule in step 2; check 1 |
| Something edits a file mid-run | Check 5 (source rehash) |
| Dates are wrong | Date rule shown per row in the dry run, reviewed before copy |
| Wrong bucket list | Dry-run summary, reviewed before copy |
| Deletion before proof | Step 5 is gated on all five PASS; no other step deletes |

## Decisions I need from you before step 3

Steps 0 to 2 are read-only and need no approval. Before anything is written:

**A. Layout order** (recommended: 1)
1. `type \ month` (as written above)
2. `month \ type`
3. `type` only, no month
4. `year \ month` only, no type

**B. Date rule** (recommended: 1)
1. Filename date first, then last-write time (as written above)
2. Last-write time only
3. Filename date only; everything without one goes to `undated`

**C. Source removal** (recommended: 1)
1. Move source to a holding folder, delete it after you say so
2. Delete source immediately after a clean PROOF
3. Leave the source in place; this is a copy, not a move

## Close

1. Approve as written
2. Approve with changes (name them)
3. Revise
4. Cancel
