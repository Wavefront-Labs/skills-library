---
id: computing-software.systems-network-administration.windows-server.bcd-repair-bcdedit-bcdboot
name: bcd-repair-bcdedit-bcdboot
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, boot-troubleshooting, winre, bcdedit, bcdboot, uefi-boot, efi-system-partition, boot-repair]
level: advanced
status: docs-checked
description: "Repair Windows Server boot files from WinRE: inspect the BCD store with bcdedit /store and rebuild system partition boot files with bcdboot /s /f."
sources:
  - https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/bcdboot-command-line-options-techref-di
  - https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/bcdedit-command-line-options
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Repair BCD with bcdedit and bcdboot

Use when the boot configuration data (BCD) store or the boot files on the system partition are missing or damaged.

## Get to a prompt
Open a command prompt in WinRE or from Windows Server media. Drive letters can differ there: find the Windows volume:
```
diskpart
list vol
exit
dir <WinVol>:\Windows
```

## Inspect
```
bcdedit /store <ESP>:\EFI\Microsoft\Boot\BCD /enum
```

## Rebuild boot files (UEFI)
```
diskpart
sel disk 0
list part
sel part 1          (the FAT32 EFI System partition)
assign letter=S
exit
bcdboot <WinVol>:\Windows /s S: /f UEFI
```
bcdboot copies boot files from the Windows installation to the system partition (`/s S:`); `/f` selects the firmware
type (UEFI, BIOS or ALL).

## Back up the store
`bcdedit /export <ESP>:\BCD.bak` exports the system store to a file that can restore it later.

## Verify
- [ ] Server boots normally; `bcdedit /enum` shows correct device entries.

## Checked

2026-10-28. Confirmed against: bcdboot command-line options (/s, /f UEFI|BIOS|ALL), bcdedit command-line options (/store, /enum, /export) and the Windows deployment page (EFI system partition is FAT32). Removed (not confirmable from the cited pages): error code and symptom list, WinRE menu path, winload.efi/winload.exe check, partition size, bootrec commands, recoveryenabled/displaybootmenu/bootstatuspolicy/safeboot edits.

Method: documentation only; no commands were run.
