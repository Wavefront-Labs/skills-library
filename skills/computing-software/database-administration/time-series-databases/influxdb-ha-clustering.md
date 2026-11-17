---
id: computing-software.database-administration.time-series-databases.influxdb-ha-clustering
name: influxdb-ha-clustering
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-influx-backup, influxdb-ha-clustering, influxdb, flux]
level: practitioner
status: docs-checked
description: "Choose a realistic HA approach for InfluxDB."
sources:
  - https://docs.influxdata.com/telegraf/v1/configure_plugins/output_plugins/
  - https://docs.influxdata.com/telegraf/v1/output-plugins/influxdb_v2/
  - https://docs.influxdata.com/influxdb3/enterprise/admin/clustering/
  - https://docs.influxdata.com/influxdb3/core/reference/internals/durability/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# InfluxDB high availability

**Goal:** Choose a realistic HA approach for InfluxDB.

## Steps
- For independent InfluxDB 2.x instances, HA means dual writes to two instances.
- Dual write with Telegraf: two `[[outputs.influxdb_v2]]` blocks (Telegraf allows multiple output plugins and multiple instances of one plugin); each output has its own buffer of up to `metric_buffer_limit` metrics, and the oldest are dropped if it fills while the destination is down.
- Put a load balancer or Grafana multi-datasource in front of reads; accept that nodes can differ after an outage.
- Reconcile gaps by backfilling from the healthy node's line-protocol export (`influxd inspect export-lp`).
- InfluxDB 3 Enterprise lets you run specialised nodes: pass `--mode` (for example `influxdb3 serve --mode=ingest`) for ingest, query and compactor roles.
- In InfluxDB 3 the write-ahead log is flushed to the object store every second by default, so durability comes from the object store rather than local replicated disks.

**Gotcha:** Two independent OSS nodes accept writes separately, so any outage on one leaves a permanent gap unless you backfill.

## Verify
- Stop one node; writers continue to the other.
- After restart, a gap check query shows no missing intervals.

## Checked

2026-11-03. Confirmed in the Telegraf output-plugins page (multiple outputs, per-output buffer, `metric_buffer_limit`), the `influxdb_v2` output plugin page (`[[outputs.influxdb_v2]]`), the InfluxDB 3 Enterprise clustering page (`--mode`, ingest/query/compactor nodes), the InfluxDB 3 durability page (WAL flush each second to object store) and the `export-lp` CLI page. Removed: the claims that OSS 2.x has no clustering and which other editions offer replication (not stated on the pages read).
Method: documentation only; no commands were run.

