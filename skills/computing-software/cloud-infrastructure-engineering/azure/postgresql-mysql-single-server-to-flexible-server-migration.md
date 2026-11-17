---
id: computing-software.cloud-infrastructure-engineering.azure.postgresql-mysql-single-server-to-flexible-server-migration
name: postgresql-mysql-single-server-to-flexible-server-migration
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, postgresql-flexible-server, mysql-flexible-server, single-server-migration, single-to-flexible, migration-service, online-migration, offline-migration, logical-replication, cutover, open-source-databases]
level: advanced
status: docs-checked
description: "Migrate Azure Database for PostgreSQL/MySQL Single Server to Flexible Server: migration service offline/online, pre-checks, users and extensions, cutover and rollback."
sources: ["https://learn.microsoft.com/en-us/azure/postgresql/migrate/migration-service/overview-migration-service-postgresql", "https://learn.microsoft.com/en-us/azure/postgresql/migrate/migration-service/tutorial-migration-service-single-to-flexible", "https://learn.microsoft.com/en-us/azure/mysql/migrate/whats-happening-to-mysql-single-server", "https://learn.microsoft.com/en-us/cli/azure/postgres/flexible-server/migration"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Single Server → Flexible Server migration (PostgreSQL / MySQL)

**Goal:** move every database off the retired Single Server platform onto Flexible Server
with tested cutover, minimal downtime and a rollback window.

## 1. Plan the target
- Map SKU, storage and major version to the target, and test the application against the target version.
- Decide networking (private access or public access with private endpoint) before creating the target.
- Carry over non-default server parameters and required extensions before migrating; the premigration validations page lists what is checked.
- Update connection strings for the new server host name and login format.

## 2. PostgreSQL migration service
```bash
# migration.json: source server id, credentials, databases to migrate and migration mode (schema is in the migration service tutorial)
az postgres flexible-server migration create -g rg-data -s pgflex-prod -n mig-orders --properties migration.json
az postgres flexible-server migration show   -g rg-data -s pgflex-prod -n mig-orders
az postgres flexible-server migration update -g rg-data -s pgflex-prod -n mig-orders --cutover   # online: when lag ~0
```
- **Validate** first (`--migration-option Validate`, or in the portal); the premigration validations page lists what is checked.
- **Offline**: applications stop and databases are copied to the flexible server. **Online**: initial copy plus replication, with limited downtime; online has restrictions (for example primary keys are required in all tables), and the CLI reference notes that setting up logical replication on the source restarts the source server.

## 3. MySQL
- Azure Database Migration Service is one supported route to MySQL flexible server; see the MySQL migration docs for current options, and test `sql_mode`, collation and version differences on the target before cutover.

## 4. Cutover and rollback
1. Freeze writes (app maintenance mode / revoke write on source).
2. Wait for lag 0 → trigger cutover; compare row counts/checksums on key tables.
3. Switch connection strings (new hostname `<name>.postgres.database.azure.com`),
   restart apps, run smoke tests.
4. Keep the Single Server stopped (not deleted) for the rollback window; delete after sign-off.

## Gotchas
- Online replication requires primary keys in all tables; handle other cases separately or go offline.
- Firewall: the target must reach the source (public access rules or private connectivity) during migration.

## Verify
- [ ] Validation passes with no errors; the migration shows as completed for every database.
- [ ] Row counts and sequence values match; app passes smoke tests against the Flexible server.
- [ ] Single Server stopped; monitoring, backups and alerts configured on the Flexible server.

## Checked
2026-10-28. Confirmed on the `az postgres flexible-server migration` reference (the server is `--server-name/-s`, the migration is `--name/-n`, `--properties`, `--migration-mode {offline, online}`, `--migration-option {Migrate, Validate, ValidateAndMigrate}`, `--cutover`) and the migration service overview (offline vs online, primary keys required online, logical replication setup restarts the source). Fixed: the commands used a nonexistent `--migration-name` flag.
Removed (not confirmed): the properties JSON keys, SKU/storage/version rules, networking lock-in, `azure.extensions` and `azure.replication_support`, sequence and large-object gotchas, role migration, pg_dump alternative, mydumper route and retirement remarks.

Method: documentation only; no commands were run.
