---
id: computing-software.software-engineering.v-lang.v-time-now-format-parse
name: v-time-now-format-parse
category: computing-software
field: software-engineering
product: v-lang
tags: [v-time-now-format-parse, time-module, time, time.now, format, parse, rfc3339, unix, timestamp, utc, strftime, v-lang]
level: practitioner
status: docs-checked
description: "Get time with time.now and time.utc, format with Time.format variants, parse RFC3339 and custom strings and convert zones."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Current time, formatting and parsing

Goal: handle dates correctly.

- `import time`; `t := time.now()`; `time.utc()`; unix: `t.unix()`, `time.unix(1700000000)`, ms `t.unix_milli()`.
- Format: `t.format()` (`YYYY-MM-DD HH:mm`), `t.format_ss()` (`YYYY-MM-DD HH:mm:ss`), `t.format_rfc3339()`, `t.custom_format('YYYY-MM-DD HH:mm:ss')` (tokens include YYYY, MM, MMM, MMMM, DD, HH, mm, ss, ddd, dddd, A).
- Parse: `time.parse('2024-05-01 10:00:00')!` (format `YYYY-MM-DD HH:mm:ss`), `time.parse_rfc3339('2024-05-01T10:00:00Z')!`, `time.parse_iso8601(...)!`, custom `time.parse_format(s, 'YYYY-MM-DD')!` (the format must cover the whole input).
- Zones: `t.local_to_utc()`, `t.utc_to_local()`, `t.as_utc()`; IANA zones load with `time.load_location(name)!` (not supported on the JS and WASM backends) and `t.zone()!` reports the active zone; store UTC.
- Fields: `t.year`, `t.month`, `t.day`, `t.hour`, `t.minute`, `t.second`, `t.weekday()`.

Gotchas:
- `parse_rfc3339` and `parse_iso8601` treat `Z`, `+00:00` and `-00:00` as UTC and keep any other offset as a fixed-offset zone; prefer them with an explicit offset.
- Month/day are 1-based.

Verify: round trip `format_rfc3339` and `parse_rfc3339`.

## Checked

2026-11-03. Confirmed against the V repository source (vlib modules and doc/docs.md) read in this batch: time.now/utc/unix/unix_milli, Time.format/format_ss/format_rfc3339/custom_format token table, parse/parse_rfc3339/parse_iso8601/parse_format and their doc comments, local_to_utc/utc_to_local/as_utc, load_location and Time.zone (vlib/time: time.c.v, time.v, format.v, parse.c.v, zoneinfo.c.v, zoneinfo.js.v).
Removed or corrected: 'V has no full tz database (confirm)' (load_location exists), and the vague 'assumes local/UTC depending on function' gotcha.
Method: documentation only; no commands were run.
