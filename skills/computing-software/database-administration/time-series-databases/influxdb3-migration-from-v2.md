---
id: computing-software.database-administration.time-series-databases.influxdb3-migration-from-v2
name: influxdb3-migration-from-v2
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-influx-v3, influxdb3-migration-from-v2, influxdb, flux]
level: practitioner
status: docs-checked
description: "Plan a v2 to v3 move without breaking dashboards and writes."
sources:
  - https://docs.influxdata.com/influxdb3/core/write-data/http-api/compatibility-apis/
  - https://docs.influxdata.com/influxdb3/core/get-started/query/
  - https://docs.influxdata.com/influxdb3/core/plugins/
  - https://docs.influxdata.com/influxdb/v2/reference/cli/influxd/inspect/export-lp/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrating from InfluxDB 2 to 3

**Goal:** Plan a v2 to v3 move without breaking dashboards and writes.

## Steps
- Writes: InfluxDB 3 Core exposes a v2-compatible `/api/v2/write` endpoint (the `bucket` query parameter is the database name) that works with client libraries and Telegraf (`outputs.influxdb_v2`).
- Queries: Flux is not supported in InfluxDB 3; rewrite as SQL or InfluxQL.
- Tasks: the Processing Engine runs Python plugins on write, on a schedule or on demand; Flux tasks must be rebuilt there.
- Retention is set per database (`influxdb3 create database --retention-period 30d`).
- Export data from v2 with `influxd inspect export-lp` (exports a bucket as line protocol), or read it in time slices with `influx query --raw` (annotated CSV), then write line protocol to v3.
- Run both in parallel with dual writes until dashboards are verified.

**Gotcha:** Dashboards built on Flux and Flux-based alerting do not port automatically; inventory them first.

## Verify
- Row counts for sample series match between v2 and v3 over a closed range.
- Rewritten queries return the same aggregates within rounding.

## Checked

2026-11-03. Confirmed in the InfluxDB 3 Core compatibility-APIs page (`/api/v2/write`, `bucket` parameter as database, Telegraf plugin), the get-started query page (Flux not supported), the Processing Engine page (scheduled triggers), the data-retention page (`--retention-period`), and the v2 `export-lp` and `influx query` CLI pages. Removed: the edition caveats and the claim that buckets "become" databases beyond the parameter mapping.
Method: documentation only; no commands were run.

