---
id: computing-software.it-support-helpdesk.desktop-support.rebuilding-windows-boot-configuration
name: rebuilding-windows-boot-configuration
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, bcdboot, bootrec, bcdedit, efi-system-partition, boot-failure, inaccessible-boot-device, bootmgr-missing, winre]
level: advanced
status: docs-checked
description: "Repair 'BOOTMGR is missing', 0xc000000f and boot-device errors by rebuilding the BCD and EFI boot files with bcdboot, bootrec and diskpart from WinRE."
sources:
  - "https://learn.microsoft.com/en-us/troubleshoot/windows-client/performance/windows-boot-issues-troubleshooting"
  - "https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/bcdboot-command-line-options-techref-di"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# rebuilding-windows-boot-configuration

Goal: the Windows volume is intact but the boot path is broken. Rebuild the
boot files; do not reinstall.

**Back up first.** Boot repair changes disk and boot data. Export the BCD
store before editing it (`bcdedit /export <file>`), and have the BitLocker
recovery key ready.

## Identify the phase
Microsoft's boot sequence: PreBoot (firmware), Windows Boot Manager,
Windows OS loader, then the kernel. Each phase troubleshoots differently.
- Boot loader phase symptoms: blinking cursor, BCD missing or corrupted,
  boot file or MBR corrupted, operating system missing, Bootmgr missing.
- Kernel phase: a Stop error after the Windows logo, such as
  `INACCESSIBLE_BOOT_DEVICE` (0x7B). That is not a BCD fault; see Microsoft's
  Stop error 7B article.

## Methods (from installation media, Shift+F10 command prompt, or WinRE)
1. **Startup Repair** (Repair your computer, Troubleshoot, Advanced options,
   Startup Repair). Log: `%windir%\System32\LogFiles\Srt\Srttrail.txt`.
2. **Boot codes**: `bootrec /fixmbr`, `bootrec /fixboot`. `/fixmbr` overwrites
   only the master boot code and may not fix partition-table damage.
3. **BCD errors**: `bootrec /scanos`; if that does not fix it:
```cmd
bcdedit /export <backup-file>
attrib <WindowsDrive>\boot\bcd -r -s -h
ren <WindowsDrive>\boot\bcd bcd.old
bootrec /rebuildbcd
```
4. **bcdboot** copies fresh boot files from the Windows folder to the system
   partition and creates a BCD store.

## bcdboot on UEFI
```cmd
diskpart
list vol
sel vol <n>              :: the ESP (FAT32)
assign letter=S
exit
bcdboot <WindowsDrive>\Windows /s S: /f UEFI
```
`/s` names the system partition and `/f` the firmware type. On UEFI, bcdboot
normally creates a Windows Boot Manager entry in firmware NVRAM, **but when `/s`
is used that entry is not created**; the firmware relies on its default
(`\efi\boot\bootx64.efi` on the ESP). Without `/s` bcdboot uses the
default system partition and does write the entry.

## Updates that left the PC unbootable
From the WinRE command prompt: `DISM /image:<WindowsDrive>\ /get-packages`,
remove pending packages, then
`DISM /Image:<WindowsDrive>\ /Cleanup-Image /RevertPendingActions`.

## Gotchas
- Drive letters in WinRE differ from the running system; confirm with `dir`
  before pointing a tool at a drive.
- If the screen keeps returning to the recovery options, Microsoft documents
  `bcdedit /set {default} recoveryenabled no` to break the cycle.
- If F8 options do not work, `bcdedit /set {default} bootmenupolicy legacy`.

## Verify
`bcdedit /enum` lists the Windows Boot Manager and a Windows Boot Loader for
the OS; two clean boots in a row.


## Checked

Date 2026-10-27. Documentation release: Microsoft Learn Windows boot troubleshooting article and bcdboot command-line options, as published October 2026. Confirmed: boot phases and loader-phase symptoms, Startup Repair steps and Srttrail.txt path, bootrec /fixmbr, /fixboot, /scanos, /rebuildbcd and the export/attrib/ren BCD sequence, bcdboot /s and /f syntax and the NVRAM-entry behaviour with and without /s, /RevertPendingActions procedure, recoveryenabled and bootmenupolicy commands. Removed: 0xc000000f/0xc0000098 mapping, 'Access denied on fixboot', AHCI/RAID and VMD causes, manage-bde unlock example, multi-boot note. Corrected: bcdboot with /s does not register the firmware entry.

Method: documentation only; no commands were run.
