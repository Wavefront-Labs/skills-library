---
id: computing-software.collaboration-platform-administration.nextcloud.convert-sqlite-to-production-database
name: convert-sqlite-to-production-database
category: computing-software
field: collaboration-platform-administration
product: nextcloud
tags: [db-convert-type, sqlite, mariadb, postgresql, occ]
level: practitioner
status: docs-checked
description: "Move a Nextcloud install from SQLite to MariaDB, MySQL or PostgreSQL with occ db:convert-type, covering the options and the follow-up utf8mb4 setting."
sources:
  - https://docs.nextcloud.com/server/latest/admin_manual/configuration_database/db_conversion.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: replace SQLite, fine for testing and single-user servers, with a database that scales to multiple users.

Two steps: create the empty target database with its credentials (following the manual MySQL or PostgreSQL setup), then run the converter.

Syntax:

```
sudo -E -u www-data php occ db:convert-type [options] type username hostname database
```

`type` takes the same values as `dbtype` in `config.php`: `mysql`, `pgsql`, or `oci` for Oracle.

Options:
- `--port="3306"`: database port, default 3306
- `--password`: new database password; omitted, the tool asks
- `--clear-schema`: clear the schema
- `--all-apps`: also convert tables of deactivated apps (tables of removed apps are never converted)
- `-n, --no-interaction`: no prompts

Example, converting to MariaDB or MySQL:

```
sudo -E -u www-data php occ db:convert-type --password="<password>" --port="3306" --all-apps mysql <username> <hostname> nextcloud
```

The tool uses the apps' schema definitions to create the new tables. On success it writes the new database settings into `config.php` for you; look for the `db*` parameters to review them.

Afterwards, for MySQL or MariaDB set:

```
sudo -E -u www-data php occ config:system:set mysql.utf8mb4 --type boolean --value="true"
```

and see mysql-4byte-support-and-emoji for the database side.

Check: log in and confirm files, shares and apps are intact; `config.php` shows the new `dbtype`.

## Checked

2026-11-03. Confirmed against these Nextcloud admin manual pages:
- https://docs.nextcloud.com/server/latest/admin_manual/configuration_database/db_conversion.html
Removed or reworded: claims the pages did not state (see the Check line and any softened wording).
Method: documentation only; no commands were run.
