---
id: computing-software.database-administration.time-series-databases.influxdb-line-protocol
name: influxdb-line-protocol
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-influx-data-model, influxdb-line-protocol, influxdb, flux]
level: practitioner
status: docs-checked
description: "Write points to InfluxDB with correct line protocol so tags, fields and timestamps land as intended."
sources:
  - https://docs.influxdata.com/influxdb/v2/reference/syntax/line-protocol/
  - https://docs.influxdata.com/influxdb/v2/reference/cli/influx/write/
  - https://docs.influxdata.com/influxdb/v2/write-data/best-practices/optimize-writes/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Line protocol format

**Goal:** Write points to InfluxDB with correct line protocol so tags, fields and timestamps land as intended.

## Steps
Format: `measurement,tag1=a,tag2=b field1=1.5,field2="text",field3=7i,field4=true 1730000000000000000`
- Space 1 separates tags from fields, space 2 separates fields from the timestamp.
- Integers need an `i` suffix (`7i`), unsigned `u`; plain numbers are floats. Strings are double-quoted.
- Escape with a backslash: commas and spaces in measurements; commas, equals signs and spaces in tag keys, tag values and field keys; double quotes and backslashes in string field values.
- Timestamp defaults to nanoseconds (`ns`); set the precision when your timestamps are coarser.
- Write with `influx write -b mybucket -o myorg -p s -f file.lp` or `POST /api/v2/write?org=myorg&bucket=mybucket&precision=s`.
- Sort tags by key for faster ingest (documented best practice).

**Gotcha:** A point is identified by measurement, tag set and timestamp. A second write with the same identity merges field sets, and conflicting field values take the new value.

## Verify
- A test write is accepted without error.
- A Flux `from(bucket: "mybucket") |> range(start: -5m)` query shows the expected tags, fields and types.

## Checked

2026-11-03. Confirmed in the line-protocol syntax page (spaces delimiting tag set, field set and timestamp; `i` and `u` suffixes; default `ns`; escape table; duplicate-point rule), the `influx write` CLI page (`-b`, `-o`, `-p/--precision`, `-f/--file`) and the optimize-writes page (sort tags by key, `/api/v2/write?org=...&bucket=...&precision=...`). Removed: the field-type-conflict claim, the HTTP 204 claim and the precision value list (not on the pages read).
Method: documentation only; no commands were run.

