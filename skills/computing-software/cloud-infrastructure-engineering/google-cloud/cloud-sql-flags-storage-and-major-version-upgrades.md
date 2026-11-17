---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cloud-sql-flags-storage-and-major-version-upgrades
name: cloud-sql-flags-storage-and-major-version-upgrades
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-sql, database-flags, cloud-sql-flags, cloud-sql-storage-autoresize, storage-full, cloud-sql-upgrade, major-version-upgrade, postgresql, mysql]
level: practitioner
status: gated
description: "Change Cloud SQL configuration safely: database flags (and the patch-replaces-all trap), storage auto-increase, disk-full recovery, major version upgrades rehearsed on a clone."
sources: ["https://cloud.google.com/sql/docs/postgres/flags", "https://cloud.google.com/sql/docs/mysql/instance-settings#automatic-storage-increase-2ndgen", "https://cloud.google.com/sql/docs/postgres/upgrade-major-db-version-inplace", "https://cloud.google.com/sql/docs/mysql/upgrade-major-db-version-inplace"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud SQL flags, storage and major version upgrades

## 1. Database flags
```bash
gcloud sql instances describe db1 --format='value(settings.databaseFlags)'
gcloud sql instances patch db1 \
  --database-flags=max_connections=400,log_min_duration_statement=500,cloudsql.iam_authentication=on
```
**`--database-flags` replaces the entire flag list** — always include existing flags (or use
Terraform where the full set is declared). `--clear-database-flags` removes all. Some flags restart
the instance (`max_connections` on PostgreSQL, `innodb_buffer_pool_size` (gated: unconfirmed, source is paywalled or blocked) changes on MySQL) —
patch in a maintenance window. Only supported flags are accepted; tiers cap some values.
Useful: PostgreSQL `cloudsql.enable_pgaudit`, `log_lock_waits`, `pg_stat_statements` via extension;
MySQL `slow_query_log=on`, `long_query_time=1`, `log_output=FILE`.

## 2. Storage
```bash
gcloud sql instances patch db1 --storage-auto-increase --storage-auto-increase-limit=2000   # GB cap
```
- Storage never shrinks; auto-increase grows permanently. Investigate *why* it grew (bloat, binlogs/WAL retention, temp files from bad queries).
- Alert on `cloudsql.googleapis.com/database/disk/utilization > 0.85`.
- Disk full: MySQL/PostgreSQL stop accepting writes. Fix: `gcloud sql instances patch db1 --storage-size=<bigger>`, then find growth (`pg_database_size` (gated: unconfirmed, source is paywalled or blocked), `SHOW BINARY LOGS`, PITR log retention `--retained-transaction-log-days`).

## 3. In-place major upgrade
```bash
# rehearse on a clone
gcloud sql instances clone db1 db1-upgrade-test
gcloud sql instances patch db1-upgrade-test --database-version=POSTGRES_16
# run app tests / extension checks against the clone, then:
gcloud sql instances patch db1 --database-version=POSTGRES_16
gcloud sql operations list --instance=db1 --limit=3
```
- A pre-upgrade backup is taken automatically; keep it until you're confident.
- PostgreSQL: incompatible extensions, `reg*` data types and unlogged/partitioned edge cases fail the pre-check — the operation error lists them. Run `ANALYZE` after upgrade (statistics are not carried over).
- MySQL 5.7 → 8.0: check reserved words, `utf8mb4` defaults, authentication plugin changes in clients.
- Read replicas have engine-specific rules (upgrade order or recreation) — read the page for your engine before upgrading the primary.

## Gotchas
- Upgrades mean downtime (minutes to tens of minutes on big instances); there's no rollback except restoring the pre-upgrade backup into a new instance.
- Changing tier and flags in one patch makes failures hard to attribute; one change per patch.

## Verify
- [ ] `gcloud sql instances describe db1 --format='value(databaseVersion,settings.storageAutoResize,settings.databaseFlags)'` matches the change record.
- [ ] App test suite passes against the upgraded clone before prod.

## Checked

2026-10-27. Confirmed: flags and commands against the gcloud reference pages, the product guides cited in sources, IAM roles pages, and API discovery documents for enums. Removed: nothing removed; flags were checked against the gcloud reference pages. Gated: the innodb_buffer_pool_size and pg_database_size names were not found in the fetched pages.

Method: documentation only; no commands were run.
