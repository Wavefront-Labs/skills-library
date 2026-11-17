---
id: computing-software.cloud-infrastructure-engineering.telegraf.telegraf-metrics-data-model
name: telegraf-metrics-data-model
category: computing-software
field: cloud-infrastructure-engineering
product: telegraf
tags: [metrics, tags, fields, line-protocol, data-model]
level: intro
status: docs-checked
description: "Explains the four parts of a Telegraf metric and how to choose between tags and fields. Use when designing what an input emits or parsing data into metrics."
sources: ["https://docs.influxdata.com/telegraf/v1/concepts/metrics/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Telegraf metric data model

A Telegraf metric is the internal representation used while data moves through the agent. It is modelled on the InfluxDB data model and has four parts:

- **Measurement name**: a description and namespace such as `cpu` or `mem`.
- **Tags**: string key-value pairs that identify the source, such as host name or region.
- **Fields**: typed key-value pairs holding the data, such as a numeric usage value.
- **Timestamp**: the time associated with the fields.

In InfluxDB line protocol one metric looks like:

```text
cpu,host=web01,cpu=cpu0 usage_idle=92.5,usage_user=4.2 1717000000000000000
```

## Tags or fields

Use tags for string values that identify and filter metrics. Use fields for the measured values themselves. Many destinations, InfluxDB included, index tags, so filtering by tag is cheaper than filtering by field.

## Serializing

Metrics sit in memory inside the pipeline. To write or view them, Telegraf converts each one with an output data format, also called a serializer. The default serializer produces InfluxDB line protocol, a one-to-one mapping of the metric. Telegraf is not tied to InfluxDB: serializers also produce Prometheus, Graphite, JSON and CSV.

Pending metrics are held in memory only by default and are lost if Telegraf stops; the `disk` buffer strategy persists them.

## Checked

Method: docs-checked 2026-11-09 against the Telegraf metrics page (raw markdown in github.com/influxdata/docs-v2, read in full). Dropped the unconfirmed claim that parsed data defaults to fields.
