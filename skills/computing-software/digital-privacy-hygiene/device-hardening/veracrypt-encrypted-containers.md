---
id: computing-software.digital-privacy-hygiene.device-hardening.veracrypt-encrypted-containers
name: veracrypt-encrypted-containers
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, veracrypt, file-encryption, encryption-software, encrypted-container, usb-encryption, hidden-volume, pim, keyfiles]
level: practitioner
status: draft
description: "Create and use VeraCrypt file containers or encrypted USB drives for sensitive documents: algorithm, password/PIM, filesystem choice, mounting hygiene and backups."
sources:
  - "https://veracrypt.fr/en/Documentation.html"
  - "https://www.privacyguides.org/en/encryption/#veracrypt-disk"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# VeraCrypt encrypted containers

**Goal:** a portable encrypted vault (file or whole USB stick) that opens on Windows,
macOS and Linux, independent of the OS's own disk encryption.

## Create a file container
1. VeraCrypt > Create Volume > **Create an encrypted file container** > Standard volume.
2. Location: e.g. `Documents/vault.hc` (any name; don't call it `secret`).
3. Encryption: **AES** (hardware accelerated) and hash **SHA-512** are fine defaults.
4. Size: what you need plus growth; it's fixed (VeraCrypt can't easily grow a container).
5. Password: 5-6 word diceware passphrase. Leave **PIM** default unless you know why
   (custom PIM raises/lower iteration count; forgetting a custom PIM = lockout).
6. Filesystem: **exFAT** for cross-platform, NTFS for Windows-only large files, ext4 Linux.
7. Move the mouse to gather randomness > Format.

## Encrypted USB drive
Create Volume > **Encrypt a non-system partition/device** > select the USB device >
"Create encrypted volume and format it" (erases it). On other computers VeraCrypt must be
installed (portable mode on Windows needs admin to mount).

## Use
Select a drive letter/slot > Select File > Mount > password. Work inside the mounted
drive, then **Dismount** (or set auto-dismount on inactivity, screen lock and sleep in
Settings > Preferences).

## Gotchas
- Mounted volumes are plaintext to any malware on the machine; dismount when done.
- Cloud-syncing a large container uploads the whole file after each change on some
  services; for cloud use Cryptomator instead.
- Hidden volumes (plausible deniability) are easy to destroy by writing to the outer
  volume, and deniability depends on context; use only with full understanding.
- Back up the container file itself (it's encrypted) and the **volume header**
  (Tools > Backup Volume Header) - header corruption = total loss.

## Verify
- [ ] Container mounts on a second OS with the password.
- [ ] Auto-dismount settings configured; header backup stored.
