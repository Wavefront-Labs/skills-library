---
id: computing-software.general-digital-literacy.file-management.encrypting-a-usb-drive
name: encrypting-a-usb-drive
category: computing-software
field: general-digital-literacy
product: file-management
tags: [file-management, file-archives-removable, bitlocker-to-go, encrypted-usb, filevault]
level: intro
status: docs-checked
description: "Encrypt a USB stick or external drive with BitLocker To Go on Windows Pro or an encrypted APFS format in Mac Disk Utility, and keep the recovery key safe."
sources:
  - https://support.microsoft.com/en-us/windows/bitlocker-drive-encryption-76b92ac9-1040-48d6-9f5f-d14b3c5fa178
  - https://support.apple.com/guide/disk-utility/encrypt-a-storage-device-dskutl35612/mac
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Encrypt a USB drive

A lost unencrypted USB stick is a data breach. Encrypt drives that carry personal or work files, and backup drives.

## Windows: BitLocker To Go
- BitLocker Drive Encryption is available only on Windows Pro, Enterprise and Education, not Home.
- Sign in as an administrator, then Start > type BitLocker > **Manage BitLocker**. USB sticks are listed under **Removable data drives - BitLocker To Go**.
- Select **Turn on BitLocker**, choose an unlock option and back up the recovery key (store it away from the drive). Encryption can take a while; you can keep using the PC.
- On managed devices the IT department may control BitLocker.

## Mac: Disk Utility (erases the drive)
- Copy off anything you need first; encrypting this way erases the device.
- Disk Utility > View > **Show All Devices** > select the device > **Erase** > scheme **GUID Partition Map** > an encrypted format such as APFS (Encrypted) > enter and verify a password > Erase.
- To change the password later: select the volume, File > Change Password.
- An external drive encrypted this way asks for the password whenever you connect it.
- To encrypt without erasing, Apple points to FileVault in Privacy & Security settings.

## Gotchas
- Lost password plus lost recovery key means the data is gone.

## Verify
- [ ] Plugging the drive in asks for a password before showing files.

## Checked
Date: 2026-10-27. Documentation: Microsoft Support "BitLocker Drive Encryption" and Apple Disk Utility User Guide "Encrypt and protect a storage device with a password" (2026). Removed unconfirmed claims: Home can unlock drives, Compatible mode, Time Machine encryption, cross-platform readability and the VeraCrypt suggestion.
Method: documentation only; no commands were run.
