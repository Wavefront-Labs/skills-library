---
id: computing-software.cloud-infrastructure-engineering.azure.dms-postgresql-and-mysql-migration-to-azure
name: dms-postgresql-and-mysql-migration-to-azure
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, migration, database-migration-service, dms, postgresql-migration, mysql-migration, postgresql-flexible-server, mysql-flexible-server, online-migration, logical-replication, binlog, data-in-replication, pg-dump]
level: advanced
status: docs-checked
description: "Migrate on-prem or other-cloud PostgreSQL and MySQL to Azure flexible servers: migration service, DMS, dump/restore and replication-based near-zero-downtime cutover."
sources: ["https://learn.microsoft.com/en-us/azure/postgresql/migrate/migration-service/overview-migration-service-postgresql", "https://learn.microsoft.com/en-us/azure/postgresql/migrate/migration-service/best-practices-migration-service-postgresql", "https://learn.microsoft.com/en-us/cli/azure/postgres/flexible-server/migration", "https://learn.microsoft.com/en-us/azure/mysql/flexible-server/concepts-data-in-replication"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PostgreSQL and MySQL migration into Azure

**Goal:** move a self-managed PostgreSQL or MySQL (on-prem, VMs, AWS RDS, GCP Cloud SQL) to
Azure flexible server with validated data and a cutover measured in minutes.

## 1. Choose the path
| Size / downtime budget | PostgreSQL | MySQL |
|---|---|---|
| Small, hours of downtime OK | native dump and restore | `mydumper`/`myloader` (parallel) |
| Any size, minutes of downtime | **Migration service in Flexible Server** (online) | **Data-in replication** after a `mydumper`/`myloader` load; for migrations Microsoft points to Azure Database Migration Service |
| Version jump | allowed: flexible server supports all major versions from 11; test extensions and app | source must be MySQL 5.7 or later; same version on source and replica is recommended; test `sql_mode` and the app |

## 2. PostgreSQL via migration service
The service is managed, handles schema and data, has no database size limit (classic DMS had a 1-TB limit), and uses
`pgcopydb` underneath. Sources supported offline and online: on-premises, Azure VM, Amazon RDS, Amazon Aurora,
Google Cloud SQL. Online migration needs a **primary key** on every table and loads the source for as long as it runs.
```bash
az postgres flexible-server migration create -g rg-data -s pgflex-prod --name mig-onprem \
  --properties migration.json --migration-mode online --migration-option ValidateAndMigrate
az postgres flexible-server migration show -g rg-data -s pgflex-prod --name mig-onprem
az postgres flexible-server migration update -g rg-data -s pgflex-prod --name mig-onprem --cutover
```
- `--migration-mode` is `offline` (default) or `online` (with CDC); `--migration-option` is `Migrate`, `Validate` or
  `ValidateAndMigrate`. `Validate` runs the premigration checks only.
- In the properties file, `sourceType` and `sslMode` are required for any source other than a PostgreSQL single server.
  `sourceType` values: `OnPremises`, `AWS_AURORA`, `AWS_RDS`, `AzureVM`, `PostgreSQLSingleServer`. `overwriteDbsInTarget`
  defaults to true, so an existing target database with the same name is overwritten.

## 3. MySQL near-zero downtime
1. Source: MySQL 5.7 or later, InnoDB, a primary key on each table (otherwise replication can be slow), and binary logs
   not purged before the replica has applied them. Allow traffic on port 3306 both ways.
2. Initial load with `mydumper` then `myloader` into the flexible server, recording the binlog position or GTID.
3. Start replication on the target with `CALL mysql.az_replication_change_master(...)` (position based) or
   `mysql.az_replication_change_master_with_gtid` (the only option on HA-enabled servers). Follow the Data-in
   replication how-to page for the full argument list and the start and stop procedures.
4. Cut over when replica lag is zero.
- The `mysql` system database and account/permission changes on the source are not replicated: create needed accounts
  on the target by hand.
- Data-in replication is not supported when the target has private endpoint only (public access disabled).
- On MySQL 8.0+ Generated Invisible Primary Keys are on by default and can break replication of tables without a
  primary key (errors 1068 and 1075); the page gives the mitigation.

## 4. Cutover
Stop writes on source, wait for lag 0, cut over (PostgreSQL: `migration update --cutover`), validate row counts, switch
connection strings, keep the source read-only for rollback.

## Verify
- [ ] Validation report clean; replication lag ~0 for at least one business-peak period before cutover.
- [ ] Row counts and checksums on key tables match; sequences/auto-increment values ahead of max IDs.
- [ ] App runs against the target; source retained read-only through the rollback window.

## Checked
2026-10-31. Confirmed against the PostgreSQL migration service overview, `az postgres flexible-server migration`
reference and the MySQL Data-in replication concept page: the CLI flags, mode/option values, `sourceType` values,
primary-key requirement, 1-TB classic limit, source version 5.7, HA/GTID procedure, private-endpoint limitation, GIPK
errors. Removed as unconfirmed: logical replication source settings, role and extension handling, large-object
and DDL caveats, `az_replication_start`/`stop`/`remove_master` details, dump tool flags, the dead DMS MySQL tutorial URL,
and `--migration-name` (the flag is `--name`; the server flag is `--server-name`/`-s`).
Method: documentation only; no commands were run.
