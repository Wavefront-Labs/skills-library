---
id: computing-software.collaboration-platform-administration.nextcloud.database-dump-commands-per-engine
name: database-dump-commands-per-engine
category: computing-software
field: collaboration-platform-administration
product: nextcloud
tags: [mariadb-dump, mysqldump, single-transaction, utf8mb4, database-backup]
level: practitioner
status: docs-checked
description: "Dump a Nextcloud database with mariadb-dump or mysqldump using --single-transaction, and add utf8mb4 charset when 4-byte support is on."
sources:
  - https://docs.nextcloud.com/server/latest/admin_manual/maintenance/backup.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: produce a consistent database dump while Nextcloud is in maintenance mode.

MariaDB is the recommended database engine. Use `mariadb-dump`:

```
mariadb-dump --single-transaction -h [server] -u [username] -p[password] [db_name] > nextcloud-sqlbkp_`date +"%Y%m%d"`.bak
```

MySQL uses the same flags with `mysqldump`:

```
mysqldump --single-transaction -h [server] -u [username] -p[password] [db_name] > nextcloud-sqlbkp_`date +"%Y%m%d"`.bak
```

If you enabled 4-byte support (needed for emoji), add the character set to either command, otherwise the dump may not round-trip:

```
--default-character-set=utf8mb4
```

See mysql-4byte-support-and-emoji for how that is turned on.

Notes:
- `--single-transaction` takes the dump inside one transaction, so tables are read at a consistent point.
- SQLite: `sqlite3 data/owncloud.db .dump > nextcloud-sqlbkp_`date +"%Y%m%d"`.bak`
- PostgreSQL: `PGPASSWORD="password" pg_dump [db_name] -h [server] -U [username] -f nextcloud-sqlbkp_`date +"%Y%m%d"`.bak`
- Do the dump after `occ maintenance:mode --on` and before turning it off.

Check: the dump file is non-empty and has a date-stamped name beside the folder copy.

## Checked

2026-11-03. Confirmed against these Nextcloud admin manual pages:
- https://docs.nextcloud.com/server/latest/admin_manual/maintenance/backup.html
Removed or reworded: claims the pages did not state (see the Check line and any softened wording).
Method: documentation only; no commands were run.
