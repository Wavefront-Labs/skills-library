---
id: computing-software.systems-network-administration.immich.filesystem-backup-layout
name: filesystem-backup-layout
category: computing-software
field: systems-network-administration
product: immich
tags: [upload-location, library, thumbs, encoded-video, storage-template]
level: practitioner
status: docs-checked
description: "Know which Immich folders under UPLOAD_LOCATION hold originals versus regenerable files, with and without the storage template, so you back up the right paths."
sources:
  - https://docs.immich.app/administration/backup-and-restore
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: choose what to include in a filesystem backup of Immich. Immich does not back up files for you; you need a real backup tool.

Under `UPLOAD_LOCATION`:

- `upload/<userID>`: original assets uploaded via browser, mobile and CLI (storage template off).
- `library/<userID>`: originals once the storage template is on; the admin's default storage label is `admin` and replaces the user ID in `library/`. Mobile uploads wait in `upload/` until transferred.
- `profile/<userID>`: avatars.
- `thumbs/<userID>`: small thumbnails, large previews and face thumbnails.
- `encoded-video/<userID>`: re-encoded videos; originals are kept.
- `backups/`: automatic database dumps.

Postgres data lives in `DB_DATA_LOCATION`.

Recommended: back up the whole `UPLOAD_LOCATION`. If you want a minimal set, back up exactly:

1. `UPLOAD_LOCATION/library`
2. `UPLOAD_LOCATION/upload`
3. `UPLOAD_LOCATION/profile`

With only those, you must rerun the transcoding and thumbnail generation jobs for all assets after restoring. If you moved a folder such as `profile/` to another device, adjust the backup path.

Turning the storage template off leaves existing files in `library/`; only new assets go to `upload/`.

Do not touch these folders except to take backups. Changing or removing a file can cause untracked and missing files. Find your user ID under Account Settings, Account.

## Checked

2026-11-03. Confirmed against the Immich docs (https://docs.immich.app/) by reading: administration/backup-and-restore (Filesystem, Asset Types and Storage Locations).
Removed or reworded: the integrity report wording.
Method: documentation only; no commands were run.
