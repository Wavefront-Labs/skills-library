---
id: computing-software.devops-ci-cd.forgejo.database-supported-engines-and-choice
name: database-supported-engines-and-choice
category: computing-software
field: devops-ci-cd
product: forgejo
tags: [database-support, sqlite3, mariadb, postgresql, database-recommendation]
level: intro
status: docs-checked
description: "Know which databases and minimum versions Forgejo supports and how to pick one by instance activity."
sources:
  - https://forgejo.org/docs/latest/admin/installation/database-preparation/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Forgejo supports four database families: MariaDB 10.6 or newer and MySQL 8.4 or newer (both with the InnoDB storage engine), PostgreSQL 14 or newer, and SQLite.

The recommendations page gives the selection rule for `[database].DB_TYPE`. For low to moderate activity, use `sqlite3`: it needs no maintenance and lives in one to three files on disk. For high activity, use `mysql` or `postgres`; neither is declared best and the choice mostly depends on your experience, since both handle large loads.

Be careful: changing to a different database later with an existing instance is not trivial and must be done carefully.

SQLite is built into the binary distributed by the Forgejo project, so no extra dependencies are needed. If you compile from source, build with `make TAGS="sqlite sqlite_unlock_notify" build`. Minimal configuration is `DB_TYPE = sqlite3` with an optional `PATH = data/forgejo.db`. No maintenance is expected, although running `VACUUM` can reclaim space after content is deleted if the file grows too large.

To investigate slow queries on any engine, lower `[database].SLOW_QUERY_THRESHOLD` below its 5 second default so moderately slow queries get logged.

## Checked

2026-11-04. Confirmed against the Forgejo Database Preparation page (supported list, SQLite section) and the Recommended Settings page ([database].DB_TYPE and the slow query tip): versions, InnoDB, sqlite build tags, VACUUM, the selection rule and the 5 second default. Removed: the advice to decide early.

Method: documentation only; no commands were run.
