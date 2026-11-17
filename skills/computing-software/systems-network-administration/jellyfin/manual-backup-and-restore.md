---
id: computing-software.systems-network-administration.jellyfin.manual-backup-and-restore
name: manual-backup-and-restore
category: computing-software
field: systems-network-administration
product: jellyfin
tags: [jellyfin, backup, restore, manual-backup, upgrade, rollback]
level: practitioner
status: docs-checked
description: "Back up and restore Jellyfin by stopping the server and copying its data and config directories, with Debian commands."
sources: ["https://jellyfin.org/docs/general/administration/backup-and-restore/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Manual backup and restore

Use a manual backup when you want a filesystem-level copy. The server **must be stopped** first, otherwise the database is locked and may not be recoverable.

**Back up**
1. Stop Jellyfin: Dashboard "Shutdown" on any platform, `docker stop jellyfin`, or `sudo systemctl stop jellyfin` for Debian and Ubuntu packages.
2. Copy both the data and configuration directories. Defaults: Debian/Ubuntu and RPMFusion packages use `/var/lib/jellyfin` for data and `/etc/jellyfin` for config (set in `/etc/default/jellyfin` or `/etc/sysconfig/jellyfin`); Docker uses whatever your `/config` volume maps to, which holds both.
3. Start Jellyfin again.

Debian example from the docs:

```bash
TIMESTAMP=$(date +%Y%m%d%H%M%S)
VERSION=10.9.10
sudo mkdir -p /media/backups/jellyfin.${TIMESTAMP}_${VERSION}
sudo cp -a /var/lib/jellyfin /media/backups/jellyfin.${TIMESTAMP}_${VERSION}/data
sudo cp -a /etc/jellyfin /media/backups/jellyfin.${TIMESTAMP}_${VERSION}/config
```

The docs suggest dated, versioned directory names for the copies.

**Restore**
1. Stop Jellyfin.
2. Move current directories aside, for example `sudo mv /var/lib/jellyfin /var/lib/jellyfin.bak`.
3. Copy, do not move or rename, the backup to the original names with `cp -a`.
4. Downgrade the package to the version of the backup if needed.
5. Start Jellyfin; it should start cleanly on the old data.

If you changed the data or config paths, back up those instead.

## Checked

2026-11-03. Confirmed against the Jellyfin Backup and Restore page, Manual Backup sections: stop first, stop commands, default Debian/RPMFusion/Docker locations, example script, restore steps. Removed: an unsupported rationale for naming.

Method: documentation only; no commands were run.
