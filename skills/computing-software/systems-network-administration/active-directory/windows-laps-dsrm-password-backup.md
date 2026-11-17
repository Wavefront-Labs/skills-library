---
id: computing-software.systems-network-administration.active-directory.windows-laps-dsrm-password-backup
name: windows-laps-dsrm-password-backup
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, windows-laps, laps, laps-dsrm, dsrm-password, directory-services-restore-mode, domain-controller, mslaps-encrypteddsrmpassword, password-rotation]
level: practitioner
status: docs-checked
description: "Have Windows LAPS manage and back up each DC's DSRM password (encrypted), retrieve it during recovery, and keep the history usable for restored DCs."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/laps/laps-management-policy-settings
  - https://learn.microsoft.com/en-us/windows-server/identity/laps/laps-scenarios-windows-server-active-directory
  - https://learn.microsoft.com/en-us/powershell/module/laps/get-lapsadpassword
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Windows LAPS for DSRM passwords

**Problem:** each DC's Directory Services Restore Mode password is set at promotion and
usually forgotten or identical everywhere. You need it exactly when AD is broken.

## Enable on DCs only
GPO linked to the **Domain Controllers** OU (Computer Configuration > Policies > Administrative Templates > System > LAPS). Policy settings:
- `BackupDirectory` = 2 (back up to Windows Server Active Directory only)
- `ADPasswordEncryptionEnabled` = True (default; DSRM backup is ignored unless it is True)
- `ADBackupDSRMPassword` = True (default False)
- `ADPasswordEncryptionPrincipal` = `AD\Domain Admins` (default) or a Tier 0 group
- `ADEncryptedPasswordHistorySize` = up to 12 (default 0, so no history is kept unless set)
- `PasswordAgeDays` (default 30)

Requirements: domain functional level 2016 or later, and Windows Server 2019 or later domain controllers for DSRM account management. The password is stored encrypted in `msLAPS-EncryptedDSRMPassword` on the DC's computer object, with history in `msLAPS-EncryptedDSRMPasswordHistory`.

Run `Invoke-LapsPolicyProcessing` on a DC and check the LAPS Operational log.

## Retrieve when needed
From another healthy DC or an admin host with RSAT:
```powershell
Get-LapsADPassword -Identity DC01 -AsPlainText -IncludeHistory
```
If you are restoring a DC from a backup taken months ago, its DSRM password is the one valid
at backup time: that is why the encrypted **history** matters.

## Fallback when AD is entirely down
LAPS passwords are stored in AD, so you normally need one domain controller to retrieve them. If every DC is down, query a mounted backup of the AD database with `Get-LapsADPassword -Port <port>` (mount the backup with `dsamain.exe`):
```powershell
Get-LapsADPassword -Identity DC01 -AsPlainText -Port 50000 -RecoveryMode
```
`-RecoveryMode` (which needs no domain controller and also works on a workgroup machine) is documented for Windows Insider build 27695 and later; check current availability before relying on it. Keep DC backups current.

## Verify
- [ ] Each DC's computer object has a recent `msLAPS-EncryptedDSRMPassword` update (`Get-LapsADPassword DC01`).
- [ ] A test reboot into DSRM on a lab DC with the retrieved password works.

## Checked
Checked 2026-10-27 against Microsoft Learn (Windows LAPS policy settings; Get started with Windows LAPS and Windows Server Active Directory, including the disaster recovery section; Windows LAPS technical reference; Get-LapsADPassword and Invoke-LapsPolicyProcessing references).
- Confirmed: setting names, defaults and ranges (ADBackupDSRMPassword default False, ADEncryptedPasswordHistorySize 0 to 12, PasswordAgeDays default 30, ADPasswordEncryptionPrincipal default Domain Admins, BackupDirectory 2); DSRM and history settings are ignored unless encryption is enabled; DFL 2016 and Windows Server 2019 or later DCs for DSRM management; msLAPS-EncryptedDSRMPassword and history attributes; Get-LapsADPassword -AsPlainText -IncludeHistory -Port -RecoveryMode; dsamain mounting of backups.
- Removed: the history value of 12 or more (maximum is 12), the ntdsutil DSRM sync procedure and the password-age range, which were not confirmed.

Method: documentation only; no commands were run.
