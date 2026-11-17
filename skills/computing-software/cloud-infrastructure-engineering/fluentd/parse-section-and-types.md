---
id: computing-software.cloud-infrastructure-engineering.fluentd.parse-section-and-types
name: parse-section-and-types
category: computing-software
field: cloud-infrastructure-engineering
product: fluentd
tags: [cloud-infrastructure-engineering, fluentd, parse-section, parser, types, time-key, null-value-pattern]
level: practitioner
status: docs-checked
description: "Configure the Fluentd parse section: parser @type, types conversion (integer, bool, time, array), time_key, null handling and parse timeout."
sources:
  - https://docs.fluentd.org/configuration/parse-section
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fluentd parse section
`<parse>` goes under `<source>`, `<match>` or `<filter>`, only for plugins that support parser features (check the plugin's page). Built-in `@type` values: `regexp`, `apache`, `apache2`, `apache_error`, `nginx`, `syslog`, `csv`, `tsv`, `ltsv`, `json`, `multiline`, `none`. Individual parsers override some defaults below.

Parameters:
- `types` (hash, default nil): `field:type[:option]` list or JSON hash, e.g. `types user_id:integer,paid:bool,paid_usd_amount:float`.
- `time_key` (default nil): field holding the event time; if absent, current time is used. `json`, `ltsv` and `regexp` default it to `time`.
- `keep_time_key` (default false): keep the time field in the record.
- `null_value_pattern` (regexp) and `null_empty_string` (default false, turns empty strings into nil).
- `estimate_current_event` (default true): use the current time as the timestamp when `time_key` is specified.
- `timeout`: parse timeout, mainly to detect a bad regexp.

`types` options: `string`; `bool` ("true", "yes", "1" become true); `integer` (not `int`); `float`; `time` (third field is the format: `date:time:%d/%b/%Y:%H:%M:%S %z`, `date:time:unixtime`, `date:time:float`); `array` (third field is the delimiter, default comma, e.g. `item_ids:array:|`).

## Checked

2026-11-04: read the fetched text of https://docs.fluentd.org/configuration/parse-section and confirmed: built-in parsers, parameter defaults, types options. Removed or reworded: nothing.

Method: documentation only; no commands were run.
