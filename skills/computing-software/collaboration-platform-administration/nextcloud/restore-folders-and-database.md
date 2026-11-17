---
id: computing-software.collaboration-platform-administration.nextcloud.restore-folders-and-database
name: restore-folders-and-database
category: computing-software
field: collaboration-platform-administration
product: nextcloud
tags: [restore, rsync, drop-database, mariadb, postgresql]
level: practitioner
status: docs-checked
description: "Restore a Nextcloud backup by copying config and data folders back, dropping and recreating the database, and loading the dump for your engine."
sources:
  - https://docs.nextcloud.com/server/latest/admin_manual/maintenance/restore.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: bring back a full instance from a backup made earlier.

You need all of the database, the data directory and the configuration files (plus the theme directory). Restoration cannot complete without the first three.

Folders. Copy the config and data folders (or the whole install and data folder) into the Nextcloud environment:

```
rsync -Aax nextcloud-dirbkp/ nextcloud/
```

Database. Existing tables must be deleted first. The easiest way is to drop and recreate the database; SQLite does this automatically.

MariaDB or MySQL (use `mysql` in place of `mariadb` for MySQL):

```
mariadb -h [server] -u [username] -p[password] -e "DROP DATABASE nextcloud"
mariadb -h [server] -u [username] -p[password] -e "CREATE DATABASE nextcloud"
mariadb -h [server] -u [username] -p[password] [db_name] < nextcloud-sqlbkp.bak
```

With emoji (4-byte) support, create it with `CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci`.

PostgreSQL:

```
PGPASSWORD="password" psql -h [server] -U [username] -d template1 -c "DROP DATABASE \"nextcloud\";"
PGPASSWORD="password" psql -h [server] -U [username] -d template1 -c "CREATE DATABASE \"nextcloud\";"
PGPASSWORD="password" psql -h [server] -U [username] -d nextcloud -f nextcloud-sqlbkp.bak
```

SQLite: `rm data/owncloud.db` then `sqlite3 data/owncloud.db < nextcloud-sqlbkp.bak`.

Afterwards read client-resync-after-restore, because stale backups need extra steps.

Check: log in, open the admin overview and confirm no setup warnings about missing tables.

## Checked

2026-11-03. Confirmed against these Nextcloud admin manual pages:
- https://docs.nextcloud.com/server/latest/admin_manual/maintenance/restore.html
Removed or reworded: claims the pages did not state (see the Check line and any softened wording).
Method: documentation only; no commands were run.
