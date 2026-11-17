---
id: computing-software.cloud-infrastructure-engineering.google-cloud.spanner-schema-and-scaling
name: spanner-schema-and-scaling
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, spanner, cloud-spanner, processing-units, nodes, multi-region-spanner, interleaved-tables, hotspotting, uuid-primary-keys, secondary-indexes, autoscaler, spanner-autoscaler, pitr-spanner, spanner-backups, googlesql, postgresql-dialect, spanner-emulator, change-streams, key-visualizer]
level: advanced
status: docs-checked
description: "Run Spanner well: size by processing units, regional vs multi-region configs, keys that avoid hotspots, interleaving and indexes, autoscaling, backups with PITR, and reading Key Visualizer."
sources: ["https://docs.cloud.google.com/spanner/docs/compute-capacity", "https://docs.cloud.google.com/spanner/quotas", "https://docs.cloud.google.com/spanner/docs/instance-configurations", "https://docs.cloud.google.com/spanner/docs/schema-design", "https://docs.cloud.google.com/spanner/docs/primary-key-default-value", "https://docs.cloud.google.com/spanner/docs/pitr", "https://docs.cloud.google.com/sdk/gcloud/reference/spanner/instances/create", "https://docs.cloud.google.com/sdk/gcloud/reference/spanner/backups/create", "https://docs.cloud.google.com/sdk/gcloud/reference/spanner/databases/restore"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spanner schema and scaling

**Goal:** a globally consistent relational database that scales linearly because the schema
spreads writes, with capacity that follows load and a recovery story that has been tested.

## 1. Size and place
- Capacity in **processing units** (PU): 1000 PU = 1 node; below 1000 PU use multiples of 100, from 1000 PU use multiples of 1000. Spanner allots 10 TiB of storage per node (1024 GiB per 100 PU below one node). Keep CPU under 65% for regional instances and 45% per region for multi-region instances when sizing or reducing capacity.
- **Instance config**: regional (`regional-europe-west1`, at least 99.99% availability) vs multi-region (`eur6`, `nam3`, `nam-eur-asia1`, 99.999% availability; writes see a small latency increase) and dual-region configs (also 99.999%). Choose multi-region or dual-region only when you need the higher availability or wider read locations.
- Editions (Standard, Enterprise, Enterprise Plus) gate features; confirm the current edition matrix before choosing.
```bash
gcloud spanner instances create prod --config=regional-europe-west1 --description=prod --processing-units=1000 --edition=ENTERPRISE
gcloud spanner databases create app --instance=prod --database-dialect=GOOGLE_STANDARD_SQL \
  --ddl-file=schema.sql
```

## 2. Keys that do not hotspot
Spanner splits by primary key range; monotonically increasing keys (timestamps, auto-increment) put every write on the last split.
- Use **UUIDv4** keys (for example `DEFAULT (NEW_UUID())`), or a hash prefix / bit-reversed sequence (`CREATE SEQUENCE s OPTIONS (sequence_kind="bit_reversed_positive")` + `DEFAULT (GET_NEXT_SEQUENCE_VALUE(SEQUENCE s))`).
- Timestamp-first keys → reverse the timestamp or prefix with a shard id (`ShardId INT64` = hash % N) and query with `WHERE ShardId IN UNNEST(...)`.
- Same rule for **secondary indexes**: a non-interleaved index on a monotonically increasing column such as `CreatedAt` is a hotspot; include a sharding column or interleave the index under a parent row.
- **Interleave** child tables in the parent (`INTERLEAVE IN PARENT Customers ON DELETE CASCADE`) when they are always read together (customer → orders); interleaving depth is limited to 7.
- Limits: 10 MiB per cell, 1,600 MiB total non-key data per row, 8 KiB per primary or index key, 1,024 columns per table.
- `NULL_FILTERED` indexes and `STORING (col)` covering indexes avoid back-joins; `FORCE_INDEX` hints when the optimiser guesses wrong.

## 3. Transactions
- Read-write transactions take locks; keep them short and retry on `ABORTED` (client libraries do this inside their transaction runner).
- Use stale reads for workloads that tolerate older data (for example dashboards).
- Use Partitioned DML for bulk updates that are idempotent.
- A commit is limited to 80,000 mutations (including index mutations); chunk bulk loads.

## 4. Autoscale, back up, observe
- **Managed autoscaler** flags on instance create/update: `--autoscaling-min-processing-units` and `--autoscaling-max-processing-units` (or the node equivalents), `--autoscaling-high-priority-cpu-target` and/or `--autoscaling-total-cpu-target`, and `--autoscaling-storage-target` (required when any autoscaling flag is set).
- Backups: `gcloud spanner backups create bk --instance=prod --database=app --retention-period=14d` (exactly one of `--retention-period` or `--expiration-date`; 6 hours to 30 days; optional `--version-time`). Restore with `gcloud spanner databases restore --source-backup=... --source-instance=... --destination-database=... --destination-instance=...` (always to a new database). **PITR**: the database retains versions for one hour by default and up to seven days via the `version_retention_period` option; recover with a stale read, or by backing up or exporting at a past timestamp and restoring to a new database.
- **Key Visualizer** (console) shows heat by key range over time: a single bright diagonal line indicates sequential keys; persistent bright horizontal bands indicate heavily used row ranges.
- **Change streams** (`CREATE CHANGE STREAM all_changes FOR ALL`) feed Dataflow → BigQuery/Pub/Sub for CDC without triggers.
- Introspection tables: `SPANNER_SYS.LOCK_STATS_TOP_MINUTE` and `SPANNER_SYS.QUERY_STATS_TOP_MINUTE`.

## Gotchas
- When reducing capacity, watch CPU and request latency in Cloud Monitoring and keep CPU under the thresholds above.
- PITR does not protect against database deletion; enable deletion protection.
- Choose the database dialect (`GOOGLE_STANDARD_SQL` or `POSTGRESQL`) when creating the database.
- The emulator (`gcloud emulators spanner start`, `SPANNER_EMULATOR_HOST`) has no IAM, authentication, TLS, drop protection or audit logging, returns empty query plans and keeps data in memory only; use it for tests, not for performance or security checks.

## Verify
- [ ] Key Visualizer after a load test shows even heat across key ranges, no diagonal.
- [ ] The autoscaler adds PUs when CPU passes the target.
- [ ] A restore from a backup taken at a known version time returns the expected row count.

## Checked
Checked 2026-10-24 against the Spanner compute-capacity, quotas, instance-configurations, schema-design, primary-key default value, PITR overview, Key Visualizer patterns and emulator pages, and the gcloud `spanner instances create`, `databases create`, `backups create` and `databases restore` references (docs.cloud.google.com). Wrong claims fixed: storage is 10 TiB per node (not 4 TB), instances need not start at 1000 PU, the per-cell limit is 10 MiB with 1,600 MiB of non-key data per row (not 10 MB per row), and `databases restore` has no `--version-time` flag (PITR goes through backups with `--version-time`). Removed throughput-per-node figures, the 2x/3x multi-region latency and cost multipliers, `GENERATE_UUID()` (the primary-key page documents `NEW_UUID()`), `--enable-drop-protection` on `databases create`, the open-source autoscaler, interleave size advice and unconfirmed emulator and dialect remarks.
Method: documentation only; no commands were run.
