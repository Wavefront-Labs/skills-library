---
id: computing-software.software-engineering.erlang.calendar-module
name: calendar-module
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-time, calendar-module]
level: practitioner
status: docs-checked
description: "Erlang calendar module: universal_time, datetime conversions, system_time_to_rfc3339 and day-of-week."
sources:
  - https://www.erlang.org/doc/apps/erts/
  - https://www.erlang.org/doc/apps/stdlib/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# calendar and RFC 3339 timestamps
**Goal:** produce and parse dates in a standard format.

```erlang
calendar:universal_time(),                                    % {{Y,M,D},{H,Mi,S}}
calendar:system_time_to_rfc3339(erlang:system_time(second), [{unit, second}, {offset, "Z"}]),
calendar:rfc3339_to_system_time("2026-11-02T10:00:00Z"),
calendar:day_of_the_week(2026, 11, 2),                        % 1 = Monday
calendar:datetime_to_gregorian_seconds({{2026,11,2},{0,0,0}}),
calendar:valid_date(2026, 2, 30).
```
- Prefer UTC internally and convert at the edges. `calendar:local_time/0` follows the host time zone.
- Gregorian seconds start at year 0 (`datetime_to_gregorian_seconds/1`).

## Gotchas
- Do not parse dates with ad hoc string splitting; `rfc3339_to_system_time/1,2` validates.

## Self-check
Round-trip a timestamp through RFC 3339 and compare.

## Checked
2026-11-02. Confirmed: apps/stdlib/calendar.html: universal_time, local_time, system_time_to_rfc3339, rfc3339_to_system_time, day_of_the_week (1 = Monday), valid_date, datetime_to_gregorian_seconds.
Removed: Time zone database remark and the epoch offset figure (not stated in the page).
Method: documentation only; no commands were run.
