---
id: computing-software.cloud-infrastructure-engineering.telegraf.telegraf-timestamp-parsing-formats
name: telegraf-timestamp-parsing-formats
category: computing-software
field: cloud-infrastructure-engineering
product: telegraf
tags: [timestamps, timestamp-format, unix, go-reference-time, timezone]
level: practitioner
status: docs-checked
description: "Reference for the timestamp formats Telegraf parsers accept: Unix variants, timestamp_tz, named layouts and custom Go reference time strings."
sources: ["https://docs.influxdata.com/telegraf/v1/configure_plugins/input_plugins/parse-data/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Timestamp formats in parsers

Tell the parser which part of the data holds the timestamp and its format. Without that, Telegraf uses the read time.

## Unix

`unix` (seconds), `unix_ms`, `unix_us`, `unix_ns`. Unix timestamps are UTC. If a device reports a Unix-style number in its local zone, use `timestamp_tz`, `timestamp_tz_ms`, `timestamp_tz_us`, `timestamp_tz_ns`, which compute the offset from a configured local timezone.

## Named formats

`ANSIC`, `UnixDate`, `RubyDate`, `RFC822`, `RFC822Z`, `RFC850`, `RFC1123`, `RFC1123Z`, `RFC3339`, `RFC3339Nano`, `Stamp`, `StampMilli`, `StampMicro`, `StampNano`.

## Custom (Go reference time)

Write the reference moment `Mon Jan 2 15:04:05 MST 2006` in your layout:

| Timestamp | Format |
| --- | --- |
| `2024-03-04T17:10:32` | `2006-01-02T15:04:05` |
| `04 Mar 24 10:10 -0700` | `02 Jan 06 15:04 -0700` |
| `2024-03-04 17:10:32.123+00` | `2006-01-02 15:04:05.999+00` |
| `2024-03-04T10:10:32.123456Z` | `2006-01-02T15:04:05.000000Z` |

For fractional seconds use either `9`s or `0`s.

## Checked

2026-11-03. Confirmed against docs-v2 Telegraf v1 pages (influxdata/docs-v2 source on GitHub): Parse data page, Parse timestamps section: Unix, timestamp_tz, named and custom Go formats. Removed: nothing.

Method: documentation only; no commands were run.
