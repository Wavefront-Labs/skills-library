---
id: computing-software.software-engineering.ocaml.dates-time-zones-and-calendars
name: dates-time-zones-and-calendars
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, dates-calendars, timedesc, time-zone, calendar-arithmetic, dst]
level: practitioner
status: docs-checked
description: "Convert Ptime timestamps to dates with tz offsets, parse RFC 3339, and know why POSIX arithmetic is not calendar arithmetic."
sources: ["https://erratique.ch/software/ptime/doc/Ptime/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dates and time zone offsets with Ptime

```ocaml
let get = function None -> assert false | Some v -> v
let t = get (Ptime.of_date_time ((2024, 3, 10), ((12, 0, 0), 0)))   (* 2024-03-10 12:00 UTC *)
let s = Ptime.to_rfc3339 ~tz_offset_s:3600 t                        (* RFC 3339 with +01:00 *)
let (y, m, d) = Ptime.to_date t
```

## Notes
- `Ptime.t` is a picosecond-precision POSIX timestamp on the UTC timeline, in the range `Ptime.min` (0000-01-01) to `Ptime.max` (9999-12-31). Constructors return `option`; invalid dates give `None`.
- A date is `(y, m, d)` in the proleptic Gregorian calendar; a time is `((hh, mm, ss), tz_offset_s)`. `tz_offset_s = local - UTC` in seconds; `to_date_time ?tz_offset_s` defaults to UTC and falls back to 0 only near `min` and `max`.
- `Ptime.weekday` and `weekday_num` (0 = Sunday) take an optional `tz_offset_s`.
- `of_rfc3339` returns `(t, tz option, byte_count)` or an error; by default (`strict = false`) it also accepts lowercase `t`/`z`, space separators and `hhmm` offsets. Use `rfc3339_error_to_msg` for messages. `to_rfc3339 ?space ?frac_s ?tz_offset_s` formats; `pp_human` is for presentation only.
- Ptime is not a calendar library and never will be. `add_span`, `sub_span` and `diff` use POSIX seconds, which may be 0, 1 or 2 SI seconds around leap seconds; do not use them for calendar arithmetic or wall-clock durations. Adding months or handling named zones and DST needs another library.
- POSIX timestamps from the OS are not monotonic; use a monotonic source such as Mtime to measure spans.
- A leap-second `ss = 60` is mapped to one second later; `to_date_time` never returns 60.

## Self-check
- [ ] A round trip through `to_rfc3339` and `of_rfc3339` gives the same timestamp.

## Checked
Date: 2026-11-08. Confirmed against the Ptime API page (read in full). Removed: all timedesc and tzdb claims and example, `Ptime_clock.now`, the Unix.tm field remark, store-in-UTC and DST test advice, and the ocaml.org/docs source.
Method: documentation only; no commands were run.
