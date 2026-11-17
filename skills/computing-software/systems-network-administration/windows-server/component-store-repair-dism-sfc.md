---
id: computing-software.systems-network-administration.windows-server.component-store-repair-dism-sfc
name: component-store-repair-dism-sfc
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, servicing, dism-restorehealth, sfc-scannow, component-store, winsxs, cbs-log, repair-windowsimage, limitaccess, source-wim, analyzecomponentstore]
level: practitioner
status: docs-checked
description: "Repair a corrupted component store and system files: DISM ScanHealth/RestoreHealth with a matching source, SFC afterwards, reading CBS.log, and cleanup."
sources:
  - https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/repair-a-windows-image
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/installing-updates-features-roles/fix-windows-update-errors
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Component store repair (DISM + SFC)

**Symptoms:** updates fail with `0x800f081f` (CBS_E_SOURCE_MISSING, the source for the package or file was not found).

## Order: DISM first, then SFC
Repair the component store with DISM, then run SFC.
```cmd
DISM /Online /Cleanup-Image /ScanHealth          :: detects (slow)
DISM /Online /Cleanup-Image /RestoreHealth       :: repairs
sfc /scannow
```
PowerShell: `Repair-WindowsImage -Online -RestoreHealth`.

## When RestoreHealth cannot download
Point it at a repair source; `/LimitAccess` stops DISM using Windows Update as a repair source.
```cmd
DISM /Online /Cleanup-Image /RestoreHealth /Source:<SOURCE_PATH> /LimitAccess
```
- A source can be a mounted image path or a healthy server's `\\<servername>\c$\windows`.

## Logs
If SFC or DISM fails, analyze `CBS.log` and fix the errors it names.

## Cleanup
```cmd
DISM /Online /Cleanup-Image /StartComponentCleanup
```

## Verify
- [ ] `ScanHealth` reports no corruption.
- [ ] `sfc /scannow` finds no integrity violations (or repaired all).
- [ ] The previously failing update installs.

## Checked
2026-10-28: Confirmed on Learn pages repair-a-windows-image and fix-windows-update-errors: ScanHealth, RestoreHealth, /Source, /LimitAccess, `\\<servername>\c$\windows` source, `sfc /scannow`, StartComponentCleanup, CBS.log, 0x800F081F = CBS_E_SOURCE_MISSING. Removed: other error codes, WIM index example, GPO alternate source, log search strings, AnalyzeComponentStore, exact success messages.
Method: documentation only; no commands were run.
