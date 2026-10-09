# Plan: move 200 mixed files into a dated, typed layout, and prove nothing was lost

Conclusion first: one approval gate, one rule the mover follows, one proof the mover must produce. Everything else is mechanism.

## The outcome

Every file now in the source folder ends up at exactly one place of the form

    <destination>\<YYYY>\<YYYY-MM>\<type>\<original filename>

where `YYYY-MM` is taken from the file's own modified date and `<type>` is one of a short fixed list derived from the extension (for example `documents`, `images`, `spreadsheets`, `audio`, `video`, `archives`, `other`). The source folder is empty when it is done. A manifest proves the before and the after match.

## The one rule

Copy, verify, then delete. Never move in one step. A file is deleted from the source only after its copy at the destination has the same SHA-256 hash.

That single rule is the whole safety story. It makes the operation restartable (re-run skips files already verified), it makes it reversible until the last step (the source is untouched until proof exists), and it makes the proof automatic (the hashes are the proof).

## The one approval gate

Before anything is written, the mover produces a dry-run table: `source path → destination path`, 200 rows, plus the count of files per `<type>` and per `<YYYY-MM>`, and any rows flagged below. The person who asked reads it and says go. Nothing else needs a yes.

Rows get flagged only when the mover cannot decide alone:

- two source files would land at the same destination path (same name, same month, same type)
- a file whose extension is not in the type list (it goes to `other`; the flag is just so you see it)
- a file with a modified date that looks wrong (before 1990 or in the future)

If no rows are flagged, the dry run is just a list to glance at.

## The steps

1. **Inventory (read-only).** Walk the source folder. For each file record: relative path, size in bytes, modified date, SHA-256. Write this as `manifest-before.csv` in a working folder outside both source and destination. Count: 200 rows expected. If not 200, stop and say so.
2. **Plan (read-only).** From the manifest compute each destination path. Write `plan.csv` (source, destination, type, month). Print the summary counts and flagged rows. **Gate: wait for go.**
3. **Copy.** For each row: create the destination folder if missing, copy the file, hash the copy, compare to the manifest hash. On match, mark the row `verified`. On mismatch, leave the source alone, record the row as `failed`, and continue with the rest.
4. **Delete.** For every row marked `verified`, delete the source file. Touch nothing else in the source.
5. **Prove.** Walk the destination tree and hash every file into `manifest-after.csv`. Then check, and print the result of each check:
   - `manifest-after` has exactly 200 rows (or 200 minus the failed rows, with the failed rows named)
   - the multiset of SHA-256 values in `manifest-after` equals the multiset in `manifest-before`
   - total bytes before equals total bytes after
   - the source folder contains zero files (or only the failed ones, named)
6. **Hand back.** Return the five lines from step 5, the path to the three CSVs, and the list of failed rows if any. If every check passes and nothing failed, the job is done. If anything failed, the source still holds those files untouched and the person decides what to do with them; nothing needs rolling back because nothing verified was lost.

## What this plan deliberately leaves out, and why

- **No backup copy of the source first.** The copy-verify-delete rule means the source *is* the backup until each file is proven. A separate backup would double the disk and add nothing.
- **No per-type or per-batch approvals.** The dry-run table shows every destination before a byte moves; approving it once covers all 200.
- **No renaming.** Original filenames are kept, so the manifest is the map and no name-mapping table is needed. Collisions are the one case that needs a human, so they are flagged, not auto-suffixed.
- **No date parsed from filenames.** Modified date is available for every file and consistent; filename dates are not. If the person wants a different date source, that is one change to step 2 and nothing else.
- **No rollback procedure.** There is nothing to roll back: at every moment each file exists verified at the destination, or untouched at the source, never neither.

## What would change this plan

- If the source holds subfolders whose structure carries meaning, keep the relative path under `<type>` rather than flattening. One line in step 2.
- If the 200 files include very large ones (many GB), hash with a streaming read and expect the run to take minutes rather than seconds; the steps do not change.
- If the destination already has files in it, step 5's row count becomes "after minus pre-existing," and step 1 should also manifest the destination so the pre-existing set is known.

## Approve

1 approve as written · 2 approve with changes · 3 revise · 4 cancel
