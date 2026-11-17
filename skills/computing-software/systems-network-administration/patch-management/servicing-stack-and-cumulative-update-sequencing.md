---
id: computing-software.systems-network-administration.patch-management.servicing-stack-and-cumulative-update-sequencing
name: servicing-stack-and-cumulative-update-sequencing
category: computing-software
field: systems-network-administration
product: patch-management
tags: [ssu-lcu-sequencing, servicing-stack-update, cumulative-update, dism, windows-patch-tooling, patch-management]
level: practitioner
status: docs-checked
description: "Sequence Windows servicing stack updates and cumulative updates: combined SSU+LCU packages, offline image servicing order with DISM, and fixing failures from missing SSUs."
sources:
  - https://learn.microsoft.com/en-us/windows/deployment/update/servicing-stack-updates
  - https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/servicing-the-image-with-windows-updates-sxs
  - https://learn.microsoft.com/en-us/windows/deployment/update/catalog-checkpoint-cumulative-updates
  - https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/dism-operating-system-package-servicing-command-line-options
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Servicing stack and cumulative update sequencing

The **servicing stack update (SSU)** updates the servicing stack, the component that installs Windows updates (it includes component-based servicing, used by DISM and SFC). A prerequisite SSU may occasionally be released out of band; those are classified Security with severity Critical.

## Current state
- Since February 2021 the monthly cumulative update includes the latest servicing stack update (a combined payload for Windows Update, WSUS and the Microsoft Update Catalog), starting on Windows 10 version 2004 and later with KB4601382; deploy the cumulative update and the SSU is applied correctly.
- Windows 11 version 24H2 and later and Windows Server 2025 and later use **checkpoint cumulative updates**: a device or image must take all prior checkpoint cumulative updates before the target update. Windows Update and WSUS handle this seamlessly; Microsoft Update Catalog users must install them in order.
- For older releases that still ship a standalone SSU, read the KB article and install the SSU first.

## Manual install order (online)
```powershell
# Standalone SSU first (older releases), then the cumulative update; or add dependent packages in one DISM command
DISM /Online /Add-Package /PackagePath:"<dir>\<ssu>.msu" /LogPath=<dir>\dism.log
DISM /Online /Add-Package /PackagePath:"<dir>\<cumulative-update>.msu" /LogPath=<dir>\dism.log
```
For packages with dependencies, either install them in order or add them all at once with a single DISM command (multiple `/PackagePath` arguments). A combined package needs one step.

## Offline image servicing (golden images, WIM)
Add packages to the mounted image with `DISM /Image:<mount> /Add-Package /PackagePath:<file>`, in dependency order (SSU if separate, then checkpoint cumulative updates in order, then the latest cumulative update) or all in one command. If you add an update to an offline image after it was applied to a target device, re-run BCDBoot so updated boot files reach the system partition. Verify with `DISM /Image:<mount> /Get-Packages`. For WinRE, .NET and component cleanup steps (`/Cleanup-Image /StartComponentCleanup`), follow Microsoft's current image servicing guidance for your release.

## Troubleshooting
- `DISM /Online /Get-Packages` lists installed packages (use `/Format:Table` for a table); filter the output for servicing stack entries.
- The CBS log under `%windir%\Logs\CBS` records servicing failures and prerequisites.

## Gotchas
- Checkpoint LCUs: a post-checkpoint LCU can be applied to images or devices on that checkpoint or on a later LCU; images that are older need the earlier checkpoint updates first when you service them from the catalog.

## Verify
The LCU installs without errors, `winver` shows the target build, and images are rebuilt in dependency order.

## Checked

Checked 2026-10-27 against Microsoft Learn: Servicing stack updates (updated 2026-02-11), Checkpoint cumulative updates and Microsoft Update Catalog usage, DISM image servicing with Windows Updates, and DISM package-servicing options.
- Combined SSU in the cumulative update since February 2021 (Windows 10 2004 and later, KB4601382); out-of-band SSUs classified Security/Critical: confirmed.
- Checkpoint cumulative updates (Windows 11 24H2 and later, Windows Server 2025 and later) and the prior-checkpoint rule: confirmed.
- DISM `/Add-Package` ordering or single command, BCDBoot note, `/Get-Packages` and `/Format:Table`: confirmed.
- Removed unconfirmed: error codes 0x800f0922 and 0x800f081f, the wusa switches, the full offline ordering with .NET and ResetBase, the WinRE Safe OS step, "SSUs cannot be uninstalled", WSUS SSU decline advice, the older-OS statement about separate SSUs.
Method: documentation only; no commands were run.
