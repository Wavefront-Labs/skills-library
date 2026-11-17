---
id: computing-software.systems-network-administration.audiobookshelf.backups-manual-restore
name: backups-manual-restore
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [backups, restore, sqlite, systemctl, docker, unzip]
level: advanced
status: docs-checked
description: "Restore an Audiobookshelf 2.3.x or newer backup manually: stop the server, unzip, copy audiobookshelf.sqlite, authors and items back, then start."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/server-management/backups.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
You can use the Restore button on the backups page, or restore through the file system:

1. Stop the service: `systemctl stop audiobookshelf.service`, `docker stop <container-name>`, or close the app via the tray on Windows.
2. Go to your base path. For a service install that is `/usr/share/audiobookshelf`; for Docker it is the folder with your compose file. If you changed the metadata or config paths, go there instead.
3. Locate and unzip the newest backup (named by creation date): `cd metadata/backups` then `unzip <date>.audiobookshelf`. If the newest fails, try the next newest. On Windows use a tool such as 7-Zip.
4. Replace the database: `cp audiobookshelf.sqlite ../../config/audiobookshelf.sqlite`.
5. Replace the folders: `cp -r metadata-authors ../authors` and `cp -r metadata-items ../items`.
6. Start the service: `systemctl start audiobookshelf.service` or `docker start <container-name>`.

On Windows copy the same file and the contents of `metadata-authors` and `metadata-items` into `metadata/authors` and `metadata/items`. Backups hold only the database and metadata images, not media files, and Windows backups restore only on Windows installs and Linux backups on Linux installs without manual database changes.

## Checked

Method: docs-checked 2026-11-09 against the Backups page of the Audiobookshelf docs repo (full raw markdown read). Replaced an unconfirmed corruption claim with the page's platform warning.
