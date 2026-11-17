---
id: computing-software.it-support-helpdesk.desktop-support.windows-in-place-upgrade-and-repair-install
name: windows-in-place-upgrade-and-repair-install
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, windows-upgrade, in-place-upgrade, repair-install, setup-exe, setupdiag, compat-scan, panther-logs, windows-installation, comptia-a-plus]
level: practitioner
status: docs-checked
description: "Run a Windows in-place upgrade or keep-everything repair install, pre-check with /compat scanonly, and read SetupDiag/Panther logs when setup rolls back."
sources:
  - "https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/windows-setup-command-line-options"
  - "https://learn.microsoft.com/en-us/windows/deployment/upgrade/setupdiag"
  - "https://learn.microsoft.com/en-us/troubleshoot/windows-client/setup-upgrade-and-drivers/windows-10-upgrade-error-codes"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# windows-in-place-upgrade-and-repair-install

Goal: move a PC to a newer Windows version, or rebuild a broken OS in place,
while keeping apps, data and settings, and diagnose a rollback without
guessing.

**Back up first.** An in-place upgrade can fail and roll back, and any
servicing step can go wrong. Back up user data and keep the BitLocker
recovery key before starting.

## When a repair install is the right tool
After `sfc /scannow` and `DISM /Online /Cleanup-Image /RestoreHealth` fail
and the symptom is OS-wide but the profile and apps are fine. A reimage costs
a day of app reinstall and data restore; a repair install replaces system
files in place.

## Run it
Mount an ISO of the Windows version you are installing.
```cmd
:: compatibility dry run only; the exit code reports the result
<ISO>\setup.exe /auto upgrade /quiet /compat scanonly
echo %errorlevel%
:: 0xC1900210 = no compatibility concerns found
:: 0xC1900208 = actionable compatibility issues (for example apps)
:: 0xC1900204 = the selected migration choice is not available

:: real run: upgrade, take Dynamic Update, skip OOBE, accept EULA
<ISO>\setup.exe /auto upgrade /dynamicupdate enable /showoobe none /eula accept
```
BitLocker: setup's default (`/BitLocker TryKeepActive`) attempts the upgrade
without suspending BitLocker and, if that fails, suspends it and completes.
`AlwaysSuspend` always suspends; `ForceKeepActive` fails the upgrade if
BitLocker is active. Check `manage-bde -status` afterwards.

## When it rolls back
- Run **SetupDiag** (a separate Microsoft tool; its default results file is
  `%windir%\logs\SetupDiag\SetupDiagResults.xml`, or choose a location with
  `/Output:`). It analyses the setup logs and names the matching rule.
- Error codes have a result code plus an extend code, for example
  `0xC1900101 - 0x4000D`. The result code `0xC1900101` is generic and means a
  rollback occurred; in most cases the cause is a driver compatibility issue.
  The extend code gives the Setup phase (first digits) and the operation that
  was running (last digits); Microsoft's upgrade error-code article has the
  tables. Disk-full style result codes mean more space is needed.

## Gotchas
- Managed devices: Windows Update for Business or an Intune feature update
  policy may block or re-offer a different target version; coordinate with the
  ring.
- Keep the old OS recoverable: after a feature update the previous version
  is removed after ten days.

## Verify
`winver` shows the expected build, the user signs in to their existing
profile with apps intact, and BitLocker protection is on.


## Checked

Date 2026-10-27. Documentation release: Microsoft Learn Windows Setup command-line options, SetupDiag and Windows upgrade error-code pages, as published October 2026. Confirmed: /auto upgrade, /compat scanonly with exit codes 0xC1900210, 0xC1900208 and 0xC1900204, /dynamicupdate Enable, /showoobe None, /eula accept, /BitLocker options and default, SetupDiag /Output and default results path, result code plus extend code structure and the 0xC1900101 meaning. Removed: /noreboot with scanonly, 20 GB and USB-disconnect advice, edition-mismatch claims, Panther and Rollback log paths, 0x800F0922 meaning, repair-install timing and hardening notes that no page covers.

Method: documentation only; no commands were run.
