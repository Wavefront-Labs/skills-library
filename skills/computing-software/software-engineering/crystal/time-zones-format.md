---
id: computing-software.software-engineering.crystal.time-zones-format
name: time-zones-format
category: computing-software
field: software-engineering
product: crystal
tags: [time-zones-format, time, time-zone, time-location, strftime, time-format, parse, rfc3339, iso8601, to-s, in-zone, tzdata, crystal]
level: practitioner
status: docs-checked
description: "Use Time::Location for IANA zones, format and parse with Time::Format, RFC 3339, ISO 8601 and custom patterns."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/crystal/tree/master/src
  - https://github.com/crystal-lang/crystal-book/tree/master/docs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Time zones, formatting and parsing

Goal: format and convert times.

- `loc = Time::Location.load("Europe/Paris")`; `t.in(loc)`; `Time.local(loc)`; `Time::Location::UTC`; `t.zone`, `t.offset`; `Location.load?` returns nil instead of raising.
- Format: `t.to_s("%Y-%m-%d %H:%M:%S %z")`, `t.to_rfc3339`, `t.to_rfc2822`, `Time::Format::ISO_8601_DATE`, `ISO_8601_DATE_TIME`, `ISO_8601_TIME`, `RFC_3339`, `RFC_2822`, `HTTP_DATE` (use as `Time::Format::RFC_3339.format(t)`).
- Parse: `Time.parse(str, "%Y-%m-%d", location)`, `Time.parse_rfc3339(str)`, `Time.parse_iso8601(str)`, `Time.parse_utc(str, fmt)`.
- JSON/YAML fields: `converter: Time::EpochConverter` or a `Time::Format` instance (the field docs name both).
- The zoneinfo database is read from system paths; `TZDIR` (legacy `ZONEINFO`) points at a directory or uncompressed ZIP of zone files; ship a copy where the system has none.

Gotchas:
- Images without a time zone database make `Time::Location.load` raise `InvalidLocationNameError`; `UTC` and `Etc/UTC` always work.
- `Time.parse(str, pattern, location)` requires the location and uses it when the text has no zone; `Time.parse_utc` and `parse_local` are the shortcuts.
- In a DST gap a local wall clock is mapped to a time before the gap; the result differs from the requested clock.

Verify: convert a UTC time to Asia/Tokyo and print the offset.

## Checked

Date 2026-11-03. Confirmed Time::Location.load and load? (IANA names, UTC and Etc/UTC special cases, TZDIR with legacy ZONEINFO, InvalidLocationNameError), Time#in, Time.local, Time#zone and offset, to_rfc3339, to_rfc2822, Time.parse (location is required), parse_utc, parse_local, parse_rfc3339, parse_iso8601, the Time::Format constants, EpochConverter in the JSON/YAML field docs, and the gap and fold behaviour of Time.local. Removed the invented require time/tz embedding claim (time/tz is the POSIX TZ string parser), the constructor Time::Format.new JSON converter claim and the 'default UTC' parse claim.

Method: documentation only; no commands were run.
