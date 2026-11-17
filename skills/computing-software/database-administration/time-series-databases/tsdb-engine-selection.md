---
id: computing-software.database-administration.time-series-databases.tsdb-engine-selection
name: tsdb-engine-selection
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-gen-selection, tsdb-engine-selection]
level: practitioner
status: draft
description: "Pick a time-series engine for a workload with explicit criteria."
sources:
  - https://prometheus.io/docs/prometheus/latest/storage/
  - https://docs.timescale.com/
  - https://docs.influxdata.com/influxdb/v2/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Choosing an engine

**Goal:** Pick a time-series engine for a workload with explicit criteria.

## Steps
- Infra metrics with alerting: Prometheus plus Thanos, Mimir or VictoriaMetrics.
- Mixed relational plus time-series, SQL joins, strong consistency: TimescaleDB (PostgreSQL).
- Event-style high-cardinality analytics at scale: ClickHouse or InfluxDB 3.
- Simple IoT fleet with Flux/SQL and Telegraf: InfluxDB.
- Very fast ingest with SQL and time-based partitions: QuestDB.
- Score on: cardinality, ingest rate, query shapes (joins, percentiles), retention, ops skill, licence (confirm current licences: Timescale community vs Apache, InfluxDB 3 Core, Grafana AGPL for Mimir).
- Prototype with a day of real data on two candidates before committing.

**Gotcha:** Choosing on benchmarks published by the vendor ignores your cardinality and query mix; run your own test.

## Verify
- Decision doc records criteria, tested numbers and rejected options.
- Pilot meets ingest and p95 query targets.
