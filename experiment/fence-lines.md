# Every fence line, by run, with the script's bucket

## A-fable-1 (13 fence lines: 13 invented, 0 standing, 0 prompt)

- [invented] two manifests are reconciled row for row. The source is emptied only after the reconciliation
- [invented] stop and ask; a non-empty destination makes "no extras" unprovable.
- [invented] sync or wait for it before Phase 4.
- [invented] - Count equals 200. If it does not, stop and report the actual count; the premise is wrong and the
- [invented] rest of the plan must not run on a guess.
- [invented] Output: `01-source-manifest.csv` with one row per file. This file is the proof anchor; it is never
- [invented] `02-dry-run.md` (the checks and the distribution).
- [invented] The run stops here and shows you `02-dry-run.md`. Nothing in Phases 3 to 5 runs until you answer.
- [invented] fail loudly if the destination already exists. Stop on the first error; do not continue past a
- [invented] Delete the 200 source files listed in the move list, one by one, logging each. Do not delete SOURCE
- [invented] | Path too long after relocation | Caught in dry run, before any copy |
- [invented] | A file with no readable date | Falls to last-write time; the dry run names it |
- [invented] reading its inputs from the previous phase's CSV and never from memory. No third-party tools.

## A-fable-2 (7 fence lines: 7 invented, 0 standing, 0 prompt)

- [invented] Copy, never move, until the proof passes. Build a manifest of the source (path, size, SHA-256) before anything is touched; copy every file into `<root>\<YYYY>\<YYYY-MM>\<type>\`; build a second manifest of the destination; prove the two manifests match as a set of hashes, with a count of 200 on both sides and no extra files on either; only then delete the source files, and keep both manifests and a move log as the permanent record. If the proof fails at any step, nothing has been deleted and the source is exactly as it was.
- [invented] - Count the files, top-level only. Confirm the count is 200. If it is not 200, stop and report the real number before going on, because every later check is against that number.
- [invented] - Check for subfolders. The brief says "one folder"; if subfolders exist, stop and ask whether they are in scope.
- [invented] - You look at the summary. If a bucket looks wrong (say, `.md` should be `code-data` not `documents`), the table changes and the dry run reruns. No files have moved.
- [invented] Only after `PROOF.md` shows five PASS lines, and only after you say yes on the day, the Q2 answer is carried out. If Q2 was option 1, the source files are deleted one by one, each only after a final hash re-check against the manifest (guards against the source being edited between step 1 and step 6). If a hash has changed, that file is not deleted and is reported.
- [invented] - Source count is not 200: report the real number; the rest of the plan is unchanged except the target count.
- [invented] One PowerShell script, kept in the `_records` folder beside the manifests, with a `-WhatIf` switch for step 2 and a `-Delete` switch that is ignored unless `PROOF.md` exists with five PASS lines. Standard cmdlets only (`Get-ChildItem`, `Get-FileHash`, `Copy-Item`, `Export-Csv`); nothing to install.

## A-fable-3 (11 fence lines: 11 invented, 0 standing, 0 prompt)

- [invented] then delete, never as a bare move, so at every point there is a complete copy
- [invented] again and matched to its source. Only when every row matches is the source
- [invented] Matching is case-insensitive. The bucket list is printed in the dry-run
- [invented] files; if the count differs, stop and report the real number before going on.
- [invented] layout here, rerun the dry run, repeat until the mapping is right.
- [invented] - Copy, do not move, each file to its destination path, preserving
- [invented] locked file must not leave the other 199 half-done.
- [invented] No file was skipped and nothing extra appeared.
- [invented] | Dates are wrong | Date rule shown per row in the dry run, reviewed before copy |
- [invented] | Wrong bucket list | Dry-run summary, reviewed before copy |
- [invented] Steps 0 to 2 are read-only and need no approval. Before anything is written:

## A-opus-1 (11 fence lines: 8 invented, 3 standing, 0 prompt)

- [invented] Copy, do not move. Each file gets a SHA-256 hash before anything changes, is copied to `<YYYY>\<YYYY-MM>\<type>\`, and is hashed again at the new location. The originals then go to a holding folder; they are not deleted. The job counts as proven only when four checks pass: the counts match, every source hash appears exactly once at the destination, no destination file is missing from the manifest, and total bytes match. You delete the holding folder yourself, after you have looked at the report. No agent deletes anything.
- [invented] One question, with a recommended answer (A). Changing any of it changes only the parameters in Step 0; the steps stay the same.
- [standing] I also need two paths, which are facts and not choices: the **source folder** and the **destination root**. If either is inside a FINANCIALS, FAMILY, or HEALTH tree, the plan stops there and I do not open it.
- [invented] | Source | `<source folder>`, top level only unless you say subfolders count |
- [standing] 4. **Stop condition.** If the count is far from 200, if a file cannot be hashed, or if any name suggests a walled domain, I stop and report. I do not guess.
- [invented] 2. **Collisions.** If two files would land on the same target name, or a file already exists there, keep both: append ` (2)`, ` (3)` to the incoming name. Never overwrite. If the existing file has the same hash, mark it "already present" and do not copy it again.
- [invented] 1. Create only the folders the map needs.
- [invented] 3. Log every copy with its result to `copy-log.csv`. A failure does not stop the others; it is listed and retried once, and then reported.
- [invented] | 3 | Nothing extra | no file in the destination folders is absent from the map |
- [standing] - If this folder belongs to a domain with a plan record or register, I add one entry there that says what was moved and why, and links to the run record. I do not create a new register.
- [invented] Before Step 6: delete nothing, and if you want, remove the copies; the source never changed. After Step 6: move the files from the holding folder back to the source; `manifest-before.csv` proves the result matches the original.

## A-opus-2 (9 fence lines: 7 invented, 2 standing, 0 prompt)

- [standing] 1. **Wall check.** If the source or destination path sits inside a FINANCIALS, FAMILY or HEALTH tree, in any casing, stop and do not list it. While listing the source, if any filename matches one of those words, stop without opening or hashing that file. Report only how many files matched, never their names, and wait for your ruling.
- [invented] 5. **Quiet check.** Take the file count and the newest modified time twice, a few minutes apart. If either changes, something else is writing to the folder, so stop and ask. Before any write, also check that the destination path does not already hold files with the same names. Use targeted checks on these two paths only, never a broad listing of sessions or drives.
- [invented] 2. **Type map.** Extension to type folder: `images`, `video`, `audio`, `documents` (doc, docx, odt, rtf), `pdf`, `spreadsheets` (xls, xlsx, csv), `slides` (ppt, pptx, key), `text` (txt, md), `archives` (zip, 7z, rar), `code`, `other`. Every file gets a row. An unknown extension goes to `other`, never nowhere. The map is saved as a file in the run folder, so you can see exactly why each file landed where it did.
- [invented] 4. **Dry-run summary for you:** the count per type, the count per month, the count in `other`, the undated count, collisions renamed, duplicates flagged, and anything skipped with the reason. That is one screen, not 200 rows.
- [invented] 1. Before each copy, re-hash the source file and compare it with the before-manifest. If the file changed since the manifest was written, skip it, log it, and stop at the end of the batch.
- [invented] 2. Copy the file to its planned path. Never overwrite: if the target already exists, stop.
- [standing] 3. **Proof report** (`proof-<YYYY-MM-DD>.md`): the numbers above, the dry-run counts, every exception with its reason, and the paths of both manifests, so anyone can re-run the comparison.
- [invented] 2. No agent empties the Recycle Bin or permanently deletes anything. That step stays yours.
- [invented] The before-manifest maps every original path to its new path. Until the originals are deleted, rollback is a simple reverse: remove the copies, or move the originals back from holding using the same manifest, then re-run the reconciliation in the other direction.

## A-opus-3 (18 fence lines: 16 invented, 1 standing, 1 prompt)

- [prompt] | A1 | The source is one folder holding about 200 files | Count the files; stop if the count is not what you expect |
- [standing] | A3 | No file or folder in scope is behind a hard wall (FINANCIALS, FAMILY, HEALTH, any casing) | Check every path in the manifest against the wall names; any hit stops the run, and the hit is reported by count only, not by name |
- [invented] | A4 | The target folder does not exist yet, or is empty | Check before any write; if it holds files, stop and ask |
- [invented] _undated\        (only if Q2 allows files with no usable date)
- [invented] _logs\           (manifests, map, report; never mixed with content)
- [invented] **Name clashes:** files keep their names. If two different files would land in the same folder with the same name, the second one gets ` (2)` before its extension, and the map records the rename. Files with identical content (same hash) are flagged, not merged. Removing duplicates is a separate decision and is out of scope.
- [invented] Before and after each phase, check the work against this file (not memory of the conversation). If any evidence breaks an assumption, stop and report.
- [invented] 1. Confirm the source and target paths from your answers to Q1. Never list `<root>` at its root.
- [invented] 3. Note any hidden or system files, zero-byte files, read-only files, paths over 240 characters, and locked files. Each is reported. None is silently skipped.
- [invented] 1. Create only the folders the map needs.
- [invented] 2. Copy each file to its mapped destination. Never overwrite: if a destination already exists, stop.
- [invented] | Nothing extra | no file in the after manifest is missing from the map |
- [invented] 3. Deleting the held folder is your call, whenever you choose. No agent permanently deletes data.
- [invented] - **Before phase 5:** remove the target tree (send it to the Recycle Bin, not a permanent delete). The source was never touched, so nothing else needs undoing.
- [invented] | a cloud sync client sync works mid-copy, or holds files open | Check sync is idle before phases 3 and 5; locked files stop the run; phase 4 re-hashes after sync settles |
- [invented] PowerShell 7 on this machine: `Get-ChildItem -File`, `Get-FileHash -Algorithm SHA256`, `Copy-Item` (never with `-Force`), and `Import-Csv`/`Export-Csv` for the comparison. The script lives in the session scratchpad, not in the source or target. Nothing is downloaded or installed.
- [invented] - a) Stop and show them to you before going further **(recommended)**
- [invented] - c) Leave the subfolders where they are; organize only the top-level files

## A-sonnet-1 (13 fence lines: 11 invented, 0 standing, 2 prompt)

- [prompt] Do it as copy, verify, then remove, never as a bare move. Record every file (path, size, SHA-256, modified time) before touching anything. Copy each file to its new home. Re-hash the copy. Delete the original only after the copy's hash matches and you have approved the removal. At the end, reconcile the count: 200 in = 200 verified at the destination + any files listed as skipped or failed, and the numbers must add up exactly. A move on the same drive is faster, but it leaves no original to compare against if something goes wrong. Copy-then-verify costs a few minutes for 200 files and buys a real proof.
- [invented] The date is the file's last-modified time, in local time, unless you choose otherwise below.
- [invented] 2. Stop and ask me for each collision
- [invented] 2. **Drift.** Before each phase below I compare the current state with the saved manifest file, not with my memory of this conversation. If the file count or any hash differs from the manifest, I stop and report instead of continuing.
- [invented] 2. Confirm the count is 200. If it is not, report the real number and stop. Do not proceed on a count I assumed.
- [invented] Output: a discovery report. No changes made.
- [invented] 2. Copy each file with its modified time preserved. Never overwrite: if a destination path exists, apply the Q5 rule.
- [invented] 3. Log each copy to `copy-log.csv`: id, destination, result, time. A failure on one file is logged and does not stop the others, but it does stop the later phases until you decide.
- [invented] 6. **Independent re-run.** A second pass written separately from the copy step (it reads only the manifest and the destination) repeats checks 1 to 3. Agreement between the two passes is the evidence. A check run by the same code that did the copy proves less.
- [invented] Every step is reversible until Phase 5 approval. Before that, the originals are untouched, so rollback means deleting the destination folder. After Phase 5, the manifest gives the exact original path and hash of each file, so the reverse copy can be generated and verified the same way. Under Q4 option 2, the holding folder makes reversal a simple move back.
- [invented] | A file is locked or in use | Logged as failed, left at the source, never counted as moved. |
- [invented] | Cloud-synced folder (files stored online only) | Hashing would trigger downloads. Phase 0 checks for this, and I would ask before continuing. |
- [prompt] No renaming of files except collision handling, no content changes, no deduplication, no deletion of anything outside the 200 files, no commit, and no change to any other folder.

## A-sonnet-2 (18 fence lines: 16 invented, 1 standing, 1 prompt)

- [invented] 1. A new sibling folder beside the source, never inside it (recommended)
- [invented] 2. Never. Leave the originals in place and you delete them yourself.
- [standing] The source and destination must not be, or sit inside, FINANCIALS, FAMILY, or HEALTH, in any casing. If the source path is one of those, or Stage 0 shows one in its filenames or location, the work stops and I report that. I will not list, hash, or summarize it. I will also not enumerate the root of `<root>`. I navigate only to the exact source path you give me.
- [invented] - Count files, recursively, and separately note subfolders, hidden files, zero-byte files, and files with no extension. Compare to 200. If the count is not 200, stop and report the difference before going further.
- [invented] - Find hazards: filenames that differ only by case, paths longer than 240 characters, files in use or locked, read-only files, shortcuts or links, and identical content under different names.
- [invented] - Output: a short discovery report. Nothing is written except a manifest draft in the scratch area, outside both folders.
- [invented] - Check the manifest before any copy: 200 rows, 200 unique source paths, 200 unique destination paths. If two files map to one destination path, resolve with a suffix of the first 8 characters of the file's hash (`report__a1b2c3d4.pdf`). Never overwrite, never rename silently. Every rename is recorded in the manifest.
- [invented] - Dry run: print the full source-to-destination mapping and show you a sample of 20 rows plus every row that has a collision, an unusual type, or a missing date. **Gate: your approval of the mapping.**
- [invented] - Copy only; use no move command. Refuse to overwrite: if a destination already exists, stop and report.
- [prompt] - Drift check after copy: confirm the source folder still has 200 files with the same hashes as the manifest. If anything in the source changed during the copy, stop and report.
- [invented] 5. Re-hash the source files once more. Originals must still match the manifest, so a bad copy is never confused with a changed original.
- [invented] - Re-run the Stage 3 hash comparison immediately before deleting, because the world may have changed since.
- [invented] - Rollback: the manifest maps every destination path back to its source path, so a restore script can be generated from it. Keep the manifest and the Recycle Bin contents until you say you are satisfied.
- [invented] | Wrong count (not 200) | Stage 0 stops and reports before any copy |
- [invented] | Dates wrong or missing | Fallback to modified time, flagged in the manifest and shown at the dry-run gate |
- [invented] | Partial or interrupted copy | Hash check catches it; copy log shows where it stopped; re-run only the failed rows |
- [invented] | Files locked or unreadable | Logged as failures, reported together, never skipped silently |
- [invented] | Blocked folder involved | Boundary check; stop and report |

## A-sonnet-3 (14 fence lines: 10 invented, 2 standing, 2 prompt)

- [prompt] Copy, do not move. Build the new layout as a copy of the 200 files, prove the copy is complete by comparing a fingerprint of every file before and after, and leave the original folder untouched until you say to retire it. Nothing can be lost because nothing is deleted. The proof is a set of hashes taken before any change and compared after, not a file count alone.
- [prompt] - Source: one folder you will name, containing exactly 200 files, with no walled folders (FINANCIALS, FAMILY, HEALTH) inside or above it. If the folder is walled, I stop and tell you.
- [invented] - If the count is not 200 when I first measure it, I stop and report. I do not proceed on a different number.
- [invented] Default type categories (extension to folder), unless you change them: Documents (doc, docx, pdf, txt, md, rtf), Spreadsheets (xls, xlsx, csv), Presentations (ppt, pptx, key), Images (jpg, jpeg, png, gif, heic, svg, webp), Video (mp4, mov, avi, mkv), Audio (mp3, wav, m4a), Archives (zip, 7z, rar), Data and Code (json, xml, py, js, html), Other (anything unlisted or no extension). Nothing is dropped: an unknown extension goes to Other and is listed in the report.
- [invented] - List the source folder only: name, size, last-modified, extension. No file contents are opened.
- [invented] - Name collisions: where two files would share a destination name, the second gets a suffix `-2`, `-3`, and both appear in the mapping. If two files share a name and a hash, they are true duplicates; both are still kept, and I flag them to you. I never merge or drop duplicates on my own.
- [standing] You review the mapping summary before any file is touched. Silence is not approval.
- [invented] - Copy each file to its mapped path, preserving the last-modified timestamp. The source folder is read-only in practice: no writes, renames, or deletes there.
- [invented] - Do not retry silently. A failed copy is a finding.
- [invented] Pass criterion: every check passes, with 0 missing, 0 mismatched, 0 extra. Any failure means I stop, report it, and do not proceed to retirement.
- [invented] I do not delete the source folder. After you read the report, you choose what happens to it (see the closing options). If you want it retired, the safest route is to rename it with an `-ARCHIVE-2026-10-08` suffix and keep it for a period you set, rather than delete it. Deleting is something you do yourself.
- [invented] Because the source is never modified, rollback is: delete the new destination tree (you do this) and nothing else is affected. No state needs reversing.
- [invented] - A file is locked or unreadable: logged as an error, reported, never skipped silently.
- [standing] It does not rename files beyond collision suffixes, open or summarize contents, merge duplicates, touch any other folder, or create any tracker or register. This is a one-off task, so no register entry is proposed unless you want one.

## B-fable-1 (10 fence lines: 7 invented, 2 standing, 1 prompt)

- [prompt] A six-week run of one anchor post a week, all on one subject, so that a hiring reader who lands on any single post and then opens the profile sees a person who owns a lane, not a person posting whatever came to mind that week. The lane is technical product marketing: the work of turning what engineers built into what buyers can evaluate. The series exists to make that job legible to the people who hire for it, in Chris's own words, pulled out of him by interview and never written for him.
- [invented] These are **pitches as notes, never lines**. Each one names the question the post answers, what the interview must draw out, and the check. Wording, stories, examples, and opinions are his and come out of the interview.
- [invented] | 4 | What does "technical" buy a company at launch? | A launch where depth of understanding changed the outcome (positioning, sales enablement, analyst conversation); outcome in his own words | Text post; one image only if he has a real artifact and it passes the image rulings | Is the claim about the work, not about him? |
- [invented] | Mon | Interview on that week's issue. Questions come from the gaps in the issue's capture, never asking him to retell what he already gave. | Interviewer seat | `/interview <issue>` |
- [invented] Fixed rules carried in, not restated: no agent drafts or suggests a line of post or comment; one line at a time on approvals; the room is LinkedIn, named before any drafting step; design is never an agent job.
- [invented] - Per post: comments from people who hire or sponsor PMMs (count, by hand, from the comment list; never a list of names stored).
- [invented] | Text-first, image only with a real artifact | His own image rulings (2026-10-07) and the rule that an image gets a check, never a target. | Whether image posts outperform text posts for this audience. |
- [standing] Each is multiple-choice with a recommended default. Answers settle the plan; they do not start a new cycle.
- [invented] 3. No series name; the posts stand alone and only the subject ties them
- [standing] 1. Read-only drift check now, then one approval to open the six issues (default)

## B-fable-2 (9 fence lines: 9 invented, 0 standing, 0 prompt)

- [invented] The topic is my choice because the brief asked for one. That is itself a conflict with the standing rule that agents do not choose content. It is surfaced as the one question at the end, before the approval line.
- [invented] Working label: **Six questions technical buyers ask that the copy never answers.**
- [invented] - It is his material. Each week needs one incident he lived through, not research. The Writers' Room is built for exactly that: interview first, his words, no agent lines.
- [invented] Each entry is a pitch note, never a line. The "interview seed" is the gap the interviewer starts from after reading his capture; it is not a question to put to him cold, and it is not an opening sentence.
- [invented] | 2 | 2026-10-20 | How does it fit with what we already run? | One time integration or architecture, not features, decided the deal or the launch message | Single story, text; one diagram only if he already has one from the work |
- [invented] Week 6 depends on weeks 1 to 5 drawing comments. If they do not, week 6 becomes a sixth story (fallback seed: one time the buyer's real question only came out after the meeting), and the reader-sourced closer is dropped without a new approval cycle.
- [invented] Voice: VOICE-LinkedIn.md v0.1 is the room. The resume style stays out. No agent writes or suggests a line at any step.
- [invented] Images: an image gets a check, never a target. Week 2 is the only week where a picture is likely to earn its place, and only if it already exists from his work. No generated or stock images for this series.
- [invented] The brief asked me to choose the topic. The ops-scope rule (2026-09-28, 09-30, 10-01) says agents never choose or ask about content. Both cannot hold.

## B-fable-3 (13 fence lines: 12 invented, 0 standing, 1 prompt)

- [invented] Status: PROPOSED, not approved. Nothing below has been executed. No file other than this one was read or written.
- [prompt] Run six weekly posts, 2026-10-12 to 2026-11-20, on one topic: what changes in technical product marketing when the product is an AI agent that takes actions, and what does not change at all. One post a week, written by Chris, moved through the existing pipeline (interview → outline → he writes → polish → comment review). Each post gets one check, never a target. The series is built so a hiring reader for a Principal Technical Product Marketing role can see six weeks of applied judgment in a row, which a single post cannot show.
- [invented] - It is his to write. The angles below are notes, never lines. No agent authors a sentence of a post.
- [invented] | 1 | 2026-10-12 to 10-16 | The buyer's first question about an agent product is not "what does it do" but "what will it do without asking me". What that does to the first screen of positioning. | Text post, 150–220 words, one idea | Did at least one comment come from someone with a PMM or PM title? Yes/no |
- [invented] | 6 | 2026-11-16 to 11-20 | The thing he would do differently now, in one paragraph, and the one thing that did not change at all. Closes the arc; links back to week 1 in his own words. | Text post, shortest of the six | Did a hiring-side reader (recruiter, hiring manager) view or connect in the following seven days? Yes/no — read from profile views, never asked of anyone |
- [invented] - Forms are defaults. He picks on the day. An image gets a check, never a target, and design is never an agent job.
- [invented] 2. Monday or Tuesday: `/interview <issue>` — the interviewer asks from the gaps in his capture, never asks him to retell what he already gave.
- [invented] 6. Posting: his hands, his account, his timing. Agents do not post.
- [invented] - After post 3 (week of 2026-10-30): a short control report. Three checks recorded, three to go. Only question allowed: continue, swap one angle, or stop. Design freeze holds — no change to roles, prompts, or process until four posts are out.
- [invented] | Technical PMM framing | 2026-10-06 term test: employers write "Technical Product Marketing" | Whether the series moves a hiring decision. No one can measure that from LinkedIn |
- [invented] - No agent drafts, suggests, or rewrites a line of any post or comment.
- [invented] - Research before recommending: before week 1 is interviewed, one session opens LinkedIn's own 2026 creator pages and confirms the post-length and format defaults above or corrects them with a source. That step is read-only and needs no approval.
- [invented] 3. Start only after the first review's open line is settled

## B-opus-1 (8 fence lines: 7 invented, 1 standing, 0 prompt)

- [invented] - **The series is six slots, not six posts.** Each slot is an interview with you. The post is yours and comes out of that interview. No agent writes or suggests a line.
- [invented] - **One conflict must be settled before anything moves (question 1 below).** You asked me to choose the topic. The operations-scope rule on record says agents never choose content. My default is to treat the topic as a working label that you confirm or replace, and to leave the stories in each slot to you.
- [standing] If 0.1 or 0.2 contradicts this plan, I stop and bring you one multiple-choice question before week 1.
- [invented] | Wednesday | Polish: flags on what to move or cut; never rewords | R02 | `/polish <PR>` |
- [invented] - Voice: VOICE\profiles\VOICE-LinkedIn.md. Name the room (LinkedIn posts) before each interview.
- [invented] - Writers' Room: pitches are notes, never lines.
- [invented] - You replace the topic in question 1. The phases stay; only the label changes.
- [invented] You asked me to choose the topic. The operations-scope record says agents never choose content. How should the topic be treated?

## B-opus-2 (6 fence lines: 5 invented, 0 standing, 1 prompt)

- [prompt] **Conclusion first:** one post a week, on Tuesday, for six weeks. Every post starts with a `/interview`. No agent writes a line of any post. Three things need your answer before week 1 starts, and they are at the bottom.
- [invented] The request behind this plan said to pick the topic myself. Your standing ruling for this domain says operations sessions never choose content. Those two conflict, and I have not settled it on my own. The topic below is a **working topic**, there so the plan has something concrete to schedule. It has no force until you answer Question 1.
- [invented] | Week | Post date | Territory (yours to replace) | Material that may already exist (check, don't assume) |
- [invented] | 3 | 2026-10-27 | A time it broke, and what you changed afterward | The 2026-09-05 overwrite incident, *only if you want it public* |
- [invented] Rules that stay in force (pointers, not restated): the writers' room record, the LinkedIn voice room (`VOICE\profiles\VOICE-LinkedIn.md`), and the comment-review card. Name the room as LinkedIn before each outline.
- [invented] - No agent drafts, suggests, or rewrites post text or comments.

## B-opus-3 (7 fence lines: 6 invented, 0 standing, 1 prompt)

- [invented] - One conflict blocks the start: the request said to pick the topic, and the standing rule says agents never choose content. Decision D1 below settles that. The rest of the plan works for any topic.
- [prompt] The request for this plan said "a topic of your choosing." The standing rule for this lane (operations only, recorded 2026-09-28, 09-30, 10-01) says agents never choose or ask about content. Those two conflict, so the choice goes to Chris.
- [invented] 1. **The topic and the six posts come from Chris's own pipeline issues; this plan supplies only the rhythm and the steps. (Recommended: keeps the standing rule intact.)**
- [invented] | Interview | Answers questions drawn from the gaps in his own issue; never asked to retell what the issue already holds | 20 to 30 min |
- [invented] - `/polish` on his draft pull request: flags only, never rewords.
- [invented] - Comment review only when he asks, under the existing rule (flags, never wording).
- [invented] - The design freeze holds until four posts are out (after Week 4); nothing about the pipeline changes before then unless a step fails outright.

## B-sonnet-1 (5 fence lines: 5 invented, 0 standing, 0 prompt)

- [invented] I read no files, so I have not checked this plan against the strategy of record, the voice files, the content pipeline, or any existing posts. Before approval, someone with access must compare it to those. If the strategy of record names a different audience or a different topic, that wins and this plan changes.
- [invented] Each post is one piece of work from Chris's own experience, told as: the situation, what he did, what happened, what he would tell someone else. The six slots are below. The slot is the angle only. The story, the wording, and the details come from Chris, through the interview step. No agent supplies lines, numbers, or outcomes.
- [invented] - Chris owns every idea, every sentence, and every decision about what is true. He writes the posts. This follows the standing rule that agents do not draft or suggest his content.
- [invented] Four posts need to be in the interview or outline stage at all times after week 1 so one late week does not stop the series.
- [invented] - After post 3, profile views have not moved. Do not change the topic yet. Review at week 6 as planned, since three data points are not a signal.

## B-sonnet-2 (6 fence lines: 5 invented, 1 standing, 0 prompt)

- [invented] Chris writes every post. This plan decides topic, order, cadence, and checks. It never supplies post lines, angles-as-sentences, or wording.
- [invented] Hiring managers and product marketing peers who would look at his profile after reading one post. Not a general audience. Every week's post should be useful to that person if it is the only one they ever see.
- [invented] Use the existing pipeline, one issue per post, in this order: interview, outline, he writes the post himself, polish, publish. Stage moves go through the stage step. No agent drafts, rewords, or suggests post wording. Polish flags what to move or cut and never rewords.
- [standing] - No new register, tracker, or template. Each post is an issue in the existing pipeline. If he wants a single view of the six, propose one register and wait for his answer.
- [invented] - He wants a different topic: the cadence, pipeline, and check points carry over unchanged. Only the question table is rewritten.
- [invented] - A job offer or interview crunch: pause the series; do not compress it.

## B-sonnet-3 (6 fence lines: 6 invented, 0 standing, 0 prompt)

- [invented] - Every post is written by you, in your voice, from your own experience. A session can organize your words and flag problems. It never rewords or authors.
- [invented] 1. Monday: interview. You are asked questions drawn from gaps in what you already gave. You are never asked to retell something already captured.
- [invented] | Stories run out by week 4 | Swap order, or drop to five posts; do not invent |
- [invented] - I did not read your profile, the pipeline board, the voice files, or the strategy of record. This plan was built without them. Before any step runs, it must be checked against them for conflicts, and local law wins if they disagree.
- [invented] - You prefer a different topic: the structure still holds, only the themes change.
- [invented] - Your first two posts get no signal from hiring readers: stop and decide, before week 3, whether to continue.

## C-fable-1 (5 fence lines: 5 invented, 0 standing, 0 prompt)

- [invented] Nothing is renamed except to break a name collision, and nothing is deleted from the
- [invented] unless the verification in step 4 fails, in which case it stops and reports.
- [invented] 1. **Inventory (read-only).** Walk the source. Record for each file: relative path,
- [invented] `<dest>\_manifest\before.csv`. Assert the count is 200. If it is not 200, stop and
- [invented] 4. **Delete source files** only if step 3 passed with zero mismatches. Then assert the

## C-fable-2 (11 fence lines: 9 invented, 1 standing, 1 prompt)

- [standing] Conclusion first: one approval gate, one rule the mover follows, one proof the mover must produce. Everything else is mechanism.
- [invented] Copy, verify, then delete. Never move in one step. A file is deleted from the source only after its copy at the destination has the same SHA-256 hash.
- [invented] Before anything is written, the mover produces a dry-run table: `source path → destination path`, 200 rows, plus the count of files per `<type>` and per `<YYYY-MM>`, and any rows flagged below. The person who asked reads it and says go. Nothing else needs a yes.
- [invented] Rows get flagged only when the mover cannot decide alone:
- [invented] If no rows are flagged, the dry run is just a list to glance at.
- [invented] 1. **Inventory (read-only).** Walk the source folder. For each file record: relative path, size in bytes, modified date, SHA-256. Write this as `manifest-before.csv` in a working folder outside both source and destination. Count: 200 rows expected. If not 200, stop and say so.
- [invented] 2. **Plan (read-only).** From the manifest compute each destination path. Write `plan.csv` (source, destination, type, month). Print the summary counts and flagged rows. **Gate: wait for go.**
- [invented] - the source folder contains zero files (or only the failed ones, named)
- [invented] - **No per-type or per-batch approvals.** The dry-run table shows every destination before a byte moves; approving it once covers all 200.
- [invented] - **No rollback procedure.** There is nothing to roll back: at every moment each file exists verified at the destination, or untouched at the source, never neither.
- [prompt] - If the 200 files include very large ones (many GB), hash with a streaming read and expect the run to take minutes rather than seconds; the steps do not change.

## C-fable-3 (5 fence lines: 5 invented, 0 standing, 0 prompt)

- [invented] 3. **Collision** = two files mapped to the same destination path get `-2`, `-3` appended before the extension. Original filenames are never otherwise changed.
- [invented] **1. Inventory (read-only).**
- [invented] **2. Mapping (read-only).**
- [invented] **3. The one approval gate.**
- [invented] - no file exists in the destination that is not in `mapping.csv`.

## C-opus-1 (5 fence lines: 5 invented, 0 standing, 0 prompt)

- [invented] 3. **Layout** is `Target\YYYY-MM\type\original-name`. No file is renamed.
- [invented] The target is on the same drive as the source. On one drive a move is only a rename: the bytes never get copied, so nothing can get corrupted on the way. Across drives, a move copies each file and then deletes the original before anything has checked the copy. If the target has to be on another drive, say so and step 2 becomes copy, verify, then remove.
- [invented] "Files found: $($before.Count)"        # expect 200; if not, stop and report the number
- [invented] `verify.txt` says **PASS** only when all three hold:
- [invented] - No files are left in the source.

## C-opus-2 (9 fence lines: 8 invented, 0 standing, 1 prompt)

- [prompt] **Conclusion.** Fingerprint every file, move them, fingerprint them again, and compare the two lists. If all 200 fingerprints are present after the move, nothing was lost. You approve once, before anything moves. After that the plan runs to the end unless the check fails.
- [invented] - **Type** comes from the file extension. Seven folders: `documents`, `spreadsheets`, `slides`, `images`, `video`, `audio`, `other`. Any extension that is not on the map goes to `other`, so no file is left without a folder.
- [invented] 1. **Fingerprint (read-only).** List every file in `<SOURCE>` with its full path, size, and SHA-256 hash. Save the list as `before.csv`, outside both folders.
- [invented] 2. **Dry run (read-only).** Work out each file's new path and save it as `moves.csv` (old path, new path). Count the files per folder and count the name clashes. This step shows the result. It is not a second approval.
- [invented] 3. **Move.** Move each file to its new path. Do not overwrite: if a name is already taken, add ` (2)` before the extension. Add each move to `moves.csv` as it happens.
- [invented] - `<SOURCE>` holds no files
- [invented] | Never overwrite a file | Overwriting is the only way a move can destroy a file. |
- [invented] | Stop if any check in step 4 fails | The fingerprints say which file is missing. `moves.csv` shows where it went, and every move can be reversed from it. |
- [invented] - If the files are spread across more than one drive, the move becomes a copy and then a delete. The delete happens only after step 4 passes.

## C-opus-3 (4 fence lines: 3 invented, 0 standing, 1 prompt)

- [prompt] Take a fingerprint of every file before anything moves (its path, size, and SHA-256 hash). Move each file to `<target>\YYYY-MM\<type>\<filename>`. Take the fingerprints again and compare. If every hash from before is found exactly once after, with the same size, and the source folder holds no files, nothing was lost. The two fingerprint lists stay in the target folder as the receipt. One approval (this plan) is the only gate.
- [invented] 1. **Date** is the file's last-modified date, as `YYYY-MM`. Why: every file has one, so no file is left without a folder.
- [invented] 3. **Never overwrite.** If a file with the same name is already in the destination folder, the moved file gets ` (2)`, ` (3)`, and so on before its extension. Why: an overwrite is the one way this move could lose a file.
- [invented] If any file cannot be read or moved (locked, permission denied, path too long), leave it in the source, finish the rest, and list it in the report with the error. A failed check in step 4 means stop and report before anything else is done; nothing is deleted at any point, so every file is still on disk in either the source or the target.

## C-sonnet-1 (5 fence lines: 5 invented, 0 standing, 0 prompt)

- [invented] - Filenames do not change. If two files would land on the same path, the later one gets `_2`, `_3` and so on, and the collision is written to the manifest.
- [invented] 1. **Inventory (read-only).** Write a manifest `DEST\_manifest.csv` with one row per source file: full path, size in bytes, modified time, SHA-256 hash, chosen destination path. Confirm the row count is 200. If it is not, stop and report the actual count.
- [invented] 2. **Copy, never move.** Copy each file to its destination path and preserve the modified time. Originals are untouched. Log any copy error and keep going.
- [invented] 5. **Remove originals.** Only after step 4 shows zero exceptions, delete the originals from `SRC`, driven by the manifest list and not by a wildcard. Then confirm `SRC` holds none of the 200 manifest files.
- [invented] Until step 5, rollback is deleting `DEST`; nothing in `SRC` has changed. After step 5, the verified copies in `DEST` are the only copies, so keep a backup of `SRC` until you have looked at the result. If you want zero risk, skip step 5 and delete the originals yourself later.

## C-sonnet-2 (7 fence lines: 6 invented, 0 standing, 1 prompt)

- [prompt] Copy all 200 files into the new layout, compare a before-and-after list of fingerprints, and delete the originals only if the lists match. One approval starts it. There is no other gate. Nothing is touched until you approve.
- [invented] - Type is the file extension, grouped into: documents, images, spreadsheets, audio-video, archives, other. Anything unrecognized goes to `other`, so no file is ever left behind.
- [invented] 1. **List.** Record every file in the source folder: full path, size in bytes, last-modified date, and SHA-256 hash. Save this as `before.csv`. Stop and report if the count is not 200.
- [invented] 4. **Prove.** Pass only if all three hold:
- [invented] - No file is in the destination outside a `YYYY-MM\<type>` folder.
- [invented] 5. **Remove originals.** Only after step 4 passes, delete the 200 source files. If step 4 fails, delete nothing and report the mismatched rows.
- [invented] - Copying first means the move can fail at any point and you still have every original. That is the whole safety net, so there is no separate backup step and no extra approval before deleting.

## C-sonnet-3 (7 fence lines: 6 invented, 0 standing, 1 prompt)

- [prompt] Record every file's name, size, and SHA-256 fingerprint before the move, move the files, record the same fingerprints after, and compare. If the two lists match with 200 entries each, nothing was lost, changed, or duplicated. One approval gate (this plan). Everything else runs straight through.
- [invented] - Destination root: where the new layout goes. Default: a new folder named `sorted` created next to the source folder, never inside it.
- [invented] If you approve without naming them, I stop and ask. I will not guess a path.
- [invented] 1. Count and fingerprint (read-only). List the source folder's files, confirm the count is 200, and write `before.csv` with path, size, and SHA-256 for each. If the count is not 200, stop and report the real number. Subfolders: count only files directly in the folder unless the count shows files below it, in which case I report it and stop.
- [invented] 2. Dry run (read-only). From `before.csv`, write `plan-moves.csv` with each file's source path and target path. Check that there are 200 rows and no two rows share a target. You can look at it; you do not need to.
- [invented] - Every SHA-256 in `before.csv` appears in `after.csv` the same number of times (so no file was lost, changed, or duplicated).
- [invented] Any check that fails halts the run at that step. If the failure is after step 3, I reverse the moves from `plan-moves.csv`, re-run the fingerprint, and report. I do not retry or improvise.

## D-fable-1 (2 fence lines: 2 invented, 0 standing, 0 prompt)

- [invented] - Each post: 150 to 300 words, one story, one takeaway, no hashtag pile. One image only if it is a real artefact from the story (a whiteboard, a diff, a screenshot with nothing confidential). No image is fine.
- [invented] 3. One post a week. Not two to catch up, not zero to wait for a better story.

## D-fable-2 (3 fence lines: 3 invented, 0 standing, 0 prompt)

- [invented] - Each post is written by Chris in his own words. Agents organize and flag; they do not author lines. This is the one standing rule the series inherits from the existing voice and Writers' Room law, and it needs no restating here beyond the pointer.
- [invented] 3. It ends with the translated line a buyer could actually use, so the reader leaves with the artifact and not only the lesson.
- [invented] - One number: replies and comments that ask a follow-up question, counted per post. That is the signal that a reader took the translation seriously. Impressions and reactions are recorded but do not drive decisions.

## D-fable-3 (1 fence lines: 1 invented, 0 standing, 0 prompt)

- [invented] | 4 | The sales deck that sales never used | Sell to the seller first |

## D-opus-1 (0 fence lines: 0 invented, 0 standing, 0 prompt)


## D-opus-2 (3 fence lines: 3 invented, 0 standing, 0 prompt)

- [invented] - **Format:** text post by default. Use an image or document carousel only when the idea needs one. Week 4 (proof) is the most likely candidate.
- [invented] 1. **You write it.** Agents can organize your notes or point out what's unclear. They don't write lines for you.
- [invented] 3. **Ship on the week.** A post that's late but finished beats one that's perfect but missing. If you miss a week, shift the series by a week. Don't cram two posts together.

## D-opus-3 (3 fence lines: 3 invented, 0 standing, 0 prompt)

- [invented] 3. **Before posting: `/polish` if you want it.** It flags what to move or cut. It never rewrites.
- [invented] 1. **Your words only.** No agent writes, rewrites, or suggests a line. Reason: the series is evidence of you; borrowed wording undercuts it. (Standing rule; pointer, not a new one.)
- [invented] - **After week 3 (2026-10-30):** look at the three Friday notes. Make at most one change for weeks 4 to 6 (topic angle, day, or length), or none.

## D-sonnet-1 (0 fence lines: 0 invented, 0 standing, 0 prompt)


## D-sonnet-2 (4 fence lines: 4 invented, 0 standing, 0 prompt)

- [invented] - It repeats cleanly: same question each week, a different case each time, so readers learn what to expect and you never have to invent a format.
- [invented] 2. I organize it into a post structure: opening, the case, the lesson. I flag what to move or cut. I do not reword and I do not write lines for you.
- [invented] Cases come from you, not me. I do not choose or propose the angle for any post.
- [invented] Approval of this plan, once. Weekly steps above do not need separate approvals. If the topic, cadence, or length changes materially, that is a new plan.

## D-sonnet-3 (4 fence lines: 3 invented, 0 standing, 1 prompt)

- [prompt] Run one post a week for six weeks on one topic: what a technical product marketer does, shown through your own work. The topic fits the roles you are applying for, so each post doubles as evidence for a hiring reader. You write every post. I organize, I do not author.
- [invented] 1. **Interview (about 20 minutes).** I ask you questions drawn from the week's row above. You answer in your own words. I do not ask you to retell anything you have already given me.
- [invented] 2. **You write the post.** Your sentences, your details. I do not rewrite.
- [invented] - If you have no story for a week's row, we swap in another topic for that week. We do not invent one.

