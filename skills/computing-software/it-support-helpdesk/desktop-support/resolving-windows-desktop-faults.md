---
id: computing-software.it-support-helpdesk.desktop-support.resolving-windows-desktop-faults
name: resolving-windows-desktop-faults
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, windows-10, windows-11, sfc, dism, event-viewer, reliability-monitor, safe-mode, clean-boot, msconfig, user-profile, profilelist, temporary-profile, office-repair, microsoft-365-apps, credential-manager, cmdkey, print-spooler, ipconfig, netsh, winsock-reset, driver-rollback, chkdsk, gpupdate, gpresult, winget, bsod, minidump, windbg]
level: practitioner
status: docs-checked
description: "Windows 10/11 desktop fixes with documented switches: DISM, SFC, msconfig clean start, ipconfig, winsock reset, chkdsk, gpupdate, gpresult, winget, cmdkey."
sources:
  - https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/repair-a-windows-image
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/sfc
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/ipconfig
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/netsh-winsock
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/chkdsk
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/gpupdate
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/gpresult
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/cmdkey
  - https://learn.microsoft.com/en-us/windows/package-manager/winget/upgrade
  - https://learn.microsoft.com/en-us/windows/client-management/advanced-troubleshooting-boot-problems
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resolving Windows desktop faults

**Goal:** apply standard L1/L2 repairs for Windows 10/11 with evidence before and after. Run
commands from an **elevated** prompt (sfc and chkdsk require administrator rights). Method for
choosing *which* fix: see
computing-software.it-support-helpdesk.troubleshooting-methodology.systematic-problem-isolation.

## 1. Read the evidence first
- **Event Viewer** (`eventvwr.msc`): Event ID 41 is the "system has rebooted without cleanly
  shutting down first" event. After a failed boot, try Safe Mode or Safe Mode with Networking;
  if one works, use Event Viewer to find the cause.

## 2. System file and image repair
```
Dism /Online /Cleanup-Image /ScanHealth
Dism /Online /Cleanup-Image /CheckHealth
Dism /Online /Cleanup-Image /RestoreHealth
sfc /scannow
```
- `sfc /scannow` is the quick check of protected system files; `DISM /Cleanup-Image` is the
  more extensive check that can repair the component store. `/CheckHealth` reports whether the
  image is healthy, repairable or non-repairable.
- `sfc /verifyonly` scans without repairing; `/scanfile=<file>` and `/verifyfile=<file>` target
  one file.
- With no `/Source`, DISM uses the Features on Demand repair source (set by Group Policy).
  `/Source:<path>` adds a source, and `/LimitAccess` stops DISM using Windows Update.

## 3. Clean start
Use `msconfig` and choose Selective startup to test services one at a time; Microsoft notes
the problem service is most often third-party.

## 4. Stale credentials
`cmdkey /list` shows stored credentials; `cmdkey /delete:<TARGET>` removes one entry.

## 5. Network stack
```
ipconfig /release
ipconfig /renew
ipconfig /flushdns
netsh winsock reset
```
- `/release` discards the DHCP configuration and disables TCP/IP on adapters set to obtain an
  address automatically; `/renew` asks DHCP for a new one.
- `/flushdns` clears the DNS resolver cache, including negative entries.
- `netsh winsock reset` resets the Winsock catalog, removing custom LSPs; it does not touch
  Name Space Provider entries.

## 6. Disk
- `chkdsk <VOLUME>: /scan` is an online scan (NTFS only). `/f` fixes errors and needs the
  disk locked; if it cannot lock the drive it offers to check at the next restart. `/r` adds
  bad-sector recovery and includes `/f`.
- Without parameters chkdsk only reports status and fixes nothing.

## 7. Policy and apps
- `gpupdate /force` reapplies all policy settings (by default only changed ones apply).
- `gpresult /r` gives an RSoP summary; `gpresult /h <FILE>` writes an HTML report;
  `/scope user` or `/scope computer` limits it.
- `winget upgrade` with no arguments previews upgrades; `winget upgrade --id <PACKAGE_ID>`
  upgrades one; `winget upgrade --all` upgrades everything with an update (pinned packages
  are skipped unless `--include-pinned`).

## Gotchas
- Interrupting chkdsk is not recommended, though it should not leave the volume worse.
- `ipconfig /release` drops connectivity on that adapter until `/renew` succeeds.

## Verify
- [ ] `sfc /scannow` reports no integrity violations.
- [ ] Re-run the exact test that originally failed.
- [ ] Ticket records commands run and their output.

## Checked
2026-11-01. Confirmed against the Microsoft Learn pages in `sources`: DISM ScanHealth,
CheckHealth, RestoreHealth, /Source, /LimitAccess; sfc switches; ipconfig switches and
effects; winsock reset; chkdsk switches; gpupdate and gpresult switches; cmdkey list/delete;
winget upgrade options; Event ID 41 wording, Safe Mode and msconfig selective startup
(boot-problems page). Removed (no page read): Reliability Monitor, other event IDs, log file
paths, ProfileList and temporary-profile repair, Microsoft 365 repair, print spooler reset,
`netsh int ip reset`, Network reset, driver rollback, WinDbg and minidump steps, and the
DISM-before-SFC rationale.
Method: documentation only; no commands were run.
