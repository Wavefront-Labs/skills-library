---
id: computing-software.digital-privacy-hygiene.two-factor-auth.ente-auth-encrypted-sync
name: ente-auth-encrypted-sync
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, ente-auth-sync, ente-auth, authenticator-app, totp-backup]
level: practitioner
status: draft
description: "Set up Ente Auth as a TOTP app with end-to-end encrypted sync, import existing codes, save the recovery key and keep an offline export."
sources:
  - "https://ente.io/auth/"
  - "https://help.ente.io/auth/"
  - "https://github.com/ente-io/ente"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Ente Auth end-to-end encrypted sync

**Goal:** TOTP codes that survive a lost phone, synced across devices, without the sync provider being able to read
the seeds.

## Why Ente Auth
- Open source (client and server), cross-platform: Android, iOS, macOS, Windows, Linux, and a read-only web view.
- Works offline with no account; sign in only if you want sync. Sync is end-to-end encrypted: seeds are encrypted
  with a key derived from your password on the device before upload.
- Imports from Google Authenticator (export QR), Aegis, 2FAS, Bitwarden, Raivo and plain `otpauth://` text.

## Setup
1. Install from the official store or GitHub releases; create an account with a long unique password stored in your
   password manager.
2. **Save the recovery key** shown at sign-up (a word list). Ente cannot reset your password; without the password
   or recovery key the synced codes are gone. Put it with your other recovery codes, offline.
3. Turn on the app lock (Settings > Security > Lockscreen) so an unlocked phone does not show every code.
4. Import: Settings > Data > Import codes, pick the source app format. Spot-check three codes against sites.
5. Install on a second device and sign in; confirm codes appear and match.

## Keep an independent backup
Settings > Data > Export codes > **Encrypted** (password-protected) and store the file offline. A plain-text export
is every seed in the clear; only use it for an immediate migration and then delete it.

## Gotchas
- Sync means a compromise of your Ente password plus email access gives remote access to the encrypted blob; the
  password still has to be cracked, so make it strong and enable Ente's own 2FA on the account.
- Deleting a code on one device deletes it everywhere. Export before bulk cleanups.
- Clock drift breaks TOTP on any app; enable automatic time.

## Verify
Factory-reset test: on a spare device, sign in with only your password (or recovery key) and confirm all codes
restore.
