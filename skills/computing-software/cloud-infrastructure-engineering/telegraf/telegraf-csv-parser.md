---
id: computing-software.cloud-infrastructure-engineering.telegraf.telegraf-csv-parser
name: telegraf-csv-parser
category: computing-software
field: cloud-infrastructure-engineering
product: telegraf
tags: [csv, parser, header-row, column-names, metadata-rows]
level: practitioner
status: docs-checked
description: "Covers the Telegraf csv input data format: header rows, column names and types, skipped rows and columns, and metadata rows turned into tags."
sources: ["https://docs.influxdata.com/telegraf/v1/data_formats/input/csv/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# The csv input data format

Set `data_format = "csv"` on an input such as `inputs.file`.

## Header and naming

- `csv_header_row_count` (default 0): rows to treat as header. 0 means no header and `csv_column_names` is required; 1 uses the first row; more than 1 concatenates that many values per column. Values in `csv_column_names` override header names.
- `csv_column_names`: names in column order; unnamed columns are ignored.
- `csv_column_types`: `int`, `float`, `bool`, `string` per column. By default each column is tried as int, float, bool, then string.

## Skipping

- `csv_skip_rows`: rows to skip before metadata and header.
- `csv_skip_columns`: columns to skip in header and data rows.
- `csv_delimiter`: column separator, default a comma. `csv_comment` marks comment lines; `csv_trim_space` trims leading space.

## Metadata rows

`csv_metadata_rows` parses that many rows as key-value pairs using `csv_metadata_separators` (in precedence order, default `[":", "="]`, case-sensitive; at least one required) and adds them as tags. `csv_metadata_trim_set` trims characters from those rows. To turn the tags into fields use the converter processor.

```toml
[[inputs.file]]
  files = ["example"]
  data_format = "csv"
  csv_header_row_count = 1
```

Set `csv_timestamp_column` together with `csv_timestamp_format` to take the timestamp from a column (formats are in the timestamp skill); otherwise the current time in UTC is used.

## Checked

2026-11-03. Confirmed against docs-v2 Telegraf v1 pages (influxdata/docs-v2 source on GitHub): CSV input data format page: header, column, skip, metadata and timestamp options and defaults. Removed: the wording that the read time is used when no timestamp column is set (page says current time in UTC).

Method: documentation only; no commands were run.
