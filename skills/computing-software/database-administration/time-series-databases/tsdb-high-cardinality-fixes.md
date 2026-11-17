---
id: computing-software.database-administration.time-series-databases.tsdb-high-cardinality-fixes
name: tsdb-high-cardinality-fixes
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-gen-cardinality, tsdb-high-cardinality-fixes]
level: practitioner
status: draft
description: "Reduce an existing cardinality explosion with the lowest-risk changes first."
sources:
  - https://prometheus.io/docs/prometheus/latest/storage/
  - https://docs.timescale.com/
  - https://docs.influxdata.com/influxdb/v2/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fixing high cardinality

**Goal:** Reduce an existing cardinality explosion with the lowest-risk changes first.

## Steps
- Find the offenders (top metrics by series; label with the most values).
- Remove or hash unbounded labels in the instrumentation; normalise URL paths to route templates (`/users/:id`).
- Move per-entity detail into logs, traces or a separate analytical store (ClickHouse) and keep metrics aggregated.
- Drop at collection time: relabel/`labeldrop` (Prometheus), `tagexclude` (Telegraf), stream aggregation (vmagent).
- Pre-aggregate with recording rules and drop raw series with `keep` allow-lists.
- Rotate short-lived entities (pods) into a stable `deployment` label.
- After fixing, wait for retention or delete old series to reclaim memory and index space.

**Gotcha:** Fixing the label without deleting old series leaves the index bloated until retention passes.

## Verify
- Active series fall and stay low.
- Memory and compaction time drop.
