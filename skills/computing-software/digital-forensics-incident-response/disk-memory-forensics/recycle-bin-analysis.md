---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.recycle-bin-analysis
name: recycle-bin-analysis
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [recycle-bin, deleted-files, rbcmd, file-access-evidence, windows-forensics, dfir]
level: practitioner
status: draft
description: "Analyse the Windows Recycle Bin: $I and $R files per user SID, original path, size and deletion time with RBCmd, and recovery of deleted content."
sources: ["https://ericzimmerman.github.io/", "https://www.sans.org/posters/windows-forensic-analysis/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Recycle Bin analysis

**Goal:** determine which files a user deleted via Explorer, when, and from where, and
recover their content if still present.

## Structure (Vista and later)
`<drive>:\$Recycle.Bin\<user SID>\` per volume. Each deletion creates a pair:
- `$I<random>.<ext>`: metadata: version, original **file size**, **deletion time**
  (FILETIME, UTC), original **full path** (v2 in Windows 10+ stores path length then path).
- `$R<random>.<ext>`: the actual file content (or folder) renamed.
Emptying the Recycle Bin deletes both; `$I` may still be recoverable from $MFT/unallocated.

## Parse
```powershell
RBCmd.exe -d "\mount\$Recycle.Bin" --csv \out --csvf recyclebin.csv
RBCmd.exe -f "\mount\$Recycle.Bin\S-1-5-21-...-1001\$IABC123.docx"
```
Map SID folder to user via SOFTWARE `ProfileList`.

## Interpretation
- Shift+Delete, command-line `del`, and most programmatic deletes bypass the Recycle Bin.
- `$R` present means content recoverable directly; hash and export it.
- Deletion of many files at once (e.g. a project folder) right after a resignation notice
  or before device return is a classic insider pattern.
- Removable drives formatted FAT/exFAT have their own `$RECYCLE.BIN`, and network shares
  generally do not use the Recycle Bin.

## Correlate
$UsnJrnl (rename to `$R...` and creation of `$I...` at deletion time), $MFT entries, LNK
files pointing to the original path, shellbags for the original folder.

## Verify
Deletion time from `$I` matches the USN journal rename record for the `$R` file.
