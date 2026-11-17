---
id: computing-software.cloud-infrastructure-engineering.fluentd.parse-format-time-parameters
name: parse-format-time-parameters
category: computing-software
field: cloud-infrastructure-engineering
product: fluentd
tags: [cloud-infrastructure-engineering, fluentd, time-format, timezone, time-type, localtime, utc]
level: practitioner
status: docs-checked
description: "Time parameters shared by parse and format sections: time_type, time_format, localtime/utc, timezone and time_format_fallbacks for mixed formats."
sources:
  - https://docs.fluentd.org/configuration/parse-section
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fluentd time parameters
Documented on the parse section page; extract and inject reuse these parameters with `time_type` defaulting to `float`.

- `time_type` (default `string`): `float` (epoch seconds plus nanoseconds, e.g. 1510544836.154709804), `unixtime` (epoch seconds), `string` (uses `time_format`), `mixed` (enables `time_format_fallbacks`; since v1.12.2).
- `time_format` (default nil): only when `time_type` is `string`. Formatting follows Ruby `Time#strftime`, parsing follows `Time.strptime`; `%iso8601` is parse-only. Use `%N` for sub-second precision, because `%3N`, `%6N`, `%9N` and `%L` are not supported by the strptime library.
- `localtime` (default true) and `utc` (default false) are mutually exclusive.
- `timezone`: `[+-]HH:MM` (recommended), `[+-]HHMM`, `[+-]HH`, `Region/Zone` (`Asia/Tokyo`) or `Region/Zone/Zone`.
- `time_format_fallbacks`: used when `time_type` is `mixed`; formats are tried in order.

```
time_type mixed
time_format unixtime
time_format_fallbacks %iso8601
```
Fallbacks are a last resort and carry a performance penalty per extra format tried.

## Checked

2026-11-04: read the fetched text of https://docs.fluentd.org/configuration/parse-section, https://docs.fluentd.org/configuration/extract-section, https://docs.fluentd.org/configuration/inject-section and confirmed: time_type values, time_format rules, localtime, utc, timezone formats, time_format_fallbacks. Removed or reworded: the claim that the parse page covers formatter sections (the page covers parse; extract and inject reuse the parameters with default time_type float).

Method: documentation only; no commands were run.
