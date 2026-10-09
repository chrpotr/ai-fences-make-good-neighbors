# Plan: move 200 mixed files into a dated, typed folder layout, and prove nothing was lost

Plan date: 2026-10-08. Status: proposed, not approved. Nothing has been run.

## Conclusion first

Copy, check, then retire. Each of the 200 files is copied into `<target>\YYYY-MM\<type>\`, with a fingerprint (SHA-256 hash) taken before and after. The originals stay where they are until the check passes with zero differences. Then they move to a holding folder, and you decide when to delete them. The proof is two manifests and one comparison report. Together they show that every source file has exactly one copy in the new layout, with the same bytes, the same size, and the same modified date, and that there are no extra or missing files.

Five things are open (section 9). Each has a recommended default. Nothing runs until you answer them and approve the plan.

## 1. What this plan assumes (each one is checked in phase 0, not trusted)

| # | Assumption | How phase 0 checks it |
|---|---|---|
| A1 | The source is one folder holding about 200 files | Count the files; stop if the count is not what you expect |
| A2 | The source is flat (no subfolders), or subfolders are meant to be flattened | List the subfolders; if any exist, ask you (Q4) |
| A3 | No file or folder in scope is behind a hard wall (FINANCIALS, FAMILY, HEALTH, any casing) | Check every path in the manifest against the wall names; any hit stops the run, and the hit is reported by count only, not by name |
| A4 | The target folder does not exist yet, or is empty | Check before any write; if it holds files, stop and ask |
| A5 | The drive has room for a full second copy | Compare free space with total source bytes x 1.1 |
| A6 | No other session or sync process is writing to the source or target | Check those two paths only; no broad session or drive listing |

If any assumption fails, the run stops at phase 0 and you get a control report. Nothing is written.

## 2. The layout

```
<target>\
  2026-09\
    documents\
    images\
    spreadsheets\
  2026-10\
    documents\
    video\
  _undated\        (only if Q2 allows files with no usable date)
  _logs\           (manifests, map, report; never mixed with content)
```

**Date** = the file's last-modified date (Q2). Creation date is not used, because Windows resets it on every copy, so it is not reliable evidence.

**Type** comes from the file extension (case-insensitive):

| Folder | Extensions |
|---|---|
| documents | .pdf .doc .docx .txt .md .rtf .odt .pages |
| spreadsheets | .xls .xlsx .csv .ods .numbers |
| presentations | .ppt .pptx .key .odp |
| images | .jpg .jpeg .png .gif .heic .webp .tif .tiff .bmp .svg |
| video | .mp4 .mov .avi .mkv .webm |
| audio | .mp3 .m4a .wav .aac .flac |
| archives | .zip .7z .rar .tar .gz |
| data-and-code | .json .xml .html .htm .js .py .ps1 .yaml .yml |
| other | everything else, and files with no extension |

Phase 2 shows you every extension found and where it lands before anything moves. You can change this table then.

**Name clashes:** files keep their names. If two different files would land in the same folder with the same name, the second one gets ` (2)` before its extension, and the map records the rename. Files with identical content (same hash) are flagged, not merged. Removing duplicates is a separate decision and is out of scope.

## 3. Phases

Before and after each phase, check the work against this file (not memory of the conversation). If any evidence breaks an assumption, stop and report.

### Phase 0: Preflight (read-only)
1. Confirm the source and target paths from your answers to Q1. Never list `<root>` at its root.
2. Run the checks in section 1 (A1 to A6).
3. Note any hidden or system files, zero-byte files, read-only files, paths over 240 characters, and locked files. Each is reported. None is silently skipped.
4. **Output:** a control report (pass or stop, with counts). No writes.

### Phase 1: Before manifest (read-only, except for the log file)
1. For every file in the source, record: relative path, file name, extension, size in bytes, last-modified time (UTC, ISO 8601), and SHA-256 hash.
2. Save the result as `_logs\manifest-before.csv`, plus the total file count and total bytes.
3. **Gate:** the count must match phase 0. If it does not, stop.

### Phase 2: The map and a dry run (no file moves)
1. For each row in the before manifest, work out its destination: `<target>\<YYYY-MM>\<type>\<name>`, applying the clash rule.
2. Save `_logs\move-map.csv` with source path, destination path, hash, and any rename or flag.
3. Show you a summary: files per date folder, files per type folder, every extension and its type, every rename, every duplicate-content flag, and every `other` or `_undated` file.
4. **Gate:** you approve the summary (approval only, not a new plan). Then check the disk again for A4 and A6, because time has passed.

### Phase 3: Copy (originals untouched)
1. Create only the folders the map needs.
2. Copy each file to its mapped destination. Never overwrite: if a destination already exists, stop.
3. After each copy, set the copy's last-modified time to the value in the before manifest, so the date survives.
4. Log each copy (ok or error) to `_logs\copy-log.csv`. Any error stops the run. Copies already made stay in place, and the originals stay intact.

### Phase 4: Prove nothing was lost (read-only, except for the report)
1. Build `_logs\manifest-after.csv` from the target tree (excluding `_logs`), with the same fields as phase 1.
2. Compare the before manifest, the map, and the after manifest. All of these must hold:

| Check | Pass condition |
|---|---|
| Count | after = before = 200 (or the phase 0 count) |
| Total bytes | after = before |
| Every file arrived | each map row's destination exists in the after manifest |
| Bytes unchanged | each destination's SHA-256 = its source's SHA-256 |
| Size unchanged | each destination's size = its source's size |
| Date unchanged | each destination's last-modified time = its source's, to within 2 seconds |
| Nothing extra | no file in the after manifest is missing from the map |
| Nothing doubled | no source row maps to more than one destination |
| Placement correct | each file's folder matches its date and extension rule |
| Originals intact | re-hash the source; it matches the before manifest exactly |

3. Write `_logs\verification-report.md`: one line per check with PASS or FAIL and counts, then every exception listed by row. **Zero exceptions is the proof.** Any FAIL stops the run. Nothing is retired, and you get the report.

### Phase 5: Retire the originals (only after phase 4 passes, and only if you say so)
1. Move the originals into `<source parent>\_originals-held-YYYY-MM-DD\`. They are not deleted.
2. Re-hash the held folder against the before manifest. It must match, with zero exceptions.
3. Deleting the held folder is your call, whenever you choose. No agent permanently deletes data.

### Phase 6: Records and handoff
1. Add one dated entry to the active domain's designated record: what moved, from where to where, the counts, the location of the report, and where the originals are held. It opens with a plain-English line on what was done and why. This does not create a new register. If the domain has no record, propose one and wait.
2. Hand off: the report path, the PASS line, and the held-originals path.

## 4. Rollback
- **Before phase 5:** remove the target tree (send it to the Recycle Bin, not a permanent delete). The source was never touched, so nothing else needs undoing.
- **After phase 5:** move the held originals back to the source path and re-hash them against the before manifest.
- The before manifest and map are kept in `_logs\` for good, so the run can always be replayed or reversed.

## 5. Risks and how each one is handled

| Risk | Handling |
|---|---|
| a cloud sync client sync works mid-copy, or holds files open | Check sync is idle before phases 3 and 5; locked files stop the run; phase 4 re-hashes after sync settles |
| Modified dates are wrong (for example, files downloaded in bulk on one day) | The phase 2 summary shows the spread of dates. If most files share one day, the date rule is suspect, and Q2 is asked again before copying |
| A walled file is in the source | Phase 0 stops the run, and the file is reported by count only |
| A long path breaks the copy | Phase 0 flags it, and it is handled before phase 3 |
| Another session writes to the same folders | Checked in phase 0, and again at the phase 2 gate |

## 6. Tools
PowerShell 7 on this machine: `Get-ChildItem -File`, `Get-FileHash -Algorithm SHA256`, `Copy-Item` (never with `-Force`), and `Import-Csv`/`Export-Csv` for the comparison. The script lives in the session scratchpad, not in the source or target. Nothing is downloaded or installed.

## 7. Done means
- `verification-report.md` shows every check PASS with zero exceptions.
- The originals are either untouched (no phase 5) or held and re-verified.
- The record entry is written.
- You have the report path.

## 8. Out of scope
Removing duplicates, renaming files beyond the clash rule, reading file contents (only hashes are taken), and any folder other than the source and target.

## 9. Open questions (answer by number and letter; the recommended default is marked)

**Q1. Source and target paths**
- a) You give both full paths in your reply **(recommended: nothing can run without them)**
- b) Source given; target is a new sibling folder named `<source name> (organized)`

**Q2. Which date sets the folder**
- a) Last-modified date; files with no usable date go to `_undated` **(recommended)**
- b) A date in the file name (YYYY-MM-DD) if there is one, else last-modified
- c) Photo or video capture date (EXIF) for media, else last-modified

**Q3. Date granularity**
- a) `YYYY-MM` **(recommended: about 200 files spread over months stays readable)**
- b) `YYYY\YYYY-MM`
- c) `YYYY-MM-DD`

**Q4. If the source has subfolders**
- a) Stop and show them to you before going further **(recommended)**
- b) Flatten them, recording the original subfolder in the map
- c) Leave the subfolders where they are; organize only the top-level files

**Q5. What happens to the originals after the proof passes**
- a) Move them to `_originals-held-YYYY-MM-DD`, and you delete them later **(recommended)**
- b) Leave them in place, untouched
- c) Send them to the Recycle Bin (not a permanent delete)

---

**Approve this plan:** 1 approve as written · 2 approve with changes · 3 revise · 4 cancel
