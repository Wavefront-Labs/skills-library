---
id: computing-software.digital-privacy-hygiene.password-managers.keepass-mobile-clients-keepassdx-and-strongbox
name: keepass-mobile-clients-keepassdx-and-strongbox
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, keepassdx, strongbox, keepassium, kdbx, mobile-autofill-service, syncthing, keepass-mobile]
level: practitioner
status: draft
description: "Use a KeePass vault on phones with KeePassDX (Android) or Strongbox/KeePassium (iOS): file access, sync, autofill and quick unlock without corrupting the database."
sources:
  - "https://www.keepassdx.com/"
  - "https://strongboxsafe.com/"
  - "https://keepassium.com/"
  - "https://www.privacyguides.org/en/passwords/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# KeePass on mobile

**Goal:** the local-vault model only works if the phone can read and write the same
`.kdbx` safely.

## Android: KeePassDX
1. Get the file onto the phone: Syncthing-Fork syncing the vault folder, or a cloud
   provider's document provider (Nextcloud, Google Drive) via Android's file picker.
2. KeePassDX > Open existing database > choose the file via the system picker.
3. Settings > **Autofill**: set KeePassDX as autofill service; or use its
   "Magikeyboard" for apps that don't support autofill.
4. **Advanced unlock**: biometric unlock stores an encrypted copy of your credentials
   in the Android Keystore; re-entry of the master password is required periodically.
5. Key file: store a copy in app-private storage, not Downloads.

## iOS: Strongbox or KeePassium
1. Add the database from Files (iCloud Drive, Dropbox, OneDrive, local) or Strongbox's
   built-in WebDAV/SFTP sync.
2. Settings > General > AutoFill & Passwords > enable the app.
3. Face ID quick unlock with "require master password every N days".
4. YubiKey: both support NFC/USB challenge-response on capable keys (feature may be paid).

## Avoiding corruption and conflicts
- Let one device finish writing and syncing before editing on another.
- Prefer "read-only" mode on devices where you rarely edit.
- If you get conflicted copies, merge on desktop (see
  `computing-software.digital-privacy-hygiene.password-managers.merging-divergent-kdbx-databases`).

## Gotchas
- Opening a `.kdbx` from an email attachment or a "copy" creates a fork nobody syncs.
- Some features (Argon2 parameters, KDBX 4.1 attributes) need up-to-date clients; keep
  apps updated across devices to avoid a client silently dropping data it doesn't
  understand.

## Verify
- [ ] Add entry on phone, see it on desktop after sync; and the reverse.
- [ ] Autofill fills a login in a mobile app.
