---
id: computing-software.systems-network-administration.windows-server.remove-bad-update-from-winre
name: remove-bad-update-from-winre
category: computing-software
field: systems-network-administration
product: windows-server
tags: [boot-troubleshooting, winre-uninstall-update, dism-remove-package, update-failures, pending-reboot]
level: advanced
status: docs-checked
description: "Recover a server that fails to boot after an update: DISM /Image /Get-Packages and /Remove-Package from WinRE, and /Cleanup-Image /RevertPendingActions."
sources:
  - https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/dism-operating-system-package-servicing-command-line-options
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Removing a bad update or driver from WinRE

## DISM against the offline image
Find the Windows drive letter in WinRE first (`dir <letter>:\Windows` for each candidate letter). Then:
```cmd
dism /Image:<WinDrive>\ /Get-Packages /Format:Table | more
dism /Image:<WinDrive>\ /Remove-Package /PackageName:<PackageName>
```
Take `<PackageName>` from the `/Get-Packages` output.

## Stuck in "Undoing changes" / boot loop with pending actions
```cmd
dism /Image:<WinDrive>\ /Cleanup-Image /RevertPendingActions
```
Then boot normally and retry the update.

## After recovery
- Pause the offending update via WSUS/Update policy until the vendor/Microsoft fixes it; check release health known
  issues.

## Verify
- [ ] Server boots; `dism /Online /Get-Packages` no longer lists the removed package; update deferral in place.

## Checked

2026-10-28. Confirmed against: DISM operating system package servicing options (/Image, /Get-Packages /Format:Table, /Remove-Package /PackageName, /Cleanup-Image /RevertPendingActions). Removed (not confirmable from the cited pages): WinRE Uninstall Updates menu path, example package name, InstallTime column, pending.xml advice, driver removal commands, CBS.log/setupapi.dev.log, Get-HotFix.

Method: documentation only; no commands were run.
