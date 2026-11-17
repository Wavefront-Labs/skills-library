---
id: computing-software.systems-network-administration.paperless-ngx.mariadb-case-and-timezones
name: mariadb-case-and-timezones
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, mariadb, mysql, collation, timezone, utf8mb4]
level: advanced
status: docs-checked
description: "MariaDB and MySQL caveats for Paperless-ngx: case-insensitive tags, optional case sensitivity, utf8mb4, and loading timezone tables."
sources:
  - "https://docs.paperless-ngx.com/advanced_usage/"
  - "https://docs.paperless-ngx.com/migration-v3/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MariaDB and MySQL caveats

## Case sensitivity
The database interface cannot make a MySQL database case-sensitive for you. A case-insensitive database prevents creating tags `Name` and `NAME`, because they are considered the same.

Turning case sensitivity on has a downside: searches become case-sensitive too, so a document titled `Invoice` is not found by `invoice`. Django requires manual action per table:
```sql
ALTER TABLE <table_name> CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;
ALTER DATABASE <db_name> CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;
```
The second statement only affects tables created afterwards.

## Character set
Use MariaDB 10.4 or newer. The `utf8mb3` set may smooth some setup problems but can break consumption; `utf8mb4` does not.

## Missing timezones
MySQL and MariaDB ship without timezone data, which causes unexpected behavior with date-based queries (some Docker images, such as the official MariaDB image, take care of this for you). Load it from the system zoneinfo:
```bash
mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root mysql -p
mariadb-tzinfo-to-sql /usr/share/zoneinfo | mariadb -u root mysql -p
```
Use the first for MySQL, the second for MariaDB.

Remember that v3 requires `PAPERLESS_DBENGINE=mariadb` to be set explicitly.

## Checked
2026-11-04. Compared with the MySQL Caveats section (case sensitivity, character set, missing timezones) of advanced usage and the v3 migration page (Markdown source of the Paperless-ngx docs; the rendered site blocks scripts). Confirmed: case-sensitivity downside and both statements, MariaDB 10.4 recommendation and utf8mb3 warning, timezone commands. Reworded two sentences that overstated the page (default collation, timezone data breaks queries).

Method: documentation only; no commands were run.
