---
id: computing-software.systems-network-administration.windows-server.bitlocker-recovery-keys-in-ad
name: bitlocker-recovery-keys-in-ad
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, bitlocker, bitlocker-recovery-key-ad, backup-bitlockerkeyprotector, group-policy, recovery-password-viewer]
level: practitioner
status: docs-checked
description: "Escrow BitLocker recovery passwords to AD DS with Backup-BitLockerKeyProtector and find them with the BitLocker Recovery Password Viewer in ADUC."
sources:
  - https://learn.microsoft.com/en-us/windows/security/operating-system-security/data-protection/bitlocker/recovery-process
  - https://learn.microsoft.com/en-us/powershell/module/bitlocker/backup-bitlockerkeyprotector
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Back up BitLocker recovery keys to AD DS

## GPO
Configure the BitLocker Group Policy setting that stores recovery information in AD DS before encrypting (see the BitLocker
recovery process page for the setting names).

## Existing volumes
```powershell
Backup-BitLockerKeyProtector -MountPoint $env:SystemDrive -KeyProtectorId '<KEY_PROTECTOR_ID>'
```
`Backup-BitLockerKeyProtector` saves a key protector for a BitLocker volume in AD DS.

## Find a key
The BitLocker Recovery Password Viewer is included with RSAT as an Active Directory Users and Computers extension. Use
*Find BitLocker Recovery Password* and type the first eight characters of the password ID.

## Verify
- [ ] The recovery password of each encrypted server can be found in AD DS by its password ID.

## Checked

2026-10-28. Confirmed against: BitLocker recovery process page (Recovery Password Viewer in RSAT, Find BitLocker Recovery Password, first eight characters of the password ID) and Backup-BitLockerKeyProtector reference (MountPoint, KeyProtectorId). Removed (not confirmable from the cited pages): GPO menu paths, manage-bde and BackupToAAD commands, Install-WindowsFeature RSAT name, msFVE-RecoveryInformation LDAP query, default-permission and delegation statements, deletion gotchas.

Method: documentation only; no commands were run.
