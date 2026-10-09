# Plan: move 200 mixed files into a dated, typed layout and prove nothing was lost

Written 2026-10-08. Plan only. Nothing has been read, listed, moved, or run. The source folder and
destination folder are inputs you supply; every step below is written so it works for any pair of
folders on the same machine.

## Conclusion

Copy first, prove, then delete. The files are inventoried and hashed (SHA-256) before anything
moves, copied into the new layout from a written move list, hashed again on the far side, and the
two manifests are reconciled row for row. The source is emptied only after the reconciliation
report shows 200 planned, 200 landed, 200 hash matches, 0 unmatched, 0 extras. Every step leaves a
file behind, so the move is reversible until the last one and auditable after it.

Estimated run time once approved: under ten minutes for 200 files on a local disk.

## Inputs you give before anything runs

| Input | What it is | Default if you say nothing |
|---|---|---|
| SOURCE | The folder holding the 200 files | none; required |
| DEST | The root of the new layout | a new empty folder beside SOURCE named `<SOURCE name> (sorted)` |
| RUN | Where scripts, manifests, and the report live | `...\2026-10-08 Fences\experiment\runs\A-fable-1\` |

Hard wall: if SOURCE, DEST, or any path inside them touches FINANCIALS, FAMILY, or HEALTH in any
casing, the run stops before Phase 1 and comes back to you. No exception is assumed.

## The target layout

```
DEST\
  <type>\
    <YYYY>\
      <YYYY-MM>\
        <original filename>
```

Type is the first split because people browse by kind, then by when. Two levels of date keep every
folder small enough to scan by eye.

Type buckets, by extension:

| Bucket | Extensions |
|---|---|
| documents | doc docx odt rtf txt md pages |
| spreadsheets | xls xlsx csv tsv ods numbers |
| presentations | ppt pptx key odp |
| pdf | pdf |
| images | jpg jpeg png gif heic webp tif tiff bmp svg |
| audio-video | mp3 wav m4a aac mp4 mov mkv avi webm |
| archives | zip 7z rar tar gz |
| code-and-data | json xml yaml yml html css js py ps1 sh sql |
| other | anything not listed, and files with no extension |

Date for each file, in this order of preference:

1. A date already in the filename that parses as YYYY-MM-DD, YYYYMMDD, or YYYY-MM.
2. Otherwise the file's last-write time.

Creation time is not used; on Windows it changes whenever a file is copied, so it is the least
trustworthy of the three.

Collision rule: if two files would land at the same path, the second keeps its name with the first
eight characters of its SHA-256 appended before the extension (`report (a1b2c3d4).pdf`). Nothing is
ever overwritten, and nothing is silently skipped.

## Phases

### Phase 0: preflight (read-only, no approval needed)

1. Confirm SOURCE exists and DEST either does not exist or is empty. If DEST already has files,
   stop and ask; a non-empty destination makes "no extras" unprovable.
2. Confirm SOURCE and DEST are on the same volume. If not, the plan still works, only slower.
3. Check whether SOURCE sits inside a cloud-synced tree (a cloud sync client, OneDrive). If so, note it in
   the report; sync clients can hold files open or re-create deleted ones, and the run will pause
   sync or wait for it before Phase 4.
4. Check for anything that breaks a simple move: reparse points or symlinks, paths longer than 250
   characters once relocated, hidden or system files, zero-byte files, files currently locked. Each
   is listed, not fixed.

Output: `00-preflight.md` in RUN.

### Phase 1: inventory and hash (read-only)

For every file directly in SOURCE (and in subfolders, if you say so; default is top level only),
record: relative path, size in bytes, last-write time, SHA-256.

Checks on the inventory:

- Count equals 200. If it does not, stop and report the actual count; the premise is wrong and the
  rest of the plan must not run on a guess.
- Duplicate hashes are listed (same content, different names). They are kept, both of them; this
  plan sorts, it does not deduplicate.

Output: `01-source-manifest.csv` with one row per file. This file is the proof anchor; it is never
edited after this phase.

### Phase 2: dry run (read-only)

Compute the destination path for every row in the source manifest using the layout, bucket table,
date rule, and collision rule above. Write it down. Then check:

- Every destination path is unique.
- No destination path is longer than 250 characters.
- Every row has a bucket (anything that fell to `other` is listed so you can see what it was).
- Every row has a date, and the report says which rule gave it (filename or last-write).

Also produce a distribution table: how many files per bucket, per month, per date rule. This is
what you look at to decide whether the layout is right before a single file moves.

Output: `02-move-list.csv` (source path, destination path, size, hash, bucket, date, date rule) and
`02-dry-run.md` (the checks and the distribution).

### Gate: concurrence

The run stops here and shows you `02-dry-run.md`. Nothing in Phases 3 to 5 runs until you answer.
Silence is not approval.

### Phase 3: copy

For each row in the move list, in order: create the destination folder if needed, copy the file,
fail loudly if the destination already exists. Stop on the first error; do not continue past a
failed copy. Each copy appends one line to `03-copy-log.csv` with the row, the result, and a
timestamp.

Copy is used instead of move at this stage on purpose. Until Phase 4 proves the copies are good,
the source is untouched and the whole run can be abandoned with zero loss by deleting DEST.

### Phase 4: prove

1. Hash every file now in DEST, recursively, into `04-dest-manifest.csv` with the same columns as
   the source manifest.
2. Reconcile the two manifests against the move list:
   - Planned: rows in the move list. Must be 200.
   - Landed: rows in the destination manifest. Must be 200.
   - Matched: destination rows whose path is in the move list AND whose hash and size equal the
     source row's. Must be 200.
   - Unmatched source rows (planned, not landed, or landed with the wrong hash). Must be 0.
   - Extras (in DEST, not in the move list). Must be 0.
   - Source re-hash: hash SOURCE again and compare to `01-source-manifest.csv`. Must match; this
     catches a file that changed under the run.
3. Write `04-reconciliation.md`: the six numbers above, the lists behind any non-zero, and a
   one-line verdict: PROVEN or NOT PROVEN.

If the verdict is NOT PROVEN, Phase 5 does not run, DEST is left in place for inspection, and the
report comes back to you with the unmatched or extra rows named.

### Phase 5: release the source

Only on PROVEN, and only on your word (second gate, one question, default yes if Phase 4 is clean).
Delete the 200 source files listed in the move list, one by one, logging each. Do not delete SOURCE
itself or anything in it that was not in the manifest. After deletion, list SOURCE: it should hold
nothing from the move list.

Output: `05-release-log.csv` and a final line appended to the reconciliation report.

### Phase 6: records

Leave RUN in place with all seven files. Write `README.md` in RUN that says, in plain English, what
was moved, from where, to where, when, and that the reconciliation came back PROVEN, with the six
numbers. That is the file anyone opens later; the CSVs are the evidence behind it.

## Rollback

Until Phase 5 runs: delete DEST. Source is untouched.

After Phase 5: `02-move-list.csv` read right-to-left is the reverse move list. A reverse script
copies each destination path back to its source path, re-hashes, and reconciles the same way.
Nothing in the plan destroys information that the move list cannot undo.

## What could still go wrong, and what the plan does about it

| Risk | Handling |
|---|---|
| A file changes between inventory and copy | Source re-hash in Phase 4 catches it; the run reports NOT PROVEN |
| Two different files, same name, same date and type | Collision rule appends a hash prefix; both land |
| Identical content under two names | Both kept; listed in Phase 1 so you know |
| Cloud sync re-creates a deleted file or locks one | Preflight flags the tree; Phase 5 waits for sync idle and re-lists SOURCE |
| Copy preserves content but not creation time | Accepted; content and last-write are what matter, and the manifest records the originals |
| Path too long after relocation | Caught in dry run, before any copy |
| A file with no readable date | Falls to last-write time; the dry run names it |
| Count is not 200 | Stops in Phase 1; the plan is for 200 and does not guess |

## Tooling

PowerShell 7 on this machine: `Get-ChildItem`, `Get-FileHash -Algorithm SHA256`, `Copy-Item`,
`Export-Csv`, `Compare-Object`. One script per phase, each saved in RUN before it runs, each
reading its inputs from the previous phase's CSV and never from memory. No third-party tools.

## Decisions that need your answer before the run

**Q1. Layout order** (default: a)
a. type \ year \ month (as written above)
b. year \ month \ type
c. year-month \ type, one date level only

**Q2. Date rule when the filename has a date and it disagrees with last-write** (default: a)
a. Filename wins
b. Last-write wins
c. Flag it and stop

**Q3. Subfolders inside SOURCE** (default: a)
a. Top level only; subfolders are reported and left alone
b. Recurse; flatten everything into the layout
c. Recurse; keep the subfolder name as a suffix on the filename

**Q4. Where RUN lives** (default: a)
a. `...\2026-10-08 Fences\experiment\runs\A-fable-1\`
b. Inside DEST as `_run\`
c. Somewhere you name

## Close

1 approve as written · 2 approve with changes · 3 revise · 4 cancel
