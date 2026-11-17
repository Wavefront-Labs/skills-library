---
id: computing-software.collaboration-platform-administration.nextcloud.mysql-4byte-support-and-emoji
name: mysql-4byte-support-and-emoji
category: computing-software
field: collaboration-platform-administration
product: nextcloud
tags: [utf8mb4, mysql, mariadb, emoji, maintenance-repair]
level: advanced
status: docs-checked
description: "Convert a Nextcloud MySQL or MariaDB database to utf8mb4 for emoji and rare scripts using innodb_file_per_table, ALTER DATABASE and occ maintenance:repair."
sources:
  - https://docs.nextcloud.com/server/latest/admin_manual/configuration_database/mysql_4byte_support.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: store emoji and other characters outside the Basic Multilingual Plane. The older three-byte `utf8` cannot hold them.

Applies only to MySQL 8 or newer and MariaDB 10.6 or newer. Back up the database first.

1. Enable InnoDB per-table files in the server config, then restart the database server:

```
[mysqld]
innodb_file_per_table=1
```

Verify with `SHOW VARIABLES LIKE 'innodb_file_per_table';` which must show `ON`.

2. Turn on maintenance mode in the install directory:

```
sudo -E -u www-data php occ maintenance:mode --on
```

3. Change the database default:

```
ALTER DATABASE nextcloud CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
```

The character set decides what can be stored; the collation decides how text is compared and sorted.

4. Enable it in Nextcloud:

```
sudo -E -u www-data php occ config:system:set mysql.utf8mb4 --type boolean --value="true"
```

5. Convert existing tables. This also changes every table's `ROW_FORMAT` to `DYNAMIC`:

```
sudo -E -u www-data php occ maintenance:repair
```

6. Turn maintenance mode off.

Result: file names, calendar events and comments can use the full Unicode range.

Remember afterwards that dumps and restores must also use `utf8mb4` (see database-dump-commands-per-engine).

Check: create a file named with an emoji and see it listed without errors.

## Checked

2026-11-03. Confirmed against these Nextcloud admin manual pages:
- https://docs.nextcloud.com/server/latest/admin_manual/configuration_database/mysql_4byte_support.html
Removed or reworded: claims the pages did not state (see the Check line and any softened wording).
Method: documentation only; no commands were run.
