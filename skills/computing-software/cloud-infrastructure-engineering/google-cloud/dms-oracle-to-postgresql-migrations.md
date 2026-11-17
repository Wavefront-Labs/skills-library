---
id: computing-software.cloud-infrastructure-engineering.google-cloud.dms-oracle-to-postgresql-migrations
name: dms-oracle-to-postgresql-migrations
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, database-migration-service, dms-oracle, oracle-to-postgresql, conversion-workspace, alloydb]
level: advanced
status: docs-checked
description: "Migrate Oracle to Cloud SQL for PostgreSQL or AlloyDB with Database Migration Service: conversion workspaces, LogMiner CDC prerequisites, connectivity, and cutover checks."
sources: ["https://cloud.google.com/database-migration/docs/oracle-to-postgresql/overview", "https://cloud.google.com/database-migration/docs/oracle-to-postgresql/configure-source-database", "https://cloud.google.com/database-migration/docs/oracle-to-postgresql/conversion-workspaces-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DMS Oracle to PostgreSQL migrations

Heterogeneous migration = **schema conversion** (conversion workspace) + **data movement** (full load + CDC).

## 1. Prepare Oracle
- Archive log mode on; supplemental logging: `ALTER DATABASE ADD SUPPLEMENTAL LOG DATA;` and per-table
  `ALTER TABLE x ADD SUPPLEMENTAL LOG DATA (ALL) COLUMNS;` (or primary key logging).
- A migration user with SELECT on tables, `LOGMINING`, `SELECT ANY TRANSACTION` and SELECT on the `V_$LOGMNR_*` views (exact grants per Oracle edition are in the configure-source-database page).
- Retain archive logs long enough to cover full load plus replication lag.

## 2. Connectivity
Create a connection profile for Oracle and one for the destination. Choose the connectivity method from the DMS docs for your source. Test the profile before creating a job.

## 3. Convert the schema
1. Create a **conversion workspace** (Oracle → PostgreSQL), pull the source schema.
2. Review the conversion issues the workspace reports (PL/SQL code, data types, sequences).
3. Apply mapping rules and edit the converted SQL in the workspace.
4. **Apply** the converted schema to the destination.

## 4. Migrate and cut over
Create the job with the workspace; full dump then CDC. Watch replication delay; when ~0:
stop app writes, wait for delay 0, validate (row counts and checksums),
reset sequences to max(id)+1, switch connection strings, **promote**.

## Gotchas
- Code (packages, triggers) usually needs hand work beyond the workspace; test the app, not just the data.

## Verify
- [ ] Row-count and column-checksum validation passes for every table; application integration tests pass against the destination before promotion.

## Checked

2026-10-28. Confirmed against: Oracle configure-source-database page: ARCHIVELOG mode, ALTER DATABASE ADD SUPPLEMENTAL LOG DATA, per-table ADD SUPPLEMENTAL LOG DATA (ALL) COLUMNS, GRANT LOGMINING, GRANT SELECT ANY TRANSACTION, SELECT on V_$LOGMNR_CONTENTS and V_$LOGMNR_LOGS.

Removed or rewritten: the V_$ARCHIVED_LOG grant, retention in days, DMS private connection / reverse SSH specifics, type-mapping examples (NUMBER, DATE), Gemini-assisted conversion, the Data Validation Tool name, and the primary-key and LOB gotchas, none of which could be confirmed from the fetched pages.

Method: documentation only; no commands were run.
