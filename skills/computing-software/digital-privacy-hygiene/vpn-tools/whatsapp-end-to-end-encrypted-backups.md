---
id: computing-software.digital-privacy-hygiene.vpn-tools.whatsapp-end-to-end-encrypted-backups
name: whatsapp-end-to-end-encrypted-backups
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, whatsapp-encrypted-backup, whatsapp, icloud-backup, google-drive-backup, 64-digit-key, backup-password, end-to-end-encryption]
level: intro
status: docs-checked
description: "Turn on WhatsApp end-to-end encrypted chat backups with a passkey, password or 64-digit key, so the cloud copy isn't readable by Apple, Google or WhatsApp."
sources:
  - "https://ssd.eff.org/module/how-to-use-whatsapp"
  - "https://engineering.fb.com/2021/09/10/security/whatsapp-e2ee-backups/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# WhatsApp end-to-end encrypted backups

**Goal:** WhatsApp chats are end-to-end encrypted in transit, but chat backups are optional, are not enabled by
default, and can be stored with or without encryption. Make any backup end-to-end encrypted.

## Enable
On Android: three-dot menu, Settings, Chats, Chat backup. On iPhone: Settings, Chats, Chat Backup. Tap "End-to-end
encrypted backup", then either "Use passkey" or "More options" to choose how the backup is protected: a passkey,
a password, or an encryption key.
- With the option on, WhatsApp, Google (or Apple) cannot access the backup contents.
- Backups are encrypted with a randomly generated key. WhatsApp's engineering post says you can secure the key
  yourself (a 64-digit encryption key) or with a password; with a password, the key is stored in a Backup Key Vault
  built on hardware security modules (HSMs).
- If you choose the key or password, save it somewhere safe such as a password manager. WhatsApp cannot help you
  recover the backup if you lose it.

## Gotchas
- Anyone you chat with can also back up their chats, including without end-to-end encryption. If that is a
  concern, help your contacts change their settings too.

## Verify
- [ ] The Chat backup screen shows end-to-end encrypted backup as on.
- [ ] The password or key is stored outside the phone.

## Checked
Method: docs-checked 2026-11-09 against the EFF Surveillance Self-Defense "How to use WhatsApp" section on end-to-end encrypted backups (read in full) and the Meta Engineering post "How WhatsApp is enabling end-to-end encrypted backups" (random-key, 64-digit key, password and HSM key vault statements found by targeted search of the downloaded page, not read in full). Dropped as unconfirmed: the restore steps, the Apple Advanced Data Protection note, the video-inclusion option, and the claim that the backup was historically the weak spot for legal requests. faq.whatsapp.com was removed from sources because it was not read.
