---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.registry-hive-forensics-and-deleted-key-recovery
name: registry-hive-forensics-and-deleted-key-recovery
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [windows-registry, registry-hive, regf, regripper, transaction-log, log1, log2, hive-recovery, deleted-registry-key, registry-explorer, autoruns, run-keys, services-registry, uac, persistence, dfir, windows-forensics]
level: advanced
status: draft
description: "Parse Windows registry hives directly with RegRipper/Registry Explorer, replay transaction logs for unsaved changes, and recover deleted keys from unallocated hive cells."
sources: ["https://github.com/keydet89/RegRipper3.0", "https://binaryforay.blogspot.com/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Registry hive forensics and deleted key recovery

**Goal:** go beyond the artefact list a super-timeline gives you (see
computing-software.digital-forensics-incident-response.disk-memory-forensics.super-timeline-with-plaso)
and read registry hives directly when you need a key the standard parsers don't surface,
when the hive is dirty (crash, unexpected shutdown) and the on-disk copy is stale, or
when a key was deleted and might still be recoverable.

## 1. Which hive, which path
- `SYSTEM`, `SOFTWARE`, `SAM`, `SECURITY`, `DEFAULT` live in `%WINDIR%\System32\config\`.
- `NTUSER.DAT` is per-user, in the profile root; `UsrClass.dat` (per-user
  shell/COM/BAM data) is in `AppData\Local\Microsoft\Windows\`.
- Pull hives from a mounted/live image with TSK's `icat`, not from a running system —
  a live hive is locked and an in-use copy can be internally inconsistent mid-write.

## 2. Transaction logs — don't skip this
Modern Windows registry hives are **not always fully flushed to the primary hive file**.
`SYSTEM.LOG1`/`SYSTEM.LOG2` (or `SYSTEM{GUID}.TM.blf` + regtrans-ms files on newer
builds) hold pending transactions not yet committed to `SYSTEM`. If you parse the hive
file alone after an unclean shutdown you can miss the most recent changes — exactly the
ones an incident responder cares about. Tools: `RegRipper` with the `-l`/log-aware mode
version 3+ auto-detects and replays logs; `Eric Zimmerman's Registry Explorer` has a
built-in "Apply Logs" function that merges log entries into a live view without
modifying the source file. Always replay logs before concluding a key or value is
absent.

## 3. Parsing and known-good plugins
- `RegRipper` runs targeted plugins per hive (`rip.exe -r SYSTEM -p shimcache`,
  `-p services`, `-p runmru`, etc.) and is the fastest path to the well-known
  persistence/execution locations: `Run`/`RunOnce` keys, `Services`, `AppInit_DLLs`,
  `Image File Execution Options` (Debugger value = classic persistence/hijack),
  `Winlogon\Shell`/`Userinit`.
- `Registry Explorer` (GUI) is better for free-browsing and for viewing a key's
  **last-written timestamp** — every registry key (not value) has one, and it's an
  independent timeline source from file-system MACB times; a key's last-written time
  changing with no corresponding legitimate admin action is itself a finding.
- UAC bypass and persistence hunting both live mostly in `SOFTWARE\Microsoft\Windows\
  CurrentVersion\Run*`, `SYSTEM\CurrentControlSet\Services`, and COM hijack locations
  under `SOFTWARE\Classes\CLSID`; cross-reference findings against Sysinternals
  Autoruns' own registry-location list if something looks persistent but doesn't match
  a documented key.

## 4. Deleted key recovery
A deleted registry key's cell isn't zeroed immediately — it's marked free in the hive's
internal allocator and can survive until that space is reused. `Registry Explorer`'s
"Find deleted keys/values" scans unallocated cells in the hive bin structure and can
recover a deleted key's name, values and last-written time if not yet overwritten.
Treat recovered deleted-key data the same way as file-carving output (see
computing-software.digital-forensics-incident-response.autopsy-sleuthkit.file-carving-and-unallocated-space-recovery):
real but with no guarantee of completeness, and note in the report that it came from
unallocated hive space, not the live registry tree.

## Verify
- Confirm you replayed `.LOG1`/`.LOG2`/regtrans-ms files before citing the absence of a
  key or value — an un-replayed hive can be hours stale.
- Cross-check a RegRipper persistence finding against Autoruns' documented location
  list and, where possible, against the super-timeline for a corresponding execution
  artefact (prefetch/Amcache) at the same time.
- Label any deleted-key recovery as coming from unallocated hive space in the report.

Unconfirmed: exact regtrans-ms replay behaviour differs between Windows 10 builds —
verify against a build-matched test hive before relying on it for a legal deliverable.
