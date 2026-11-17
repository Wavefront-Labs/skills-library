---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.usn-journal-deletion-and-fsutil-abuse
name: usn-journal-deletion-and-fsutil-abuse
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [usn-journal-deletion, anti-forensics, usnjrnl, ntfs, dfir]
level: advanced
status: docs-checked
description: "Detect deletion or tampering of the NTFS USN change journal (fsutil usn deletejournal), interpret the gap, and carve journal records from unallocated space."
sources: ["https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/fsutil-usn", "https://attack.mitre.org/techniques/T1070/", "https://github.com/PoorBillionaire/USN-Record-Carver"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# USN journal deletion and fsutil abuse

**Goal:** attackers can remove file-activity history by deleting the NTFS USN change journal (ATT&CK T1070, Indicator Removal).
The deletion is itself evidence, and old records can remain in unallocated space.

## What the journal is (fsutil usn)
The USN change journal is a persistent per-volume log of changes to files: NTFS appends a record for each add, delete or modify,
indicating the type of change and the object. Indexing Service, FRS, RIS and Remote Storage use it.

## How it is done
```cmd
fsutil usn deletejournal /d C:
fsutil usn deletejournal /n C:
fsutil usn createjournal m=<maxsize> a=<allocationdelta> C:
fsutil usn queryjournal C:
```
- `deletejournal` deletes or disables an active journal. `/d` disables it and returns I/O control while the disable proceeds;
  `/n` disables it and returns I/O control only after it is disabled. Neither switch is documented as recreating the journal:
  recreation is a separate `createjournal` call.
- `createjournal` on an existing journal only updates its `m=` (maximum size, bytes) and `a=` (allocation delta, bytes).
- `queryjournal` gathers data about the current journal, its records and its capacity.
- Disabling a journal is slow because the system must visit every MFT record and set its last USN attribute to 0; it can take
  minutes and continue after a restart. Meanwhile journal operations return errors, and FRS and the Indexing Service must rescan
  the volume afterwards. This side effect is a possible signal in service or replication logs.

## Detection
- Process creation of `fsutil.exe` with `usn deletejournal` in the command line (command-line auditing or EDR process telemetry).
- A journal whose earliest records are much later than the volume's history would suggest, or whose coverage is far shorter than
  its configured size implies, indicates deletion or recreation. Know the normal coverage for the host: the journal is
  trimmed at NTFS checkpoints once it exceeds maxsize plus allocationdelta, so busy volumes wrap naturally.
- Cross-check other NTFS artefacts (MFT, log file) for activity the journal no longer shows.

## Recovery
- As the journal reaches its maximum size, clusters are marked unallocated, so USN records often survive in unallocated space.
  The USN-Record-Carver script carves NTFS USN records from raw/dd input (`python usncarve.py -f file.raw -o usn.raw`) and writes
  them in binary form for a parser of your choice.
- Older copies of the journal may exist in volume shadow copies (not covered by the cited pages).

## Verify
State what evidence shows the deleting process, how the journal's coverage differs from expectation, and what was recovered by
carving.

## Checked
Date: 2026-11-08.
Confirmed in fsutil-usn: syntax, `/d` versus `/n`, `m=` and `a=`, truncation rule, MFT/last-USN reset cost, FRS and Indexing
Service impact, services that use the journal. Confirmed in the USN-Record-Carver README: carving from raw/dd input and the
`usncarve.py -f ... -o ...` usage. Confirmed in T1070: technique name and sub-technique list.
Corrected: `/n` does not "delete, then recreate empty"; the carver script is `usncarve.py`.
Removed (not on the cited pages): `$UsnJrnl:$Max` journal-ID FILETIME heuristic, Prefetch name, event IDs, USN_RECORD version
signatures, the MFTECmd step, the sparse-`$J` statement, and the createjournal `m=... a=...` placeholders replaced by the
documented ones.
Method: docs-only read of cited pages, 2026-11-08
