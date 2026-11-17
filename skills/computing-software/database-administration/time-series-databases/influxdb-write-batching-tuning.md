---
id: computing-software.database-administration.time-series-databases.influxdb-write-batching-tuning
name: influxdb-write-batching-tuning
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-influx-performance, influxdb-write-batching-tuning, influxdb, flux]
level: practitioner
status: docs-checked
description: "Achieve high write throughput with batched, compressed writes."
sources:
  - https://docs.influxdata.com/influxdb/v2/write-data/best-practices/optimize-writes/
  - https://docs.influxdata.com/influxdb/v2/reference/config-options/
  - https://docs.influxdata.com/telegraf/v1/configure_plugins/output_plugins/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Write batching and ingest tuning

**Goal:** Achieve high write throughput with batched, compressed writes.

## Steps
- Write in batches to cut network overhead; the documented optimal batch size is 5000 lines of line protocol.
- Gzip request bodies with `Content-Encoding: gzip` (in Telegraf set `content_encoding = "gzip"` on the `influxdb_v2` output).
- Sort tags by key before writing.
- Server options that matter: `--storage-write-timeout`, `--storage-cache-max-memory-size`, `--storage-cache-snapshot-memory-size`.
- Use the coarsest timestamp precision your data allows; the default is nanoseconds.
- Telegraf retries failed batches from each output's buffer.

**Gotcha:** A point is identified by measurement, tag set and timestamp, so a retried batch merges into existing points rather than duplicating them; never add a random timestamp to force uniqueness.

## Verify
- Write throughput in points per second reaches the target in a load test.

## Checked

2026-11-03. Confirmed in the optimize-writes page (5000-line batches, sort tags, coarsest precision, gzip and the Telegraf `content_encoding` option), the `influxd` config options page (the three `storage-*` options) and the Telegraf output-plugins page (retry from the buffer). Removed: the 10,000-line upper bound, parallel-writer guidance, 429/5xx backoff and the metric names.
Method: documentation only; no commands were run.

