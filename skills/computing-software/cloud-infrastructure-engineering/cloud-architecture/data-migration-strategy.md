---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.data-migration-strategy
name: data-migration-strategy
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, cloud-migration, data-migration-strategy, change-data-capture, offline-transfer, database-migration]
level: advanced
status: draft
description: "Choose a data migration method for cloud moves: offline bulk, online replication, CDC with cutover, or devices; size bandwidth, validate data and plan the switch."
sources: ["https://docs.aws.amazon.com/dms/latest/userguide/Welcome.html", "https://learn.microsoft.com/azure/dms/dms-overview", "https://cloud.google.com/database-migration/docs", "https://debezium.io/documentation/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Data migration strategy (offline / online / CDC)

## Choose by downtime tolerance and volume
| Method | Downtime | Use when |
|---|---|---|
| dump and restore (offline) | hours, proportional to size | small DBs, generous window |
| full load + CDC (online) | minutes at cutover | most production databases |
| native replication (log shipping, logical replication, read replica promotion) | minutes | same engine, supported versions |
| transfer devices (Snowball, Data Box, Transfer Appliance) | days of shipping | tens of TB+ over thin links |
| online file sync (DataSync, AzCopy, Storage Transfer Service) | incremental, final delta | file and object data |

## Steps
1. **Bandwidth math**: days = data (TB) x 8,000,000 / (Mbps x 86,400 x 0.8 efficiency).
   10 TB over 1 Gbps is about 1.2 days; over 100 Mbps about 12 days. Above roughly a week, use devices or seed then sync.
2. **Schema and engine changes**: heterogeneous moves (Oracle to PostgreSQL) need schema
   conversion (AWS SCT / DMS Schema Conversion, ora2pg) and code changes; test separately from the data move.
3. **CDC prerequisites**: binary logging / supplemental logging / logical replication
   enabled, primary keys on all tables (CDC tools struggle without them), LOB handling settings.
4. **Validate**: row counts, checksums per table or partition (DMS data validation),
   application-level reconciliation queries.
5. **Cutover**: stop writes, let CDC drain to zero lag, final validation, switch connection
   strings / DNS, keep reverse replication if rollback must preserve new writes.

## Gotchas
- Sequences, triggers, jobs and users are not migrated by most CDC tools.
- Large LOB columns slow full loads drastically; use limited LOB mode or separate handling.

## Verify
- [ ] Rehearsed cutover with timed lag drain and validation.
- [ ] Validation report signed off by data owner.
