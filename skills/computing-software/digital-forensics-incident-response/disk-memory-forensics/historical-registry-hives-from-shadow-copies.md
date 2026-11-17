---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.historical-registry-hives-from-shadow-copies
name: historical-registry-hives-from-shadow-copies
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [historical-hives, volume-shadow-copy, windows-registry, registry, dfir]
level: advanced
status: draft
description: "Extract historical registry hives from shadow copies and RegBack, diff them against current hives to date when persistence or settings changed."
sources: ["https://github.com/libyal/libvshadow", "https://ericzimmerman.github.io/", "https://learn.microsoft.com/en-us/troubleshoot/windows-client/installing-updates-features-roles/system-registry-no-backed-up-regback-folder"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Historical registry hives from shadow copies

**Goal:** a key last-write time only shows the latest change. Older copies of the same hive let
you bracket when a value first appeared or was deleted.

## Sources of old hives
| Source | Notes |
|---|---|
| Volume shadow copies | Each store has `Windows\System32\config\SYSTEM`, `SOFTWARE`, `SAM`, `SECURITY` and user `NTUSER.DAT`/`UsrClass.dat` as of its creation time |
| `Windows\System32\config\RegBack\` | Backup copies; disabled by default since Windows 10 1803 (files 0 bytes) unless `EnablePeriodicBackup` set |
| Transaction logs (.LOG1/.LOG2) | Recent pending changes, not a full history |
| Hive slack / deleted keys | Old values recoverable from unallocated cells |

## Extract
```bash
vshadowmount -o <offset> image.dd /mnt/vss
for s in /mnt/vss/vss*; do n=$(basename $s); mkdir -p /mnt/$n; mount -o ro,loop,show_sys_files $s /mnt/$n
  cp /mnt/$n/Windows/System32/config/{SYSTEM,SOFTWARE} hives/$n/ 2>/dev/null; done
```
Or KAPE with `--vss` and target `RegistryHives`.

## Diff
- Run the same RECmd batch over every copy and compare CSV output keyed on KeyPath+ValueName.
- Registry Explorer can compare two hives (or use `regdiff`-style scripts).
- Typical questions: when did the malicious Run value / service / IFEO appear? When was a USB device first seen in older hives (USBSTOR history beyond current)? Which user accounts existed before deletion (SAM)?

## Gotchas
- Each VSS hive may itself be dirty; include its LOG files from the same VSS.
- VSS creation time brackets: a value absent in VSS(t1) and present in VSS(t2) was added between t1 and t2.

## Verify
Bracketed times are stated with the VSS creation times used as bounds.
