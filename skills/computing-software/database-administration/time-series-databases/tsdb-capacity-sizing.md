---
id: computing-software.database-administration.time-series-databases.tsdb-capacity-sizing
name: tsdb-capacity-sizing
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-gen-sizing, tsdb-capacity-sizing]
level: practitioner
status: draft
description: "Estimate disk, memory, CPU and IOPS for a time-series deployment."
sources:
  - https://prometheus.io/docs/prometheus/latest/storage/
  - https://docs.timescale.com/
  - https://docs.influxdata.com/influxdb/v2/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Capacity and hardware sizing

**Goal:** Estimate disk, memory, CPU and IOPS for a time-series deployment.

## Steps
- Inputs: series count, sample interval, retention, replication factor, query concurrency.
- Samples/s = series / interval. Example: 500k series at 10 s = 50k samples/s = 4.3 billion/day.
- Disk = samples/day x retention x bytes per sample x replication. At 1.5 bytes: 6.5 GB/day, about 200 GB/month, before replication.
- Memory: active series x per-series overhead (Prometheus 3 to 8 KB, VictoriaMetrics 1 to 2 KB claimed, Influx and Timescale depend on indexes); confirm with a pilot.
- Disk type: NVMe for ingest-heavy; avoid network filesystems for WAL.
- Add 30 percent headroom for compaction and growth, and test with a representative load generator.
- Re-run the estimate after cardinality or interval changes.

**Gotcha:** Capacity planned from average ingest fails at spikes; size for peak and for compaction temporary space.

## Verify
- Pilot shows measured bytes per sample within 25 percent of the estimate.
- Disk-full alert fires at 70 percent.
