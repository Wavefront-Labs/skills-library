---
id: computing-software.cloud-infrastructure-engineering.google-cloud.database-migration-service-mysql-postgresql-to-cloud-sql-and-alloydb
name: database-migration-service-mysql-postgresql-to-cloud-sql-and-alloydb
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, database-migration-service, dms-mysql, dms-postgresql, alloydb-migration, dms-to-alloydb, cdc, cutover]
level: advanced
status: docs-checked
description: "Migrate MySQL and PostgreSQL to Cloud SQL or AlloyDB with Database Migration Service: source prerequisites, continuous migration jobs with gcloud, and promotion at cutover."
sources: ["https://cloud.google.com/database-migration/docs/mysql/configure-source-database", "https://cloud.google.com/database-migration/docs/postgres/configure-source-database", "https://cloud.google.com/sdk/gcloud/reference/database-migration/migration-jobs"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DMS: MySQL and PostgreSQL to Cloud SQL and AlloyDB

## 1. Source prerequisites
| Engine | Needs |
|---|---|
| MySQL (self-hosted, per the one-time-migration source page) | InnoDB tables outside system schemas, `GTID_MODE` ON or OFF only, a dedicated user allowed from `host=%` with a password of at most 32 characters and `SELECT`, `SHOW VIEW`, `TRIGGER` (plus `RELOAD` when GTID is on) for the managed dump; user accounts are not migrated |
| PostgreSQL | `pglogical` installed (`shared_preload_libraries`) and `CREATE EXTENSION pglogical` in every migrated database, `wal_level='logical'`, `max_replication_slots` (default 10), `max_wal_senders` (default 10) and `max_worker_processes` (default 8) raised as the page's formulas require, `GRANT USAGE ON SCHEMA pglogical` and `SELECT` on tables and sequences for the migration user |
The MySQL page covers one-time migrations: check Google's continuous-migration source page for CDC prerequisites. Test the configuration with the migration job test (`verify`) before starting.

## 2. Connectivity
`--peer-vpc` on the job selects VPC peering to the source network. Other options (IP allowlist,
reverse SSH tunnel, Private Service Connect) are described on Google's connectivity pages.

## 3. Create and run
```bash
gcloud database-migration connection-profiles create postgresql src-pg --region=<R> \
  --host=10.1.2.3 --port=5432 --username=dms --password=<PW>
# destination: Cloud SQL (DMS can create it) or existing AlloyDB cluster profile
gcloud database-migration migration-jobs create orders-mig --region=<R> --type=CONTINUOUS \
  --source=src-pg --destination=dst-alloydb --peer-vpc=projects/<HOST>/global/networks/prod
gcloud database-migration migration-jobs verify orders-mig --region=<R>
gcloud database-migration migration-jobs start orders-mig --region=<R>
gcloud database-migration migration-jobs describe orders-mig --region=<R> --format='value(state,phase)'
```
A continuous job takes a full dump, then runs change data capture (CDC); wait for the CDC phase to catch up before cutover.

## 4. Cutover
1. Freeze writes on the source (app maintenance mode).
2. Wait for CDC to catch up; run row-count / checksum validations.
3. `gcloud database-migration migration-jobs promote orders-mig --region=<R>` to cut over to the destination.
4. Point apps at the destination; keep the source read-only for rollback window.

## Gotchas
- PostgreSQL: logical replication needs primary keys to replicate UPDATE and DELETE during CDC. For tables without them DMS migrates only the initial snapshot and later INSERTs; add primary keys first (or use the quick-start flow with `REPLICA IDENTITY`).
- MySQL: metadata with a `DEFINER` clause can block the migration because user accounts are not migrated; check it before starting.

## Verify
- [ ] Validation report shows matching row counts/checksums for all tables.
- [ ] Post-promotion app smoke tests pass; source writes are disabled.

## Checked
2026-10-31. Confirmed against the DMS MySQL and PostgreSQL source-configuration pages and the `gcloud database-migration migration-jobs` reference. Removed: binlog_format/binlog_row_image, REPLICATION privilege lists, the connectivity option list, DDL, sequence, large-object and retention claims, the Data Validation Tool pointer, lag-metric advice and the AlloyDB overview source (404).
Method: documentation only; no commands were run.
