---
id: computing-software.database-administration.time-series-databases.influxdb-tsi-index
name: influxdb-tsi-index
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-influx-cardinality, influxdb-tsi-index, influxdb, flux]
level: practitioner
status: docs-checked
description: "Understand the InfluxDB 2.x time series index and rebuild it with influxd inspect build-tsi."
sources:
  - https://docs.influxdata.com/influxdb/v2/reference/internals/storage-engine/
  - https://docs.influxdata.com/influxdb/v2/reference/cli/influxd/inspect/build-tsi/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TSI index and memory

**Goal:** Understand the InfluxDB 2.x time series index and rebuild it with influxd inspect build-tsi.

## Steps
- The Time Series Index (TSI) stores series keys grouped by measurement, tag and field, so queries stay fast as cardinality grows and meta queries can find which measurements, tags and fields exist.
- The TSM data directory defaults to `~/.influxdbv2/engine/data`.
- `influxd inspect build-tsi` rebuilds the TSI index and, if necessary, the series file. Narrow it with `--bucket-id`, `--shard-id` (needs `--bucket-id`) and `--data-path`.

**Gotcha:** Rebuild the index on a copy or in a maintenance window first; the page does not say it is safe against a running server.

## Verify
- Server starts and queries return after rebuild.

## Checked

2026-11-03. Confirmed in the storage-engine page (TSI role) and the `influxd inspect build-tsi` CLI page (purpose, `--bucket-id`, `--shard-id`, `--data-path` and its default). Removed: the memory-mapping and page-cache claims, the 1.x comparison, the heap metric, the SSD advice and the duration estimate (not on the pages read).
Method: documentation only; no commands were run.

