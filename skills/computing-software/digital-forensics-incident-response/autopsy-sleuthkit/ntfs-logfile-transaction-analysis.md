---
id: computing-software.digital-forensics-incident-response.autopsy-sleuthkit.ntfs-logfile-transaction-analysis
name: ntfs-logfile-transaction-analysis
category: computing-software
field: digital-forensics-incident-response
product: autopsy-sleuthkit
tags: [ntfs-logfile, logfile, ntfs, lfs, logfileparser, file-operations, timestomping, dfir]
level: advanced
status: draft
description: "Parse the NTFS $LogFile to recover recent file creates, renames, deletes and attribute changes, including timestomping, beyond what $MFT and $UsnJrnl show."
sources: ["https://github.com/jschicht/LogFileParser", "https://flatcap.github.io/linux-ntfs/ntfs/files/logfile.html", "https://www.sans.org/posters/windows-forensic-analysis/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# $LogFile transaction analysis

**Goal:** use the NTFS transaction journal to see the last few minutes to hours of metadata
operations at a granularity the USN journal does not provide (old and new attribute values).

## What it is
`$LogFile` (MFT record 2, default 64 MiB) is the redo/undo log NTFS uses for crash
recovery. Each LSN record has redo and undo operations (e.g. `InitializeFileRecordSegment`,
`UpdateResidentValue`, `AddIndexEntryAllocation`, `DeleteAttribute`) with the bytes changed.
Because it is circular and busy, it covers a short window: minutes on a busy system drive,
longer on quiet data volumes.

## Extract and parse
```bash
icat image.E01 2 > LogFile.bin                 # TSK, offset with -o if partitioned
# Windows: KAPE/RawCopy to collect $LogFile from a live volume
LogFileParser.exe   # (jschicht) select LogFile.bin + $MFT; outputs CSVs and an SQLite db
```
Other parsers: `NTFS Log Tracker`, `dfir_ntfs` (`ntfs_parser --log`), commercial suites.

## What you get that $J does not
- **Old and new values** of `$STANDARD_INFORMATION`: timestomping shows as an update to $SI
  timestamps with the prior (real) values in the undo data.
- Resident data changes (small file contents before and after a write).
- Index entry adds/removes: directory listing changes, including files that existed only
  briefly.
- Rename sequences with both names in one transaction.

## Workflow
1. Parse with the matching `$MFT` so record numbers resolve to paths.
2. Filter on files of interest or on the incident window.
3. Correlate LSNs with `$J` USN entries (both carry record numbers and sequence numbers) to
   build an ordered sequence of operations.
4. Report what changed, previous values, and the transaction order.

## Gotchas
- Short retention: collect it early; every hour of system activity on a live box overwrites it.
- Timestamps are not stored per LSN record; ordering comes from LSNs, times from the values
  being written or correlated `$J` entries.
- Parsing tools vary in maturity; validate key findings with a second tool or with `$J`/`$MFT`.

## Self-check
For each finding you can cite the LSN, the operation, the record number/path and, where
relevant, the before and after values.
