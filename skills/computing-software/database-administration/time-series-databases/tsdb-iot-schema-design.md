---
id: computing-software.database-administration.time-series-databases.tsdb-iot-schema-design
name: tsdb-iot-schema-design
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-gen-schema, tsdb-iot-schema-design]
level: practitioner
status: draft
description: "Model device telemetry for storage and query efficiency."
sources:
  - https://prometheus.io/docs/prometheus/latest/storage/
  - https://docs.timescale.com/
  - https://docs.influxdata.com/influxdb/v2/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# IoT schema design

**Goal:** Model device telemetry for storage and query efficiency.

## Steps
- Wide row per reading time: `(time, device_id, temp, humidity, battery)` suits sensors reporting several values together; narrow `(time, device_id, metric, value)` suits sparse or heterogeneous metrics.
- Keep device metadata (location, model, firmware) in a separate relational table joined by `device_id`; do not repeat it per row.
- Use device-assigned UTC timestamps and also store ingest time to measure lag.
- Use smallint or int codes for status values; typed numeric columns compress better than text/JSON.
- Partition or order by `(device_id, time)` for per-device queries, time-only for fleet scans.
- Plan late and out-of-order data with idempotent keys `(device_id, time)`.

**Gotcha:** Storing JSON blobs per reading prevents column compression and server-side aggregation.

## Verify
- Per-device last-24h query runs in milliseconds.
- Row size and compressed size per day match the capacity estimate.
