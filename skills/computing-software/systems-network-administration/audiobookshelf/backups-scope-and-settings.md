---
id: computing-software.systems-network-administration.audiobookshelf.backups-scope-and-settings
name: backups-scope-and-settings
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [backups, retention, backup-path, sqlite, database]
level: practitioner
status: docs-checked
description: "Know what Audiobookshelf backups contain, where they are stored, and how the keep-count and maximum-size limits work."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/server-management/backups.md
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/install/11.env-configuration.md
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/0.introduction.md
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/server-management/migration-os.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Audiobookshelf backups let you restore a previous database state. They include only the database and cover images stored in the `metadata/` directory (authors and items). **No media files** and no covers stored with library items are included, so back those up by another method.

Location: by default `/metadata/backups`. Change it in the web interface or with the `BACKUP_PATH` environment variable. If you set it with the environment variable, the web interface can no longer edit the path.

Limits: you can set how many backups to keep and a maximum backup size. For both fields, `0` means unlimited.

Compatibility warnings:

- Backups cannot be loaded from another installation method without losing progress and metadata.
- Windows backups restore only on Windows installs and Linux backups only on Linux installs, unless you manually modify the database.

The introduction page lists backups with automated backup scheduling as a feature.

## Checked

2026-11-04. Confirmed against the Audiobookshelf docs: Backups page, Environment Configuration page and Introduction page.

Method: documentation only; no commands were run.
