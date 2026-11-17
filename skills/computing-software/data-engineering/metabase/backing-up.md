---
id: computing-software.data-engineering.metabase.backing-up
name: backing-up
category: computing-software
field: data-engineering
product: metabase
tags: [backup, application-database-backup, h2-file, rds-backups, restore]
level: intro
status: docs-checked
description: "Back up Metabase application data: what the application database holds, copying the H2 file for JAR and Docker installs, RDS backups, and what the docs leave out."
sources:
  - https://www.metabase.com/docs/latest/installation-and-operation/backing-up-metabase-application-data
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
What to back up: the application database. Metabase keeps all runtime application data (questions, dashboards, collections) in a single SQL database, so that is the one thing to protect.

Default H2 (embedded):
- The file is `metabase.db.mv.db` in the Metabase directory.
- JAR: stop Metabase, copy `metabase.db.mv.db` somewhere safe, then restart with `java --add-opens java.base/java.nio=ALL-UNNAMED -jar metabase.jar`.
- Docker: copy the file out of the container, for example `docker cp metabase:/metabase.db/metabase.db.mv.db ./` where `metabase` is the container name.
- If you have content worth keeping, migrate to a production database before upgrading.

Amazon RDS: enable automated RDS backups and follow the AWS guide for backup and restore.

Self-hosted PostgreSQL: use PostgreSQL's own backup documentation.

Gaps in the page:
- It gives no `pg_dump` or `mysqldump` commands, no MySQL guidance and no restore steps.
- It says a backup lets you recover "if anything goes wrong (like during an upgrade)", with no detail.
- Cloud backups are not covered.

## Checked
2026-11-03. Confirmed against the Metabase docs page Installation and operation, Backing up Metabase application data: single application database, metabase.db.mv.db, docker cp example, JAR stop/copy/restart steps, RDS automated backups, self-hosted PostgreSQL deferral. Removed the unsupported closing advice about serialization and upgrades (the page does not say it).
Method: documentation only; no commands were run.
