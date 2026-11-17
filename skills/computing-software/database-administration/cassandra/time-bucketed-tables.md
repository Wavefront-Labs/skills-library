---
id: computing-software.database-administration.cassandra.time-bucketed-tables
name: time-bucketed-tables
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, time-bucket, bucket-size, ttl-timeseries, time-series-modeling, iot-data-model, rollup-tables, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "Bucket design"
sources: ["https://cassandra.apache.org/doc/latest/cassandra/managing/operating/compaction/twcs.html", "https://cassandra.apache.org/doc/latest/cassandra/developing/cql/ddl.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Time-bucketed time-series tables

Goal: model telemetry.
- Use a composite partition key such as `PRIMARY KEY ((device_id, bucket), ts)` with `WITH CLUSTERING ORDER BY (ts DESC)`.
- The docs recommend TWCS for time-series and expiring TTL workloads: it groups SSTables by time window and drops whole SSTables when they expire; the window unit is `compaction_window_unit`. Avoid `USING TIMESTAMP` writes with TWCS.
- Partition-key equality is required, so a range across buckets needs one query per bucket.
Verify: partition size stays bounded under peak ingestion.

## Checked

2026-11-03. Confirmed against the Apache Cassandra documentation: composite partition key syntax, `CLUSTERING ORDER BY`, TWCS recommendation and window options, USING TIMESTAMP caveat. Removed: the partition-size target and the advice to align window and bucket size.

Method: documentation only; no commands were run.
