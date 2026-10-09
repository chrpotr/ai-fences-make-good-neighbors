# Plan: move 200 files into a dated, typed layout and prove nothing was lost

**Conclusion.** One approval, three rules, one bound. Hash every file before the move. Move the files with a rename so no data is rewritten. Hash them again afterwards. If the two lists match file for file, nothing was lost. A move log makes the whole thing reversible, so no further gates are needed.

## What you give me (the only inputs)

- **Source:** the folder that holds the 200 files.
- **Target:** a new or empty folder on the **same drive** as the source.

## The three rules

1. **Date** is the file's last-modified month, written as `YYYY-MM`. Every file has one, and a move does not change it.
2. **Type** is the file extension in lower case, such as `pdf`, `jpg`, or `docx`. A file with no extension goes under `no-extension`.
3. **Layout** is `Target\YYYY-MM\type\original-name`. No file is renamed.

## The one bound, and why

The target is on the same drive as the source. On one drive a move is only a rename: the bytes never get copied, so nothing can get corrupted on the way. Across drives, a move copies each file and then deletes the original before anything has checked the copy. If the target has to be on another drive, say so and step 2 becomes copy, verify, then remove.

## Steps (PowerShell; run once, top to bottom)

```powershell
$Source = 'D:\path\to\source'          # fill in
$Target = 'D:\path\to\target'          # fill in; same drive, new or empty
$Proof  = Join-Path $Target '_proof'
New-Item -ItemType Directory -Force $Proof | Out-Null

# 1. Before: inventory and hash every top-level file
$before = Get-ChildItem -LiteralPath $Source -File -Force | ForEach-Object {
  $ext  = if ($_.Extension) { $_.Extension.TrimStart('.').ToLower() } else { 'no-extension' }
  $dest = Join-Path $Target (Join-Path $_.LastWriteTime.ToString('yyyy-MM') (Join-Path $ext $_.Name))
  [pscustomobject]@{ From = $_.FullName; To = $dest; Size = $_.Length
                     Hash = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash }
}
$before | Export-Csv (Join-Path $Proof 'before.csv') -NoTypeInformation
"Files found: $($before.Count)"        # expect 200; if not, stop and report the number

# 2. Move (no -Force, so it can never overwrite anything)
foreach ($f in $before) {
  New-Item -ItemType Directory -Force (Split-Path $f.To) | Out-Null
  Move-Item -LiteralPath $f.From -Destination $f.To
}

# 3. After: re-hash at the new paths and compare
$after = Get-ChildItem -LiteralPath $Target -File -Recurse -Force |
  Where-Object { $_.FullName -notlike "$Proof*" } | ForEach-Object {
  [pscustomobject]@{ To = $_.FullName; Size = $_.Length
                     Hash = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash }
}
$after | Export-Csv (Join-Path $Proof 'after.csv') -NoTypeInformation

$diff = Compare-Object $before $after -Property To, Size, Hash
$left = @(Get-ChildItem -LiteralPath $Source -File -Force).Count
$ok   = ($before.Count -eq $after.Count) -and (-not $diff) -and ($left -eq 0)
"Before: $($before.Count)  After: $($after.Count)  Mismatches: $(@($diff).Count)  Left in source: $left  Result: $(if ($ok) {'PASS'} else {'FAIL'})" |
  Tee-Object (Join-Path $Proof 'verify.txt')
$diff | Export-Csv (Join-Path $Proof 'mismatches.csv') -NoTypeInformation
```

## What counts as proof

`verify.txt` says **PASS** only when all three hold:

- The count before equals the count after.
- Every file appears at its expected new path, with the same size and the same SHA-256 hash as before. Zero mismatches.
- No files are left in the source.

`before.csv`, `after.csv`, and `verify.txt` stay in `Target\_proof\` as the record.

## If it says FAIL

Nothing has been deleted, because a move on one drive only renames. `mismatches.csv` names each file that failed. To undo everything, move each row of `before.csv` from `To` back to `From`.

## Not covered

- Subfolders inside the source, and anything in them, are left where they are.
- The source folder itself is not removed.

## Your call

1. approve as written (recommended): send the source and target paths with your approval
2. approve with changes
3. revise
4. cancel
