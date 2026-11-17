---
id: computing-software.cloud-infrastructure-engineering.telegraf.telegraf-choosing-a-parser
name: telegraf-choosing-a-parser
category: computing-software
field: cloud-infrastructure-engineering
product: telegraf
tags: [parsers, data-format, json, xpath-json, json-v2]
level: practitioner
status: docs-checked
description: "Explains how Telegraf parsers turn raw input into metrics and how to choose among the json, json_v2 and xpath_json parsers."
sources: ["https://docs.influxdata.com/telegraf/v1/configure_plugins/input_plugins/parse-data/", "https://docs.influxdata.com/telegraf/v1/data_formats/input/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Choosing an input parser

Telegraf does not store raw data internally. A parser converts what an input reads into a measurement, tags, fields and a timestamp. Inputs that read raw data expose `data_format`:

```toml
[[inputs.file]]
  files = ["example.json"]
  data_format = "json_v2"
```

Each parser has its own options for mapping your data.

## JSON

Three parsers read JSON:

| Parser | Best for |
| --- | --- |
| `json` | Flat objects; flattens everything, optional GJSON `json_query`; numbers only by default; strings and booleans via `json_string_fields`. |
| `json_v2` | Existing configs that select nested values with GJSON paths and a per-value `type`. |
| `xpath_json` | Nested documents and arrays; selects with XPath 1.0. Recommended over `json_v2` for new configurations, especially with arrays. |

Use `json` when data is flat and you need no type control.

## Tags versus fields

Parsed values are fields unless configured as tags. Tags are always strings. If you give no timestamp source, Telegraf stamps the time the data was read.

Output-side counterpart: serializers.

## Checked

Method: docs-checked 2026-11-09 against the influxdata docs-v2 sources for "Parse incoming data" (configure_plugins/input_plugins/parse-data) and "Input data formats" (data_formats/input), both read in full.
