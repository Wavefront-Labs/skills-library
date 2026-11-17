---
id: computing-software.digital-privacy-hygiene.device-hardening.cryptomator-vaults-over-cloud-storage
name: cryptomator-vaults-over-cloud-storage
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, cryptomator, file-encryption, encryption-software, e2ee-cloud-storage, client-side-encryption, dropbox, google-drive, onedrive, recovery-key]
level: practitioner
status: draft
description: "Encrypt files client-side before they reach Dropbox, Google Drive or OneDrive with a Cryptomator vault, including mobile access and the recovery key."
sources:
  - "https://docs.cryptomator.org/"
  - "https://www.privacyguides.org/en/encryption/#cryptomator-cloud"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cryptomator vaults over cloud storage

**Goal:** keep using your existing cloud storage while the provider sees only encrypted
blobs. Cryptomator encrypts **file by file**, so sync stays efficient (unlike one big
VeraCrypt container).

## Create a vault
1. Install Cryptomator (desktop: Windows/macOS/Linux; mobile apps are paid on some
   platforms).
2. Add Vault > Create New > name > location **inside your synced cloud folder**
   (e.g. `Dropbox/Vaults/Personal`).
3. Password: long passphrase. Choose **Show recovery key** and store it in your password
   manager / recovery sheet; it's the only way back if you forget the password.
4. Unlock: Cryptomator mounts the vault as a virtual drive; work in the drive, never in
   the encrypted folder directly.

## What's protected
File contents and **file names** are encrypted; folder structure is obfuscated. The cloud
sees number of files, sizes (roughly) and modification times.

## Mobile
iOS/Android apps connect to the same cloud account, unlock with the password (biometric
option), and integrate with Files app (iOS).

## Gotchas
- Don't open the same vault on two devices while both are offline and editing; cloud
  conflict copies of encrypted files are confusing (Cryptomator detects some conflicts).
- Back up: the cloud copy is not a backup (deletions sync). Keep versioning on or a
  separate backup of the encrypted folder.
- Lock the vault when idle (auto-lock setting).

## Verify
- [ ] Viewing the cloud provider's web interface shows only encrypted filenames.
- [ ] Vault opens on a second device; recovery key stored.
