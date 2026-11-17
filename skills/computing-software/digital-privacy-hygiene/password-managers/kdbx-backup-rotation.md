---
id: computing-software.digital-privacy-hygiene.password-managers.kdbx-backup-rotation
name: kdbx-backup-rotation
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, kdbx-backup-rotation, keepassxc, kdbx, backups, 3-2-1-backup, sync-conflict, versioning, offline-backup]
level: practitioner
status: draft
description: "Back up a KeePassXC database with automatic pre-save backups, versioned copies and an offline copy, and handle sync-conflict files before they lose entries."
sources:
  - "https://keepassxc.org/docs/KeePassXC_UserGuide"
  - "https://docs.syncthing.net/users/versioning.html"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# KDBX backup rotation

**Goal:** with a local vault, you are the backup provider. One corrupted save or
deleted file must never cost you your credentials.

## Layers
1. **Pre-save backup**: KeePassXC Settings > General > File Management >
   "Backup database file before saving". Set the backup path pattern to include a
   timestamp, e.g. `{DB_FILENAME}.{TIME:yyyyMMdd-HHmmss}.old.kdbx` (check the
   pattern placeholders in your version's settings dialog).
2. **Versioned sync**: with Syncthing, enable **Staggered File Versioning** on the vault
   folder (keeps versions for a year at decreasing frequency). Cloud drives' version
   history works too.
3. **Offline copy**: monthly, copy the `.kdbx` to an encrypted USB stick kept elsewhere
   (relative's house, safe deposit box). The file is already encrypted; the stick's own
   encryption protects key files stored beside it, which should not be.
4. **Key file backup** if you use one: a separate location from the database copies.

## Pruning
Keep: last 10 pre-save backups, monthly offline copies for a year. Old copies open with
**old passwords**, so after a master password change because of compromise, delete
them (see
`computing-software.digital-privacy-hygiene.password-managers.changing-master-password-and-rotating-encryption-key`).

## Sync conflicts
Syncthing writes `vault.sync-conflict-<date>-<device>.kdbx`; cloud drives write
"conflicted copy" files. Never delete one without merging: open the main DB > Database >
**Merge from database** > choose the conflict file, then delete it.

## Verify
- [ ] Monthly: open the newest offline copy with your password (and key file).
- [ ] No `sync-conflict` files older than a day exist in the vault folder.
