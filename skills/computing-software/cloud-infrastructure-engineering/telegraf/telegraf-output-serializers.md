---
id: computing-software.cloud-infrastructure-engineering.telegraf.telegraf-output-serializers
name: telegraf-output-serializers
category: computing-software
field: cloud-infrastructure-engineering
product: telegraf
tags: [serializers, data-format, influx, json, prometheus]
level: practitioner
status: docs-checked
description: "Describes Telegraf output serializers selected by data_format on generic outputs, with influx, json and prometheus examples and their caveats."
sources: ["https://docs.influxdata.com/telegraf/v1/configure_plugins/output_plugins/serialize-data/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Output serializers

A serializer converts metrics into the format a destination expects. Generic outputs (file, http, kafka, mqtt) take `data_format`. Service-specific outputs such as `influxdb_v3` and `prometheus_client` use a fixed format and do not.

## influx

InfluxDB line protocol; the default for most generic outputs and recommended unless the destination needs another. NaN and Inf float fields are skipped, and tags with an empty key or value are skipped.

```toml
[[outputs.file]]
  files = ["stdout"]
  data_format = "influx"
```

## json

```toml
[[outputs.file]]
  files = ["stdout"]
  data_format = "json"
  json_timestamp_units = "1s"
```

Each metric becomes a document with `fields`, `name`, `tags`, `timestamp`. Outputs that send many metrics may use batch form with a top-level `metrics` array, depending on the plugin. `json_transformation` applies a JSONata transform to reshape the result.

## prometheus

```toml
[[outputs.file]]
  files = ["stdout"]
  use_batch_format = true
  data_format = "prometheus"
```

Emits text exposition with HELP and TYPE lines, with metric names joining measurement and field key (such as `cpu_usage_idle`) and tags as labels.

## Checked

Method: docs-checked 2026-11-09 against the Serialize outgoing data page (raw markdown in github.com/influxdata/docs-v2, read in full). All claims confirmed.
