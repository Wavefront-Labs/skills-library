---
id: computing-software.cloud-infrastructure-engineering.fluentd.format-section
name: format-section
category: computing-software
field: cloud-infrastructure-engineering
product: fluentd
tags: [cloud-infrastructure-engineering, fluentd, format-section, formatter, time-type, out-file, json]
level: practitioner
status: docs-checked
description: "Configure the Fluentd format section: formatter @type, built-in formatters, and time_type/time_format/timezone settings for formatted output."
sources:
  - https://docs.fluentd.org/configuration/format-section
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fluentd format section
`<format>` goes under `<match>` or `<filter>` for plugins that support formatter features. `@type` picks the formatter; built-in: `out_file`, `json`, `ltsv`, `csv`, `msgpack`, `hash`, `single_value`.

```
<match tag.*>
  @type file
  <format>
    @type json
  </format>
</match>
```
Time parameters:
- `time_type` default `float`; values `float` (epoch seconds plus nanoseconds), `unixtime`, `string` (uses `time_format`).
- `time_format` (default nil) only for `string`; see Ruby `Time#strftime`; use `%N` for sub-second precision.
- `localtime` (default true) / `utc` (default false), mutually exclusive.
- `timezone` (default nil): `[+-]HH:MM` recommended, `[+-]HHMM`, `[+-]HH`, `Asia/Tokyo` style names.

## Checked

2026-11-04. Confirmed against the Fluentd Config: Format Section page (docs.fluentd.org/configuration/format-section): placement, built-in formatter list, time parameter defaults and values. Removed: the comparison with parse-section defaults and the closing generic advice (not on the page).

Method: documentation only; no commands were run.
