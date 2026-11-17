---
id: computing-software.software-engineering.cpp.chrono-clocks-durations-and-time-zones
name: chrono-clocks-durations-and-time-zones
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, cpp-text-io, cpp-ti-chrono, std-chrono, steady-clock, time-point, year-month-day, zoned-time]
level: practitioner
status: docs-checked
description: "Use std::chrono: pick steady_clock or system_clock, durations and time points, C++20 calendar types, and zoned_time with the IANA time zone database."
sources: ["https://en.cppreference.com/w/cpp/chrono", "https://en.cppreference.com/w/cpp/chrono/zoned_time"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# std::chrono

The chrono library (since C++11) defines clocks, time points and durations; C++20 adds time of day, calendar types, time zones and chrono I/O (`parse`, stream output, formatting). The old C-style `time_t`, `difftime` and `CLOCKS_PER_SEC` are provided separately.

## Vocabulary
- A **clock** is an epoch plus a tick rate. A **time point** is the duration that has passed since a specific clock's epoch. A **duration** is a number of ticks of a time unit ("42 seconds" is 42 ticks of a 1-second unit).
- `system_clock`: wall-clock time from the system-wide realtime clock.
- `steady_clock`: monotonic clock that will never be adjusted. Use it for measuring intervals.
- `high_resolution_clock`: the clock with the shortest tick period available.
- C++20 clocks: `utc_clock`, `tai_clock`, `gps_clock`, `file_clock` (file times) and the pseudo-clock `local_t` for local time; `clock_cast` converts time points between clocks.
- Literals: `h`, `min`, `s`, `ms`, `us`, `ns` (C++14), and `y`, `d` for year and day (C++20), from `std::literals::chrono_literals`.

## Timing example (from the reference)
```cpp
const auto start{std::chrono::steady_clock::now()};
// ... work ...
const auto finish{std::chrono::steady_clock::now()};
const std::chrono::duration<double> elapsed_seconds{finish - start};
std::cout << elapsed_seconds << '\n';   // C++20 streams the duration with its unit; before C++20 print .count()
```
A floating-point `duration<double>` holds seconds without a cast.

## Calendar and time zones (C++20)
- Calendar types include `year`, `month`, `day`, `weekday`, `year_month_day`, `year_month_day_last`, `year_month_weekday` and variants; `operator/` builds dates conventionally (for example year/month/day). The tag `last` names the last day or weekday of a month.
- `hh_mm_ss` splits a duration since midnight into hours, minutes, seconds and fractions; the docs say it is primarily a formatting tool.
- `zoned_time<Duration, TimeZonePtr>` pairs a time zone with a time point. It always refers to a valid zone and an existing, unambiguous time point, so it has no move operations (a move copies). Construct it from a zone name and a time point, for example `std::chrono::zoned_time zt{"Asia/Tokyo", std::chrono::system_clock::now()}`; a name missing from the IANA time zone database throws (the reference example catches `std::runtime_error`: "tzdb: cannot locate zone").
- Useful members: `get_sys_time`, `get_local_time`, `get_time_zone`, `get_info`. `std::formatter` and `operator<<` exist for `zoned_time`. Time zone support lives in `tzdb`, `locate_zone`, `current_zone`, with `nonexistent_local_time` and `ambiguous_local_time` exceptions and `choose` to resolve ambiguity.
- Convert UTC to local with, for example, `std::chrono::current_zone()->to_local(tp_utc)`.
- The feature-test macro `__cpp_lib_chrono` has value 201907L for calendars and time zones.

## Rules
- Intervals: `steady_clock`. Timestamps for logs and storage: `system_clock`.
- Keep values as durations until display.

## Checked
Read the cppreference chrono overview page in full and the zoned_time page in full. Removed as unconfirmed: duration_cast truncation, implicit lossless conversion rules, wait_until advice, `file_clock` semantic details beyond its description, std::format output sample, standard library version support table (GCC, MSVC, libc++), date arithmetic examples (month addition validity), overflow example, thread safety of `localtime` and the serialisation advice.
Method: docs-checked 2026-11-09 against the cppreference chrono and zoned_time pages.
