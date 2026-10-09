# Plan: move 200 mixed files into a dated, typed layout, and prove nothing was lost

Date: 2026-10-08

## The plan in one paragraph

Take a fingerprint of every file before anything moves (its path, size, and SHA-256 hash). Move each file to `<target>\YYYY-MM\<type>\<filename>`. Take the fingerprints again and compare. If every hash from before is found exactly once after, with the same size, and the source folder holds no files, nothing was lost. The two fingerprint lists stay in the target folder as the receipt. One approval (this plan) is the only gate.

## The layout

```
<target>\
  2026-09\
    documents\
    images\
  2026-10\
    spreadsheets\
    other\
  _manifest-before.csv
  _manifest-after.csv
```

## The three rules

Each rule exists because the move cannot run without it.

1. **Date** is the file's last-modified date, as `YYYY-MM`. Why: every file has one, so no file is left without a folder.
2. **Type** is set by the file extension from this table. Anything not in it goes to `other`. Why: a fixed table means the same file always lands in the same place.

   | Type | Extensions |
   |---|---|
   | documents | .pdf .doc .docx .txt .md .rtf |
   | spreadsheets | .xls .xlsx .csv |
   | presentations | .ppt .pptx |
   | images | .jpg .jpeg .png .gif .heic .webp .svg |
   | video | .mp4 .mov .avi |
   | audio | .mp3 .wav .m4a |
   | archives | .zip .7z .rar |
   | other | everything else |

3. **Never overwrite.** If a file with the same name is already in the destination folder, the moved file gets ` (2)`, ` (3)`, and so on before its extension. Why: an overwrite is the one way this move could lose a file.

No other rules. Files in subfolders of the source are included; their original path is kept in the manifest, so flattening loses nothing.

## The steps

1. **Fingerprint.** For every file under the source, write path, size, last-modified date, and SHA-256 to `_manifest-before.csv`. Confirm the count is 200. If it is not, report the real count and continue with that count; the proof works for any number.
2. **Move.** For each file, compute its destination from the three rules and move it with `Move-Item`. Record the new path beside the old one in the before-manifest.
3. **Fingerprint again.** Write path, size, and SHA-256 for every file under the target (excluding the two manifests) to `_manifest-after.csv`.
4. **Prove.** All four checks must pass:
   - The after count equals the before count.
   - Every before hash appears in the after list, at the recorded new path, with the same size.
   - No after file is missing from the before list (nothing extra, nothing duplicated).
   - The source folder holds zero files.
5. **Report.** One short result: counts before and after, the four checks as pass or fail, files per date and type folder, and any renamed by rule 3.

## The only stop condition

If any file cannot be read or moved (locked, permission denied, path too long), leave it in the source, finish the rest, and list it in the report with the error. A failed check in step 4 means stop and report before anything else is done; nothing is deleted at any point, so every file is still on disk in either the source or the target.

## The script (PowerShell, run once)

```powershell
$Source = '<source folder>'
$Target = '<target folder>'
$Types = @{
  documents='.pdf .doc .docx .txt .md .rtf'; spreadsheets='.xls .xlsx .csv'
  presentations='.ppt .pptx'; images='.jpg .jpeg .png .gif .heic .webp .svg'
  video='.mp4 .mov .avi'; audio='.mp3 .wav .m4a'; archives='.zip .7z .rar'
}
function TypeOf($ext) { foreach ($k in $Types.Keys) { if (($Types[$k] -split ' ') -contains $ext.ToLower()) { return $k } }; 'other' }

# 1 Fingerprint
$before = Get-ChildItem $Source -File -Recurse | ForEach-Object {
  [pscustomobject]@{ OldPath=$_.FullName; Size=$_.Length; Modified=$_.LastWriteTime.ToString('yyyy-MM-dd')
    Hash=(Get-FileHash $_.FullName -Algorithm SHA256).Hash; NewPath=''; Error='' } }
"Before count: $($before.Count)"

# 2 Move
foreach ($f in $before) {
  try {
    $dir = Join-Path $Target (Join-Path $f.Modified.Substring(0,7) (TypeOf ([IO.Path]::GetExtension($f.OldPath))))
    New-Item -ItemType Directory -Force $dir | Out-Null
    $base = [IO.Path]::GetFileNameWithoutExtension($f.OldPath); $ext = [IO.Path]::GetExtension($f.OldPath)
    $dest = Join-Path $dir "$base$ext"; $n = 2
    while (Test-Path -LiteralPath $dest) { $dest = Join-Path $dir "$base ($n)$ext"; $n++ }
    Move-Item -LiteralPath $f.OldPath -Destination $dest -ErrorAction Stop
    $f.NewPath = $dest
  } catch { $f.Error = $_.Exception.Message }
}
$before | Export-Csv (Join-Path $Target '_manifest-before.csv') -NoTypeInformation

# 3 Fingerprint again
$after = Get-ChildItem $Target -File -Recurse | Where-Object Name -notlike '_manifest-*' | ForEach-Object {
  [pscustomobject]@{ Path=$_.FullName; Size=$_.Length; Hash=(Get-FileHash $_.FullName -Algorithm SHA256).Hash } }
$after | Export-Csv (Join-Path $Target '_manifest-after.csv') -NoTypeInformation

# 4 Prove
$moved = $before | Where-Object NewPath
$byPath = @{}; $after | ForEach-Object { $byPath[$_.Path] = $_ }
"Check 1 counts match:      " + ($after.Count -eq $moved.Count)
"Check 2 every hash landed: " + (-not ($moved | Where-Object { $a = $byPath[$_.NewPath]; -not $a -or $a.Hash -ne $_.Hash -or $a.Size -ne $_.Size }))
"Check 3 nothing extra:     " + (-not ($after | Where-Object { $_.Path -notin $moved.NewPath }))
"Check 4 source empty:      " + ((Get-ChildItem $Source -File -Recurse).Count -eq ($before | Where-Object Error).Count)
$before | Where-Object Error | Select-Object OldPath, Error
```

Check 4 passes when the only files left in the source are the ones listed with an error.

## What is needed to run it

The source folder path and the target folder path. Nothing else.

## Approval

1 approve as written (send the two paths with it) · 2 approve with changes · 3 revise · 4 cancel

Recommended: 1.
