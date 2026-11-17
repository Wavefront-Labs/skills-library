---
id: computing-software.collaboration-platform-administration.nextcloud.backup-contents-and-maintenance-mode
name: backup-contents-and-maintenance-mode
category: computing-software
field: collaboration-platform-administration
product: nextcloud
tags: [backup, maintenance-mode, rsync, config-folder, data-folder]
level: practitioner
status: docs-checked
description: "List the five things to back up for Nextcloud, lock sessions with maintenance:mode, and copy folders with rsync before dumping the database."
sources:
  - https://docs.nextcloud.com/server/latest/admin_manual/maintenance/backup.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: take a restorable backup without inconsistencies.

Five things to retain:
1. the `config` folder
2. the custom `apps` folder (only if you have custom apps installed)
3. the `data` folder
4. the `theme` folder
5. the database

Step 1, maintenance mode. It locks the sessions of logged-in users and prevents new logins, so data cannot change mid-backup. Run `occ` as the HTTP user:

```
sudo -E -u www-data php occ maintenance:mode --on
```

Alternatively set `"maintenance" => true` in `config/config.php`, and set it back to `false` when finished.

Step 2, copy folders to a location outside the Nextcloud environment. You can copy config, data and theme, or the entire installation directory:

```
rsync -Aavx nextcloud/ nextcloud-dirbkp_`date +"%Y%m%d"`/
```

Step 3, dump the database with the tool for your engine (see database-dump-commands-per-engine).

Step 4, turn maintenance mode off:

```
sudo -E -u www-data php occ maintenance:mode --off
```

Before you ever restore, read the restore page; a backup you cannot restore is not a backup.

Check: the backup folder holds config, data and theme, and a database dump file dated today exists beside it.

## Checked

2026-11-03. Confirmed against these Nextcloud admin manual pages:
- https://docs.nextcloud.com/server/latest/admin_manual/maintenance/backup.html
Removed or reworded: claims the pages did not state (see the Check line and any softened wording).
Method: documentation only; no commands were run.
