---
id: computing-software.cybersecurity-defensive.keycloak.upgrade-prep-and-db-migration
name: upgrade-prep-and-db-migration
category: computing-software
field: cybersecurity-defensive
product: keycloak
tags: [cybersecurity-defensive, keycloak, upgrade, database-migration, liquibase, migration-strategy]
level: practitioner
status: docs-checked
description: "Upgrade Keycloak safely: stop old nodes, handle automatic or manual schema migration, index threshold, timeout and no-rollback rules."
sources:
  - https://github.com/keycloak/keycloak/blob/main/docs/documentation/upgrading/topics/migrate_db.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# upgrade prep and db migration
Keycloak can migrate the database schema automatically, or you can do it manually. Shut down all nodes running the old version before migrating. Migration is not supported with the default H2 `dev-file` database type.

- By default the schema migrates automatically when the new version starts for the first time.
- The default migration timeout is 30 minutes; extend it with `kc.sh start --transaction-setup-timeout=60m`.
- Large tables: a threshold of `300000` records applies to automatic migration. Above it, index creation is skipped during schema migration. On databases with non-blocking index creation (PostgreSQL, Oracle Enterprise Edition, MySQL/MariaDB, SQL Server Enterprise, Developer or Azure SQL editions) Keycloak creates the skipped indexes in the background after startup; on other databases a warning is logged with the SQL to apply manually. Set `--spi-connections-jpa--quarkus--auto-create-missing-indexes=false` to log the SQL instead of creating them.
- Tune the threshold with `--spi-connections-liquibase--quarkus--index-creation-threshold=300000`; zero or a negative number disables the feature.
- Manual migration: `--spi-connections-jpa--quarkus--migration-strategy=manual`. The server checks whether migration is needed, writes the changes to `keycloak-database-update.sql` in the working directory (path via `--spi-connections-jpa--quarkus--migration-export`), and exits. A DBA reviews and runs the SQL, then you start the new version; the first startup may perform further data migrations.
- Even with the manual strategy, Keycloak creates the Liquibase bookkeeping tables `DATABASECHANGELOG` and `DATABASECHANGELOGLOCK` itself on the database it generates the script against, so use a database user allowed to create tables there or create them up front.

Customised themes: compare each changed template, message and stylesheet against the new base theme with a diff tool (upgrading guide, themes section).

## Checked
2026-11-03. Confirmed against the upgrading guide pages migrate_db.adoc and migrate_themes.adoc: H2 dev-file limitation, 30 minute timeout and `transaction-setup-timeout`, 300000 threshold, supported non-blocking databases, the three option names, manual strategy and SQL file, bookkeeping tables. Removed (not on the pages read): rollback and backup advice, the 26.6.0 rolling-update statement, `persistent-user-sessions` and brute-force storage notes, the provider-rebuild note and the invented Verify step.
Method: documentation only; no commands were run.
