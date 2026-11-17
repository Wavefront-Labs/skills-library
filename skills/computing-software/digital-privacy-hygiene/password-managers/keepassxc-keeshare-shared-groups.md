---
id: computing-software.digital-privacy-hygiene.password-managers.keepassxc-keeshare-shared-groups
name: keepassxc-keeshare-shared-groups
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, keeshare, keepassxc, password-sharing]
level: practitioner
status: docs-checked
description: "Share a group of KeePassXC entries through a KeeShare container on a shared location, and keep import, export and synchronize modes and merge limits straight."
sources:
  - "https://keepassxc.org/docs/KeePassXC_UserGuide#_keeshare"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# KeePassXC KeeShare shared groups

**Goal:** share some entries (household logins) between people with separate KeePassXC databases, without sharing the whole database.

## Enable (per application)
Tools > Settings > KeeShare. Tick **Allow import** to import shared credentials and **Allow export** to share yours. An optional signing certificate (Generate) is marked deprecated and slated for removal.

## Set up a shared group
Sharing is defined on a group; every entry under it and its children is shared. Enabling it on the root node shares the whole database.
1. Edit the group, open the KeeShare category.
2. Type: Inactive; Import (read-only, merges changes); Export (write-only, no merge); Synchronize (read/write, merges changes).
3. Path: where the container is stored; it must be accessible to others (the guide suggests a network share or cloud storage).
4. Password for the share container.

The container is not generated automatically: the file is written each time the database is saved.

## Behaviour
- KeeShare watches the container and merges changes in Import and Synchronize modes. Entries merge in time order; older data goes to the entry history.
- A shared group shows a cloud badge and a banner with mode and location; a red cloud with a white X means the share is disabled or unavailable.

## Limits (from the guide)
- Group structure is not synchronised after the initial share; it works at entry level, so entries moved out of a shared group still sync.
- The merge relies on entry history, so history must be enabled with sufficient size.
- Moving an entry out of an export group stops further export but does not remove data already shared with other clients.
- Signing proves the exporter but cannot detect replacement with an older version from a valid signer; keep the container writable only by valid signers.

## Gotchas (judgement, not from the guide)
- Keep backups of both databases before enabling two-way sync.
- To remove someone, stop sharing and rotate the shared passwords: they keep what they already received.

## Checked
Method: 2026-11-08 read the KeeShare section of the KeePassXC User Guide. Settings, types, merge behaviour and limits follow it. Removed as unsupported: named sync tools (Syncthing, Nextcloud, Dropbox), "send the password via Signal", "container is a normal KDBX", and duplicate-edit claims. The cited keepassxc.org/docs root was dropped as a landing page.
