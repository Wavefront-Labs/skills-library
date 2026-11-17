---
id: computing-software.database-administration.time-series-databases.telegraf-processors-aggregators
name: telegraf-processors-aggregators
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-influx-telegraf, telegraf-processors-aggregators, influxdb, telegraf]
level: practitioner
status: draft
description: "Clean, rename and pre-aggregate metrics inside Telegraf before storage."
sources:
  - https://docs.influxdata.com/influxdb/v2/
  - https://docs.influxdata.com/telegraf/v1/
  - https://docs.influxdata.com/influxdb3/core/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Processors and aggregators

**Goal:** Clean, rename and pre-aggregate metrics inside Telegraf before storage.

## Steps
- Processors run per metric: `processors.rename`, `processors.regex`, `processors.converter`, `processors.override`, `processors.dedup`.
```
[[processors.converter]]
  [processors.converter.fields]
    integer = ["status_code"]
```
- Aggregators emit summary metrics over a `period`: `[[aggregators.basicstats]]` with `period = "30s"`, `drop_original = false`, `stats = ["mean","max"]`.
- Use `tagpass` / `tagdrop` / `namepass` filters to restrict plugins to the metrics they should touch.
- Drop noisy high-cardinality tags with `tagexclude = ["container_id"]` on the input or output.
- Order is set by the `order` option on processors.

**Gotcha:** Aggregators see only metrics whose timestamps fall inside the current period; late or batched metrics are dropped from aggregation.

## Verify
- `--test` or `outputs.file` shows renamed tags and aggregated fields.
- Series count in the destination matches expectations.
