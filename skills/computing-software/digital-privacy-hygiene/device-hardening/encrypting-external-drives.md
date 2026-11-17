---
id: computing-software.digital-privacy-hygiene.device-hardening.encrypting-external-drives
name: encrypting-external-drives
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, external-drive-encryption, device-encryption, file-encryption]
level: practitioner
status: draft
description: "Encrypt USB sticks and external drives with BitLocker To Go, APFS encryption, LUKS or VeraCrypt, choosing by which computers must read them."
sources:
  - "https://support.microsoft.com/windows/bitlocker-to-go-overview"
  - "https://support.apple.com/guide/disk-utility/encrypt-a-storage-device-dskutl35612/mac"
  - "https://gitlab.com/cryptsetup/cryptsetup/-/wikis/FrequentlyAskedQuestions"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Encrypting external drives

**Goal:** a lost backup drive or USB stick reveals nothing.

## Pick by compatibility
| Must open on | Use |
|---|---|
| Windows only | BitLocker To Go |
| Mac only | APFS (Encrypted) |
| Linux only | LUKS |
| Windows + Mac + Linux | VeraCrypt container/volume (exFAT inside) |
| Any machine without software | Hardware-encrypted drive with keypad |

## Windows: BitLocker To Go
File Explorer > right-click drive > **Turn on BitLocker** (Pro/Enterprise/Education to encrypt; Home can unlock).
Choose password, save recovery key, "Encrypt entire drive" for used drives, compatible mode for older Windows.
CLI: `manage-bde -on E: -Password` then `manage-bde -status E:`.

## macOS
- Empty drive: Disk Utility > View > Show All Devices > select drive > Erase > Format **APFS (Encrypted)**.
- Existing APFS drive: Finder > right-click > Encrypt "Name".
Time Machine offers "Encrypt backups" when choosing the disk.

## Linux
```
sudo cryptsetup luksFormat /dev/sdX1
sudo cryptsetup open /dev/sdX1 backup
sudo mkfs.ext4 /dev/mapper/backup
```
GNOME Disks can do the same ("Password protect volume (LUKS)").

## Gotchas
- Store the password/recovery key in your password manager, not on the drive.
- `/dev/sdX` mistakes erase the wrong disk; confirm with `lsblk` first.
- Some TVs/cars/cameras can't read encrypted media; keep those drives free of sensitive data instead.
