---
id: computing-software.it-support-helpdesk.desktop-support.using-windows-recovery-environment
name: using-windows-recovery-environment
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, winre, windows-recovery, boot-failure, startup-repair, safe-mode, reagentc, recovery-environment, comptia-a-plus]
level: practitioner
status: docs-checked
description: "Get into Windows RE on a PC that won't boot, pick the right tool (Startup Repair, Safe Mode, command prompt, System Restore, uninstall update) and handle the BitLocker key prompt."
sources:
  - "https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/windows-recovery-environment--windows-re--technical-reference"
  - "https://learn.microsoft.com/en-us/troubleshoot/windows-client/performance/windows-boot-issues-troubleshooting"
  - "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/shutdown"
  - "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/sfc"
  - "https://learn.microsoft.com/en-us/windows/security/operating-system-security/data-protection/bitlocker/recovery-overview"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# using-windows-recovery-environment

Goal: from a PC stuck at a spinner, boot loop or "Automatic Repair couldn't
repair your PC", get to a working desktop with the least destructive tool.

**Back up first.** Several WinRE tools change disk, update or registry data.
If the user's data is not backed up, copy it off before anything invasive,
and have the BitLocker recovery key ready.

## Getting in
- WinRE starts automatically after two consecutive failed attempts to start
  Windows, two consecutive unexpected shutdowns within two minutes of boot
  completion, or two consecutive reboots within two minutes of boot completion.
- From the sign-in screen: select Shutdown, then hold Shift while selecting
  Restart.
- From a working desktop: `shutdown /r /o /t 0` (`/o` opens Advanced boot
  options and must be used with `/r`).
- Installation media: Install Windows screen, Next, Repair your computer,
  Troubleshoot, Advanced options. Shift+F10 opens a command prompt.
- `reagentc /info` shows whether WinRE is enabled.

## Order of tools (least to most invasive)
1. **Startup Repair**: log at `%windir%\System32\LogFiles\Srt\Srttrail.txt`.
2. **Safe Mode / Safe Mode with Networking** from the advanced boot options:
   if it boots, use Event Viewer to find the failing driver or service.
3. **System Restore**, only if restore points exist (the feature is off by
   default).
4. **Command Prompt**: offline system file check:
   `sfc /scannow /offbootdir=<WindowsDrive>\ /offwindir=<WindowsDrive>\windows`,
   and the boot repair steps in the `rebuilding-windows-boot-configuration`
   skill.
5. Remove pending or bad updates with DISM (see
   `uninstalling-bad-windows-updates`).

## BitLocker prompt
WinRE can ask for the BitLocker recovery key (for example before a Remove
everything reset when the OS drive uses TPM plus PIN or a password). Get it
from the escrow location named in the `bitlocker-recovery-key-retrieval`
skill, and verify the caller's identity before reading a key out. The key ID
on screen must match the stored key ID.

## Gotchas
- Drive letters in WinRE differ from the running system. Check with `dir`
  before running a repair against a drive.
- If the system keeps looping back to the recovery options,
  `bcdedit /set {default} recoveryenabled no` breaks the cycle (Microsoft's
  boot troubleshooting article).

## Verify
Normal boot reaches sign-in twice in a row; `reagentc /info` shows WinRE
enabled; Event Viewer has no new Event ID 41 (unexpected restart) after the
fix.


## Checked

Date 2026-10-27. Documentation release: Microsoft Learn WinRE technical reference, Windows boot troubleshooting article, shutdown and sfc command pages, BitLocker recovery overview, as published October 2026. Confirmed: the automatic WinRE triggers, Shift plus Restart from the sign-in screen, shutdown /r /o, installation-media route and Shift+F10, Startup Repair log path, Safe Mode options, offline sfc switches, System Restore availability, the WinRE BitLocker key prompt, recoveryenabled, Event ID 41 reference. Removed: hold-power-three-times trick, Startup Settings numbers, X: RAM disk, chkdsk and DISM /RestoreHealth /Source recipes, Reset this PC and SMART advice, aka.ms key link, comptia.org source.

Method: documentation only; no commands were run.
