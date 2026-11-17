---
id: computing-software.cloud-infrastructure-engineering.telegraf.telegraf-json-v2-parser
name: telegraf-json-v2-parser
category: computing-software
field: cloud-infrastructure-engineering
product: telegraf
tags: [json-v2, gjson, json, object-parsing, timestamp-path]
level: advanced
status: docs-checked
description: "Describes the json_v2 parser structure: measurement name, timestamp path, tag, field and object sub-tables selected by GJSON paths."
sources: ["https://docs.influxdata.com/telegraf/v1/data_formats/input/json_v2/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# The json_v2 parser

Instead of flattening a document, you describe the metrics you want. Values are selected with GJSON path syntax; develop paths in the GJSON playground. The docs recommend `xpath_json` over `json_v2` for new configurations, especially with arrays.

## Structure

A `json_v2` sub-table of the input holds `field`, `tag` and `object` sub-tables:

```toml
[[inputs.file]]
  files = ["example.json"]
  data_format = "json_v2"
  [[inputs.file.json_v2]]
    measurement_name = "weather"
    timestamp_path = "time"
    timestamp_format = "unix"
    [[inputs.file.json_v2.tag]]
      path = "station"
    [[inputs.file.json_v2.field]]
      path = "temp"
      type = "float"
```

## Options

- Top level: `measurement_name`, `measurement_name_path`, `timestamp_path`, `timestamp_format`, `timestamp_timezone`.
- `tag` and `field`: `path`, `rename`, `optional`; fields add `type` (`int`, `uint`, `float`, `string`, `bool`).
- `object` (for an object or array): `path`, `optional`, `timestamp_key`, `tags` (keys stored as tags), `included_keys`, `excluded_keys`, `disable_prepend_keys`, plus `renames` and `fields` (force a type per key) tables.

`optional = true` suppresses the error when a path does not match.

## Checked

Method: docs-checked 2026-11-09 against the influxdata docs-v2 source for the JSON v2 input data format (overview, root options and field/tag/object options read; worked examples not read).
