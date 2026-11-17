---
id: computing-software.email-administration.mailcow.mailcow-backup-script-and-cron
name: mailcow-backup-script-and-cron
category: computing-software
field: email-administration
product: mailcow
tags: [backup-script, backup-and-restore-sh, threads, delete-days, backup-location, cron-backup, rsync-backup]
level: practitioner
status: docs-checked
description: "Back up mailcow components with helper-scripts/backup_and_restore.sh, tune threads and location, schedule with cron, and combine with rsync of volumes."
sources: ["https://docs.mailcow.email/backup_restore/b_n_r-backup/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# mailcow backup script and scheduling

Use `helper-scripts/backup_and_restore.sh backup <components>` where components are `vmail`, `crypt`, `redis`, `rspamd`, `postfix`, `mysql` or `all`. Append `--delete-days n` to remove backups older than n days. Do not copy the script elsewhere.

Environment variables:
- `THREADS=n` enables multithreading (since 2022-10) for backup and restore; the docs advise leaving two cores free (core count minus 2).
- `MAILCOW_BACKUP_LOCATION=/path/to/backups` runs unattended; without it the script prompts for a location. Inside it the script creates `mailcow_DATE` folders; do not rename them or restore breaks.

Cron example: `5 4 * * * cd /opt/mailcow-dockerized/; MAILCOW_BACKUP_LOCATION=/mnt/mailcow_backups /opt/mailcow-dockerized/helper-scripts/backup_and_restore.sh backup mysql crypt redis --delete-days 3`. Cron mails full output by default; a user-contributed wrapper in `/etc/cron.daily/mailcow-backup` prints output only when the exit code is non-zero.

Alternative strategy: nightly `rsync -aH --delete` of the mailcow directory and of the Docker volumes directory to an external share, plus the script for `mysql crypt redis`. Put snapshots (ZFS, Btrfs) on the destination and never rsync to a Samba share, because permissions must be preserved. To restore, rsync back, restart Docker and run `docker compose pull` and `up -d`; Redis and MariaDB may self-repair, otherwise use the script for the damaged components.

## Checked

2026-11-09. Confirmed on the Backup page: script syntax and components, delete-days, THREADS and its core count advice, MAILCOW_BACKUP_LOCATION, mailcow_DATE folders, cron example, the user-contributed cron.daily wrapper, and the rsync strategy with snapshots, Samba warning and restore steps. No changes needed.

Method: docs-checked 2026-11-09 against the full Backup page (b_n_r-backup.en.md in mailcow-dockerized-docs).
