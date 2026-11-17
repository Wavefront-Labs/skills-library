---
id: computing-software.systems-network-administration.patch-management.patch-uninstall-and-rollback-verification
name: patch-uninstall-and-rollback-verification
category: computing-software
field: systems-network-administration
product: patch-management
tags: [patch-uninstall, wusa-uninstall, rollback-plan, dism, dnf-history-undo, patch-testing]
level: practitioner
status: docs-checked
description: "Prove a patch can be removed before you need to: Windows LCU removal with DISM, Linux downgrade paths, what cannot be uninstalled, and testing rollback in pilot."
sources:
  - https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/dism-operating-system-package-servicing-command-line-options
  - https://dnf.readthedocs.io/en/latest/command_ref.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Patch uninstall and rollback verification

A rollback plan that was never tested is a hope. Test removal on a pilot machine each cycle
for high-risk updates.

## Windows
`wusa /uninstall /kb:<KB_NUMBER>` works for many standalone updates but a servicing stack
update part of a combined package is permanent. Remove the cumulative update package with DISM:
```powershell
dism /online /get-packages /format:table
dism /online /remove-package /packagename:<PACKAGE_NAME> /norestart
```
Then reboot and confirm the build with `winver`.
Block reinstallation while investigating: pause updates or decline/expire in WSUS,
WUfB pause, or ConfigMgr deployment disabled.

Not removable: servicing stack updates, some .NET and firmware updates, a feature update
after its rollback window has passed, updates whose superseding update is installed.

## Linux
```sh
dnf history list openssl
dnf history undo <id>          # reverts the transaction (needs old packages available in repos/cache)
dnf downgrade openssl          # lower version, or give a target version
```
Kernel: keep the previous kernel installed and boot it from the boot menu.
Old versions must still be available: dated repo snapshots or local package caches.

## VM-level rollback
Snapshot before patching (short-lived) gives a fast rollback but loses data written since;
OK for stateless servers, risky for databases.

## Test procedure (pilot ring)
1. Patch the pilot VM, record build/versions.
2. Remove the update with the method above, reboot.
3. Confirm versions reverted and the app works.
4. Document the exact commands and timings in the change's backout plan.

## Checked
2026-11-01. Confirmed: DISM `/Get-Packages /Format` and `/Remove-Package /PackageName` (Learn DISM package servicing page); `dnf history list|undo` and `dnf downgrade` (DNF command reference). Removed: specific KB, package names and versions, 10-day rollback window, `Get-OSUninstallWindow`, apt pin syntax, `grubby`, `keepcache`, cache paths, OS-version claims.
Method: documentation only; no commands were run.

## Verify
Backout plan in each high-risk change references a test run with date and result.
