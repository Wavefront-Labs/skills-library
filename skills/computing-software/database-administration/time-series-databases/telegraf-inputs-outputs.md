---
id: computing-software.database-administration.time-series-databases.telegraf-inputs-outputs
name: telegraf-inputs-outputs
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-influx-telegraf, telegraf-inputs-outputs, influxdb, telegraf]
level: practitioner
status: draft
description: "Configure Telegraf to collect metrics and write them to InfluxDB."
sources:
  - https://docs.influxdata.com/influxdb/v2/
  - https://docs.influxdata.com/telegraf/v1/
  - https://docs.influxdata.com/influxdb3/core/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Telegraf inputs and outputs

**Goal:** Configure Telegraf to collect metrics and write them to InfluxDB.

## Steps
- Generate a starting config: `telegraf --input-filter cpu:mem:disk --output-filter influxdb_v2 config > telegraf.conf`.
```
[agent]
  interval = "10s"
  flush_interval = "10s"
[[inputs.cpu]]
  percpu = false
[[outputs.influxdb_v2]]
  urls = ["http://influx:8086"]
  token = "$INFLUX_TOKEN"
  organization = "myorg"
  bucket = "telegraf"
```
- Use environment variables for secrets; do not commit tokens.
- Test once: `telegraf --config telegraf.conf --test`.
- Load many configs with `--config-directory /etc/telegraf/telegraf.d`.

**Gotcha:** A plugin-level `interval` changes how often that plugin collects but it still flushes with the agent, so slow plugins need their own setting and timeout.

## Verify
- `--test` prints line-protocol metrics.
- Points appear in the target bucket within one flush interval.
