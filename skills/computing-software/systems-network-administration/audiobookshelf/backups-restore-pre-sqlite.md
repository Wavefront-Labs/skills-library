---
id: computing-software.systems-network-administration.audiobookshelf.backups-restore-pre-sqlite
name: backups-restore-pre-sqlite
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [backups, restore, sqlite, migration, legacy-backups]
level: advanced
status: docs-checked
description: "Restore a backup made before Audiobookshelf 2.3.0 by restoring on 2.2.23 first and then migrating to the SQLite database."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/server-management/backups.md
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/install/2.docker-compose-install.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Audiobookshelf moved from a file-based data structure to an SQLite database in server version 2.3.x (released July 2023). Backups from before 2.3.0 are **not supported** on 2.3.x and above.

Required path: first restore the old backup on server version 2.2.23, then let the server go through the migration to SQLite. Do not try to load it directly into a current server.

You can restore these older backups through the web interface or by extracting the backup zip manually. The manual mapping from the page:

- Copy `/config` to the `/config` location.
- Copy `/metadata-items` to `/metadata/items`.
- Copy `/metadata-authors` to `/metadata/authors`.

If you are on a current version and the backup is from 2.3.x or later, use the standard restore procedure instead (Restore button, or copy `audiobookshelf.sqlite`, `authors` and `items`).

## Checked

2026-11-04. Confirmed against the Audiobookshelf docs: Backups page (Restoring backups for 2.2.23 and older).

Method: documentation only; no commands were run.
