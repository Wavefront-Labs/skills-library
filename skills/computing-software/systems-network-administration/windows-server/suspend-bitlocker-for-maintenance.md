---
id: computing-software.systems-network-administration.windows-server.suspend-bitlocker-for-maintenance
name: suspend-bitlocker-for-maintenance
category: computing-software
field: systems-network-administration
product: windows-server
tags: [bitlocker, suspend-bitlocker, manage-bde, firmware-updates, bitlocker-recovery]
level: practitioner
status: docs-checked
description: "Suspend BitLocker correctly before firmware, BIOS, boot manager or TPM changes using Suspend-BitLocker reboot counts, and avoid surprise recovery prompts."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/bitlocker/suspend-bitlocker
  - https://learn.microsoft.com/en-us/windows/security/operating-system-security/data-protection/bitlocker/recovery-overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Suspending BitLocker for maintenance

The TPM protector seals the key to boot measurements (firmware, Secure Boot state, boot manager). Changing them
without suspending triggers recovery mode: someone needs the 48-digit key at the console, painful on a remote server.

## Suspend
```powershell
Suspend-BitLocker -MountPoint C: -RebootCount 2
manage-bde -protectors -disable C: -RebootCount 2
```
- Protection resumes after the given number of reboots. If `-RebootCount` is omitted, it stays suspended until `Resume-BitLocker`. `manage-bde -protectors -disable` accepts a reboot count from 0 to 15.

## Changes that need it
Microsoft notes you might suspend protection for firmware upgrades or system updates. Changes to the Secure Boot PCR 7 profile or other TPM validation PCRs can also trigger recovery.

## Resume and check
```powershell
Resume-BitLocker -MountPoint C:
Get-BitLockerVolume C: | Select MountPoint,ProtectionStatus,VolumeStatus,KeyProtector
```
ProtectionStatus On = good.

## If recovery triggers anyway
Unlock with the recovery password, then suspend and resume once:
```cmd
manage-bde -protectors -disable C: -RebootCount 1
```

## Verify
- [ ] Maintenance runbooks include suspend before firmware tools; ProtectionStatus On after the change.

## Checked
2026-10-28: Confirmed on Learn pages suspend-bitlocker, manage-bde-protectors and the BitLocker recovery overview: Suspend-BitLocker -RebootCount, Resume-BitLocker, manage-bde -protectors -disable -rebootcount (0-15), suspension for firmware upgrades, PCR 7 and TPM validation profile changes. Removed: clear-key-on-disk statement, the detailed change list (boot order, bcdedit, disk moves), automatic suspension by Windows updates, key sources.
Method: documentation only; no commands were run.
