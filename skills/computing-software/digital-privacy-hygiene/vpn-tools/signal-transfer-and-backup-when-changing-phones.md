---
id: computing-software.digital-privacy-hygiene.vpn-tools.signal-transfer-and-backup-when-changing-phones
name: signal-transfer-and-backup-when-changing-phones
category: computing-software
field: digital-privacy-hygiene
product: vpn-tools
tags: [digital-privacy-hygiene, vpn-tools, signal-backup, signal, signal-messenger, device-transfer, secure-backups, backup-passphrase, new-phone, android, ios]
level: practitioner
status: draft
description: "Move Signal history to a new phone with direct transfer or an encrypted backup, store the 30-digit passphrase / recovery key, and wipe the old phone afterwards."
sources:
  - "https://support.signal.org/hc/en-us/articles/360007059752-Backup-and-Restore-Messages"
  - "https://support.signal.org/hc/en-us/articles/360007321171-Can-I-transfer-my-Signal-account-to-a-new-device"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Signal transfer and backup

**Goal:** Signal history lives only on your devices. Without a planned transfer or
backup, a new or lost phone means starting empty (which some people prefer).

## Direct transfer (old phone in hand)
- Same platform (iOS to iOS, Android to Android): on the new phone, register and choose
  **Transfer from old device**; scan the QR shown on the new phone with the old one.
  Both on the same Wi-Fi.
- Cross-platform (Android <-> iOS): Signal supports transferring account and message
  history directly in recent versions; follow the in-app prompts.
After transfer, the old phone's Signal is deactivated.

## Backups (phone may be lost)
- **Android local backup**: Settings > Chats > Chat backups > Turn on; records a
  **30-digit passphrase** (write it down) and saves an encrypted `.backup` file to a
  folder you choose; copy that file off the phone regularly.
- **Signal Secure Backups** (newer, opt-in cloud backup): end-to-end encrypted with a
  recovery key you must store; check availability and terms on your platform.
- iOS historically had no local backup; use direct transfer or Secure Backups.

## Store the secrets
Passphrase/recovery key in your password manager and on the recovery sheet; without it
the backup is useless.

## After moving
Old phone: wipe it (see `computing-software.digital-privacy-hygiene.device-hardening.secure-data-wiping-and-disposal`).

## Gotchas
- Disappearing messages that expired aren't transferred (by design).
- Registration Lock PIN is still needed when re-registering.

## Verify
- [ ] New phone shows full history; old phone shows "deregistered".
- [ ] Backup passphrase/recovery key retrievable from the vault.
