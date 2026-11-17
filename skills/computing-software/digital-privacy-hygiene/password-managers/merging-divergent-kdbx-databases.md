---
id: computing-software.digital-privacy-hygiene.password-managers.merging-divergent-kdbx-databases
name: merging-divergent-kdbx-databases
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, kdbx-merge, keepassxc, kdbx, sync-conflict, entry-history, uuid]
level: practitioner
status: docs-checked
description: "Merge two diverged copies of a KeePass database (sync conflicts, laptop vs phone) with KeePassXC's Merge From Database so no new or edited entries are lost."
sources:
  - "https://keepassxc.org/docs/KeePassXC_UserGuide"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Merging divergent KDBX databases

**Goal:** when two devices edited the vault offline and you now have `vault.kdbx` and a conflict copy, combine
them without losing entries.

## How KeePassXC merges
Per the User Guide, the merge compares entries by their unique identifiers (UUIDs) and modified timestamp. When a
UUID matches, wherever the entry sits, the most recently modified version becomes current and the previous version
goes into the entry's history. New entries and groups are added to the open database. The guide says this is useful
for synchronizing databases from conflict files in cloud storage.

When you delete an entry, KeePassXC stores a record of the deletion (the UUID) so the entry does not reappear from
a merge; an existing entry with the same UUID as a deleted item is removed without a prompt.

## Steps
1. Back up both files.
2. Open the database you will keep.
3. **Database > Merge From Database**, choose the conflict copy, and enter its credentials if prompted.
4. Review recently changed entries and check an entry's **History** if you need an overwritten value (View, Restore
   and Delete are available per history item).
5. Save, and delete the conflict file only after the merged file has synced to every device.

## Gotchas
- The merge relies on entry history, so keep history enabled with a sufficient size (Max history items and Max
  history size are in the database settings; setting items to 0 saves no history).
- Check critical entries after merging; a wrong clock on one device can make a stale edit look newer.

## Verify
- [ ] Entries created on each side exist in the merged file.
- [ ] No conflict copies remain after confirming sync.

## Checked
2026-11-01. Confirmed in the KeePassXC User Guide: Merge From Database behaviour, deletion records, entry history
actions, history limits and their effect on merging. Removed: the `keepassxc-cli merge` commands and flags (the man
page URL returned 404), claims on mobile apps saving files, duplicate-entry behaviour, "older edit wins" detail.
Method: documentation only; no commands were run.
