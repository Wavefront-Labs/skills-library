---
id: computing-software.cybersecurity-defensive.security-operations.ntfs-mft-and-usn-journal-analysis
name: ntfs-mft-and-usn-journal-analysis
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [digital-forensics, ntfs-mft-analysis, mft, usn-journal, mftecmd, timestomping, file-system-forensics, si-vs-fn]
level: advanced
status: docs-checked
description: "Analyse NTFS $MFT and $UsnJrnl:$J with MFTECmd: file creation timelines, $SI vs $FN timestamps to spot timestomping, deleted files, and renames that reveal attacker staging."
sources: ["https://github.com/EricZimmerman/MFTECmd", "https://learn.microsoft.com/en-us/windows/win32/fileio/change-journals", "https://learn.microsoft.com/en-us/windows/win32/api/winioctl/ns-winioctl-usn_record_v2", "https://learn.microsoft.com/en-us/windows/win32/fileio/creating-modifying-and-deleting-a-change-journal"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NTFS $MFT and USN journal analysis

## Collect
From a triage collection or an image: `$MFT`, `$LogFile`, `$Extend\$UsnJrnl:$J`, `$Boot`. These are
locked on a live system; MFTECmd reads locked files and Volume Shadow Copies (`--vss`) through raw disk access, so use
raw-copy capable tools, not Explorer copy.

## Parse with MFTECmd
```
MFTECmd.exe -f "<evidence>\$MFT" --csv out --csvf mft.csv
MFTECmd.exe -f "<evidence>\$J" -m "<evidence>\$MFT" --csv out --csvf usn.csv   # resolves parent paths
MFTECmd.exe -f "<evidence>\$MFT" --de 0x1234                                    # dump one entry
```
`-m` supplies the `$MFT` used to resolve parent paths for a `$J` (or `$LogFile`); use the `$MFT` and `$J` of the same
volume collected at the same time. Without `-m`, ParentPath is empty. `--de` takes `Entry` or `Entry-Seq`, decimal or
hex. Filter the CSVs by path, extension and time window (`--cutoff` limits `$MFT` records by $SI created/modified time).

## $SI vs $FN timestamps
Each file record carries timestamps in two attributes: `$STANDARD_INFORMATION` (0x10, $SI) and `$FILE_NAME`
(0x30, $FN). By default MFTECmd shows the 0x30 timestamps only when they differ from the 0x10 ones; `--at` includes
all of them, so differences between the two sets are visible. Indicators to look for:
- `SI Created < FN Created` (file claims to be older than its name record).
- $SI timestamps with zero sub-second precision (`.0000000`) while neighbours have full precision.
- Executable in a user temp folder "created" years before the OS install date.
- For `$LogFile`, MFTECmd (2026.10 and later) decodes `$STANDARD_INFORMATION` timestamp changes (time stomping) with their previous values.

## USN journal ($J)
NTFS keeps an update sequence number (USN) change journal per volume, updated with a description of each change.
Reason flags include `USN_REASON_FILE_CREATE`, `DATA_EXTEND`, `RENAME_OLD_NAME`/`RENAME_NEW_NAME`,
`FILE_DELETE` and `SECURITY_CHANGE`. Useful for:
- Attacker staging: an archive created, many data extends, then a delete (exfil and cleanup).
- Renames: the old-name and new-name records show both names.
- Short-lived files: created and deleted between collections; the MFT entry may have been reused while the journal
  record can remain.
The journal has a target maximum size and is trimmed at NTFS checkpoints once it exceeds MaximumSize plus
AllocationDelta, so old records age out; collect it early. With `-m`, MFTECmd resolves each record's parent path as
it was when the record was written (the journal is "rewound" through renames and deletions).

## Deleted files
MFT entries not in use may keep name, size and timestamps until reused. `--dr` dumps resident files from the `$MFT`
and `--ir` includes resident data in CSV/JSON, so small files can be recovered from the record itself.

## Gotchas
- MFTECmd JSON output uses ISO 8601 UTC timestamps. Keep everything UTC.
- Volume shadow copies may hold older $MFT/$J versions; `--vss` processes them and `--dedupe` drops duplicates by SHA-1.
- Entry sequence numbers matter when an entry was reused; match on entry + sequence.
- Exit code 1 means the tool failed; damaged records are skipped and reported, and the rest is still processed.

## Verify
Pick a known event (e.g. a tool the attacker dropped per EDR) and confirm its create time and path
agree across $MFT, $J and EDR telemetry; discrepancies point to timestomping or clock issues.

## Checked
Checked 2026-11-08 against the MFTECmd README (options -f -m --csv --csvf --de --at --vss --dedupe --dr --ir --cutoff,
$J path rewinding, $LogFile time stomp decoding, output formats, exit codes) and Microsoft Learn: Change Journals,
USN_RECORD_V2 (reason constants), Creating, Modifying, and Deleting a Change Journal (MaximumSize trimming). Removed
because not on those pages: KAPE and Velociraptor target names, Timeline Explorer, the claim that MFTECmd flags
timestomping, the 32 MB to hundreds of MB journal sizes, and the SANS poster source (page only a listing). The claims about which
attribute user-mode APIs can change were dropped as unconfirmed.
Method: documentation only; no commands were run.
