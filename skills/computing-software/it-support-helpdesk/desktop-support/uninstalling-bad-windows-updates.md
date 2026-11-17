---
id: computing-software.it-support-helpdesk.desktop-support.uninstalling-bad-windows-updates
name: uninstalling-bad-windows-updates
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, uninstall-updates-winre, wusa, dism-remove-package, known-issue-rollback, windows-update, boot-failure, patch-rollback, windows-recovery]
level: practitioner
status: gated
description: "Remove a Windows update that broke a PC, from the desktop (wusa / DISM) or WinRE when it won't boot, and stop it reinstalling via pause, hide or ring policy."
sources:
  - "https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/dism-operating-system-package-servicing-command-line-options"
  - "https://learn.microsoft.com/en-us/troubleshoot/windows-client/performance/windows-boot-issues-troubleshooting"
  - "https://learn.microsoft.com/en-us/troubleshoot/windows-server/installing-updates-features-roles/known-issue-rollback"
  - "https://support.microsoft.com/en-us/windows/deployment/install-upgrade/delete-your-previous-version-of-windows"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# uninstalling-bad-windows-updates

Goal: when a cumulative or driver update breaks something, roll back the one
PC fast and stop the fleet from following.

**Back up first.** Removing updates and servicing an offline image can leave
a PC unbootable if interrupted; make sure user data is backed up, and keep the
BitLocker recovery key to hand because WinRE may ask for it.

## Before uninstalling
- Check Windows release health for a known issue. Microsoft's **Known Issue
  Rollback** (KIR) reverts only the faulty change while the rest of the update,
  including its security fixes, stays in place. It is built into Windows
  updates, and managed devices can receive it through Group Policy.
  Uninstalling the whole update, or skipping it, leaves the organisation
  without that update's security fixes.
- Confirm correlation: Settings, Windows Update, Update history, against
  when the symptoms began.

## From a working desktop
List installed packages and remove the specific one with DISM:
```cmd
dism /online /get-packages /format:table
dism /online /remove-package /packagename:<package-name-from-list>
```
Use the exact package name from the list. Removing by KB number with
`wusa /uninstall /kb:<number>` is also commonly used (gated: unconfirmed, source is paywalled or blocked). The
Microsoft reference page for wusa was not readable, so check `wusa /?` on your
build.

## When it will not boot
In WinRE, Troubleshoot, Advanced options, Uninstall Updates (gated: unconfirmed, source is paywalled or blocked).
That menu wording was not on a readable Microsoft page. A BitLocker recovery
key may be requested. The documented offline method for updates that were
installed but not completed is from the WinRE command prompt (use the real
Windows drive letter, which is often not C: in WinRE):
```cmd
DISM /image:<WindowsDrive>\ /get-packages
DISM /image:<WindowsDrive>\ /remove-package /packagename:<name of the package>
DISM /Image:<WindowsDrive>\ /Cleanup-Image /RevertPendingActions
```
If the PC still does not start, Microsoft's boot troubleshooting article
covers renaming `pending.xml` and removing the `pendingxmlidentifier` value
from the offline COMPONENTS hive. Back up the registry before touching it.

## Stop it coming back
- Single PC: pause updates in Settings, Windows Update (gated: unconfirmed, source is paywalled or blocked). The
  maximum pause length was not on a readable page.
- Managed: pause the quality update in your update ring or decline it in
  WSUS for the affected group, and record it in the ticket and problem record
  so the pause is lifted when a fix ships. Never leave a ring paused silently.

## Gotchas
- Ten days after a feature update the previous Windows version is deleted
  automatically, so the rollback window closes.
- Removing a cumulative update removes all the security fixes in it; time-box
  the exception.

## Verify
`dism /online /get-packages` no longer lists the package; the symptom is gone
after a reboot; the pause is in place and the ticket links to a problem or
known-error record.


## Checked

Date 2026-10-27. Documentation release: Microsoft Learn DISM package servicing options, Windows boot troubleshooting and Known Issue Rollback articles, Microsoft Support delete-previous-Windows page, as published October 2026. Confirmed: DISM /Get-Packages /Format:Table and /Remove-Package syntax, WinRE offline /get-packages, /remove-package and /RevertPendingActions steps, pending.xml and pendingxmlidentifier steps, KIR behaviour and delivery by Group Policy, the 10-day removal of the previous Windows version. Gated: wusa, the WinRE Uninstall Updates menu wording and the pause length. Removed: wmic, the combined SSU+LCU claim, Set-OSUninstallWindow, Show or hide updates troubleshooter and driver-policy advice.

Method: documentation only; no commands were run.
