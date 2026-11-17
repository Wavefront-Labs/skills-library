---
id: computing-software.general-digital-literacy.digital-communication.backing-up-and-moving-chat-history
name: backing-up-and-moving-chat-history
category: computing-software
field: general-digital-literacy
product: digital-communication
tags: [digital-communication, messaging, chat-backup, whatsapp-backup, end-to-end-encrypted-backup, transfer-chats, signal-backup, new-phone]
level: intro
status: docs-checked
description: "Back up WhatsApp and Signal chats (encrypted cloud backup, local backup), restore them on a new phone, and transfer between iPhone and Android."
sources:
  - https://support.signal.org/hc/en-us/articles/360007059752-Backup-and-Restore-Messages
  - https://support.signal.org/hc/en-us/articles/360007320551-Linked-Devices
  - https://faq.whatsapp.com/490592613091019
  - https://faq.whatsapp.com/481135090640375
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Back up and move chat history

**Goal:** keep years of messages, photos and voice notes when changing or losing a phone.

## WhatsApp
- WhatsApp has a chat backup feature (see its help article "How to back up your chat history") and an optional **end-to-end encrypted backup**.
- For an encrypted backup you protect it with a passkey, a password, or a 64-digit encryption key. That password or key is the only way to open the backup or move it to a new device; WhatsApp cannot reset it or restore the backup for you. Store it somewhere safe.
- Check the backup settings inside WhatsApp for where the backup is stored and when it last ran; menu names change between versions.

## Signal
- Signal keeps messages only on your devices. It does not recover them if you have lost, wiped or uninstalled on the old phone, or switched between Android and iOS.
- **Android to Android:** on the new phone choose *Transfer or restore account*; on the old phone go to Settings > Account > **Transfer account**. Both phones need Wi-Fi and Bluetooth on and must be close; confirm the 7-digit code matches. Messages with a disappearing timer of one day or less are not transferred.
- **Android on-device backup:** Settings > **Backups > On-device backups**. Write down the 30-digit passphrase: without it the backup cannot be restored. Copy the backup file off the phone, because a backup on a lost phone is lost with it.
- **iPhone to iPhone:** choose *Transfer from iOS Device* on the new device and scan the QR code from the old one. The history is moved, not copied: the old device deletes it. iCloud and iTunes backups do not contain Signal messages.
- Signal's help also lists "Signal Secure Backups" and desktop backups; read the current article for what your version offers.

## Verify
- [ ] You can find a recent backup time, and you have recorded the backup password, key or passphrase offline.

## Checked
Date: 2026-10-27. Documentation: Signal Support "Backup and Restore Messages" (Android and iOS sections), WhatsApp Help Center encrypted-backup article (via search results). Confirmed: Signal menu paths, 30-digit passphrase, 7-digit code, one-day timer exclusion, iOS move-not-copy, no iCloud backup; WhatsApp encrypted-backup key/password and no-recovery statements. Removed unconfirmed WhatsApp menu paths, transfer-chats details, iMessage and Google One backup claims, and Wi-Fi-only default.
Method: documentation only; no commands were run.
