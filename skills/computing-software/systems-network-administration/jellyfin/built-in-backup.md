---
id: computing-software.systems-network-administration.jellyfin.built-in-backup
name: built-in-backup
category: computing-software
field: systems-network-administration
product: jellyfin
tags: [jellyfin, backup, built-in-backup, restore-archive, trickplay, dashboard]
level: practitioner
status: docs-checked
description: "Create and restore Jellyfin's built-in online backup from the Dashboard Backups tab or with the --restore-archive argument."
sources: ["https://jellyfin.org/docs/general/administration/backup-and-restore/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Built-in backup and restore

Jellyfin has a built-in backup that works while the server is running, unlike a manual copy, which needs the server stopped. The docs still advise running it at low activity and with no scan in progress.

**Create:** open the Dashboard, go to the `Backups` tab and choose `Create Backup`. Pick what to include:

- Database: always enabled; all data from `jellyfin.db` or the configured provider.
- Metadata: the metadata folder, possibly with metadata images.
- Subtitles: all extracted and downloaded subtitles.
- Trickplay: trickplay data not stored alongside media.

The backup folder must have at least 5 GB free, which may not be enough once subtitles and trickplay are included, so check space first. Each backup is written as a new zip archive in a `backups` folder inside the data directory, for example `/var/lib/jellyfin/data/backups` for Debian, Ubuntu and RPMFusion packages, or `<volume path>/config/data/backups` for the official Docker image (one extra `data` level for LinuxServer.io).

**Restore:** either use the restore button next to the archive in the Backups list, which immediately restarts the server and makes it unavailable meanwhile, or start Jellyfin with `--restore-archive PATH_TO_BACKUP_ZIP`.

Jellyfin has no downgrade mechanism: once a new version has started, pending migrations are applied and old versions cannot read the data. A backup taken before upgrading is the only way back.

## Checked

2026-11-03. Confirmed against the Jellyfin Backup and Restore page, Built-in Backup sections: online backup, Backups tab and Create Backup, four data choices, 5 GB free-space check, backups folder locations, restore button restarting the server, --restore-archive, no downgrade mechanism. Removed: unsupported advice to copy archives off the host.

Method: documentation only; no commands were run.
