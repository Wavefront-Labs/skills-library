---
id: computing-software.digital-privacy-hygiene.device-hardening.checking-disk-encryption-status
name: checking-disk-encryption-status
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, encryption-status-check, full-disk-encryption, bitlocker, filevault]
level: practitioner
status: docs-checked
description: "Check disk encryption: manage-bde -status on Windows, what FileVault on versus off means on Apple silicon and T2 Macs, and Android file-based encryption."
sources:
  - "https://learn.microsoft.com/windows-server/administration/windows-commands/manage-bde-status"
  - "https://support.apple.com/guide/deployment/intro-to-filevault-dep82064ec40/web"
  - "https://source.android.com/docs/security/features/encryption"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Checking disk encryption status

**Goal:** confirm encryption rather than assuming it, on every device you own.

## Windows
```
manage-bde -status C:
```
`manage-bde -status [<drive>]` reports on all drives, whether or not they are BitLocker-protected: size, BitLocker version,
conversion status, percentage encrypted, encryption method, protection status, lock status, identification field and key
protectors. Omit the drive to list every drive. The `-protectionaserrorlevel` (or `-p`) switch makes the command return 0 if
the volume is protected and 1 if it is unprotected, which suits batch scripts.

## macOS
- With FileVault on, credentials are required during boot, and without valid login credentials or a cryptographic recovery
  key the internal APFS volumes stay encrypted even if the storage device is removed and connected to another computer.
- On Apple silicon and T2 Macs the volume is encrypted even if FileVault was not turned on at set-up, but then the volume
  encryption key is protected only by the hardware UID in the Secure Enclave. Turning FileVault on later is immediate (the data
  was already encrypted); the volume is then protected by the user password combined with the hardware UID, and an
  anti-replay mechanism stops the old key being used.
- Removable storage encryption does not use the Secure Enclave and works as on Intel Macs without a T2 chip.

## Android
Android 7.0 and later support file-based encryption, where different files are encrypted with different keys that can be
unlocked independently (enabling Direct Boot). Android 9 added metadata encryption where hardware supports it. Full-disk
encryption (a single key protecting the userdata partition) was supported from Android 5.0 up to Android 9 and is not
allowed on new devices running Android 10 and higher; new devices use file-based encryption.

## Record
Note the status and where the recovery key is stored for each device.

## Checked
Date: 2026-11-09. Read in full: Microsoft Learn `manage-bde status`, Apple Platform Deployment "Intro to FileVault" and the
AOSP Encryption page. Removed as not on those pages: `Get-BitLockerVolume` output values, the Settings paths, the
"Waiting for activation" and "Suspended" BitLocker explanations, the `fdesetup status` command, all Linux LUKS commands, the
iPhone passcode data protection check, and the Android settings screen path.
Method: docs-checked 2026-11-09 against the three vendor pages named above.
