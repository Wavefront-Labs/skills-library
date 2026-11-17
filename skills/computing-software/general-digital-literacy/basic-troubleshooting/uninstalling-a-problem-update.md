---
id: computing-software.general-digital-literacy.basic-troubleshooting.uninstalling-a-problem-update
name: uninstalling-a-problem-update
category: computing-software
field: general-digital-literacy
product: basic-troubleshooting
tags: [basic-troubleshooting, ts-updates, uninstall-update, rollback-update]
level: intro
status: docs-checked
description: "Remove a Windows update that broke something from Update history or from the recovery environment, pause updates, go back after an upgrade within 10 days, and what Mac offers."
sources:
  - https://support.microsoft.com/en-us/windows/deployment/updates-lifecycle/windows-update-faq
  - https://support.microsoft.com/en-us/windows/experience/backup-recovery/recovery-options-in-windows
  - https://support.apple.com/guide/mac-help/reinstall-macos-mchlp1599/mac
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Uninstall a problem update

Microsoft says it does not recommend removing installed updates unless you must, and that not all updates can be removed. Back up important files first, and enable Windows Backup (Settings > Accounts > Windows Backup) to save apps and settings.

## Remove a Windows update
- Settings > Windows Update > **Update history** > **Uninstall updates** > select the update > **Uninstall**. Restart afterwards. Your files and apps are not affected; the changes from that update are removed.
- Windows will not start: in the Windows Recovery Environment (WinRE) choose **Troubleshoot > Advanced options > Uninstall updates**. If BitLocker is on, you need the BitLocker recovery key to use most WinRE options.

## Stop it coming straight back
- **Pause updates** in Settings > Windows Update and pick a length. After the pause limit is reached you must install the latest updates before you can pause again.

## Go back after upgrading to a new Windows version
- If the problem started after upgrading to a new version of Windows, you can try going back to the previous version. It is available for **10 days** after upgrading. Your personal files are kept, but apps, drivers and settings added or changed after the upgrade are removed.
- Other options in Microsoft's recovery article are more disruptive: System Restore (rolls back system files and settings, keeps personal files), Reset this PC (you choose to keep or remove personal files; apps and settings are removed) and a reinstall from installation media. Start with the least disruptive.

## Mac
Software Update installs macOS updates; this guide does not describe uninstalling one. If a macOS install needs repair, macOS Recovery can reinstall macOS, which keeps your files and user settings (internet connection required).

## Verify
- [ ] The problem is gone after restart and the update no longer shows as installed.

## Checked
Checked 2026-10-27 against Microsoft Support "Windows Update: FAQ" and "Recovery options in Windows" and the Apple Mac User Guide "Reinstall macOS". Confirmed: Update history > Uninstall updates path, not-all-updates-removable warning, WinRE Uninstall updates path, pause behaviour, 10-day going-back window and what it keeps, recovery option effects, Mac Recovery reinstall keeping files. Removed unconfirmed claims (wusa command and KB example, Known Issue Rollback, wushowhide tool, Shift-Restart and automatic recovery trigger, "Settings > System > Recovery > Go back" path, 1 to 5 week pause lengths, Apple silicon reinstall version rules).
Method: documentation only; no commands were run.
