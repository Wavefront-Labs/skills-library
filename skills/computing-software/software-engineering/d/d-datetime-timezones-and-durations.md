---
id: computing-software.software-engineering.d.d-datetime-timezones-and-durations
name: d-datetime-timezones-and-durations
category: computing-software
field: software-engineering
product: d
tags: [d-datetime-timezones-and-durations, std-datetime, timezone, posixtimezone, utc, localtime, duration, dur, total, split, stopwatch, core-time, monotonic, d]
level: practitioner
status: docs-checked
description: "Convert across zones (TimeZone, PosixTimeZone, UTC, LocalTime), build Durations with dur!, convert units with total!/split!, and time code with StopWatch."
sources:
  - https://dlang.org/phobos/std_datetime_timezone.html
  - https://dlang.org/phobos/core_time.html
  - https://dlang.org/phobos/std_datetime_stopwatch.html
  - https://dlang.org/phobos/std_datetime_systime.html
  - https://dlang.org/phobos/std_datetime_interval.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Time zones, core.time Duration and StopWatch

Goal: zones and elapsed time.

- Zones: `PosixTimeZone.getTimeZone("America/Los_Angeles")` reads the TZ database files from `tzDatabaseDir` (default `getDefaultTZDatabaseDir()`, empty on Windows, so supply the files there). `WindowsTimeZone.getTimeZone("Pacific Standard Time")` reads the Windows registry (Windows names). Also `UTC()` and `LocalTime()`.
- Convert: `st.toOtherTZ(tz)`, `st.timezone`, `st.utcOffset`, `SysTime(dt, tz)`.
- Durations: `dur!"seconds"(90)`, `90.seconds` (aliases `weeks`, `days`, `hours`, `minutes`, `seconds`, `msecs`, `usecs`, `hnsecs`, `nsecs`), `d.total!"minutes"`, `d.split!("hours", "minutes", "seconds")()`, `abs(d)`, `Duration.max`, `Duration.zero`.
- Clocks: `core.time.MonoTime` is the monotonic timestamp; `Clock.currStdTime` returns hnsecs since midnight, January 1st, 1 A.D. UTC.
- Timing code: `import std.datetime.stopwatch : StopWatch, AutoStart, benchmark; auto sw = StopWatch(AutoStart.yes); work(); writeln(sw.peek.total!"msecs");`; `benchmark!(f1, f2)(1000)` returns `Duration[fun.length]`, one total per function.
- Intervals: `Interval!Date`, `PosInfInterval`, `.contains`, `.intersection`. `TickDuration` is deprecated.
- Sleep: `core.thread.Thread.sleep(100.msecs)`.

Gotchas:
- Use a monotonic clock for durations, not wall-clock differences (clock changes).
- DST gaps/overlaps make local times ambiguous; keep UTC internally.

Verify: unittest converting a known UTC instant to a zone and checking the hour.

## Checked

2026-11-03. Confirmed against: std.datetime.timezone, core.time, std.datetime.stopwatch, std.datetime.systime and std.datetime.interval reference pages.

Removed because the pages read did not confirm it: `TimeZone.getTimeZone` picks per platform, `5.minutes + 30.secs` (no `secs` alias; now `30.seconds`), `benchmark` return type corrected to `Duration[fun.length]`, Windows zone example name replaced by the page's own example.

Method: documentation only; no commands were run.
