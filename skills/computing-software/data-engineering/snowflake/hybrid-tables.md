---
id: computing-software.data-engineering.snowflake.hybrid-tables
name: hybrid-tables
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, hybrid-tables, unistore, primary-keys, low-latency]
level: advanced
status: docs-checked
description: "Use Snowflake hybrid tables for low-latency point lookups and enforced keys: creation, indexes, bulk loading, quotas, cost, and when a normal table or Postgres is better."
sources:
  - https://docs.snowflake.com/en/user-guide/tables-hybrid
  - https://docs.snowflake.com/en/user-guide/tables-hybrid-limitations
  - https://docs.snowflake.com/en/user-guide/tables-hybrid-best-practices
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Hybrid tables

**Goal:** serve single-row reads/writes in milliseconds (app state, job control tables, lookups) inside Snowflake, with enforced constraints.

## Create
```sql
CREATE HYBRID TABLE app.job_runs (
  run_id     NUMBER PRIMARY KEY,
  job_name   VARCHAR NOT NULL,
  status     VARCHAR,
  started_at TIMESTAMP_NTZ,
  UNIQUE (job_name, started_at),
  INDEX idx_status (status)
);
```
- PRIMARY KEY is required and enforced; FOREIGN KEY constraints are optional and enforced (referential integrity). Row-level locking.
- Secondary indexes serve lookup columns (see the index design page).

## Load
See the hybrid tables best-practices page on bulk loading data; batch inserts rather than loading row by row.

## Good fit
- High-concurrency point lookups by key, small transactional updates, control/metadata tables for pipelines, Streamlit/app backends needing row locks.
## Poor fit
- Large scans/aggregations (use standard tables), heavy analytics joins, very high write throughput beyond the documented quotas.

## Costs and limits
- Throughput is subject to quotas and throttling; Time Travel queries and cloning have limitations. Read the limitations page first.

## Verify
Query profile shows index usage for point lookups; latency measured from the app meets target under expected concurrency.

## Checked

2026-10-28: reviewed against the official documentation fetched this batch.

Confirmed on the hybrid tables, CREATE HYBRID TABLE, limitations and best-practices pages: PRIMARY KEY required, UNIQUE/FOREIGN KEY/CHECK optional, INDEX clause for secondary indexes, row-level locking, quotas and throttling, Time Travel and cloning limitations.

Removed: the earlier unsupported claims (enforced UNIQUE, INCLUDE indexes, bulk-load fast path, pricing, latency figures) and the Postgres suggestion.

Method: documentation only; no commands were run.
