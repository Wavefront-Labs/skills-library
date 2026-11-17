---
id: computing-software.database-administration.time-series-databases.tsdb-high-availability
name: tsdb-high-availability
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-gen-backup-ha, tsdb-high-availability]
level: practitioner
status: draft
description: "Choose an HA design that matches the engine's capabilities."
sources:
  - https://prometheus.io/docs/prometheus/latest/storage/
  - https://docs.timescale.com/
  - https://docs.influxdata.com/influxdb/v2/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# High availability patterns

**Goal:** Choose an HA design that matches the engine's capabilities.

## Steps
- Prometheus: two independent servers with replica label plus dedup in Thanos or Mimir.
- Influx OSS: dual writes via Telegraf; clustered editions replicate internally.
- Timescale: PostgreSQL streaming replication with Patroni; synchronous replica for zero loss at write-latency cost.
- VictoriaMetrics cluster: `-replicationFactor=2`; ClickHouse: ReplicatedMergeTree with Keeper.
- Buffer at the edge: agents (Telegraf, vmagent, Prometheus agent mode) hold data during outages.
- Define failover: who promotes, how clients discover (DNS, VIP, proxy), and test it.
- Distinguish ingest HA from query HA; they fail separately.

**Gotcha:** Two uncoordinated writers can leave diverging copies; after failover always check for gaps and backfill.

## Verify
- Planned failover test shows no data gap beyond the RPO.
- Alerts exist for replica lag and unhealthy members.
