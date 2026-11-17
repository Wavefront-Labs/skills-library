---
id: computing-software.software-engineering.erlang.time-api
name: time-api
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-time, time-api]
level: advanced
status: docs-checked
description: "Erlang time: system_time, monotonic_time, time warp modes (+C), convert_time_unit, unique_integer and timer:tc."
sources:
  - https://www.erlang.org/doc/apps/erts/time_correction.html
  - https://www.erlang.org/doc/apps/erts/erlang.html
  - https://www.erlang.org/doc/apps/stdlib/timer.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Time API: system, monotonic and unique
**Goal:** measure and timestamp with the right clock.

```erlang
Now = erlang:system_time(millisecond),           % Erlang system time (OS time based, can warp)
T0 = erlang:monotonic_time(microsecond),         % monotonic, for durations
Elapsed = erlang:monotonic_time(microsecond) - T0,
Id = erlang:unique_integer([positive, monotonic]),
erlang:convert_time_unit(1, second, millisecond).
{Micros, Result} = timer:tc(fun() -> work() end).
```
- Take timestamps with `erlang:monotonic_time/0` and subtract to get durations; the result is in the native time unit, convertible with `erlang:convert_time_unit/3`. Pass an explicit unit to `monotonic_time/1` for portability.
- `erlang:monotonic_time/0` is monotonically increasing but not strictly: consecutive calls can return the same value. `unique_integer([monotonic])` is strictly increasing but, per the docs, expensive and poorly scalable; do not pass `monotonic` unless you need it.
- `timer:tc(Fun)` returns `{Time, Value}` with the time in microseconds.
- Time warp modes are selected with the `+C` argument to `erl`: `no_time_warp`, `single_time_warp` or `multi_time_warp`. From OTP 26 (ERTS 14.0) `multi_time_warp` is the default and the preferred configuration, and assumes all code is time warp safe.

## Gotchas
- `erlang:now/0` is strongly discouraged: it behaves badly when system time warps (values can freeze) and scales poorly.

## Self-check
Measure a sleep of 100 ms with both monotonic and system clocks.

## Checked

2026-11-03. Confirmed in "Time and Time Correction in Erlang" (time warp modes, OTP 26 default, `erlang:now/0` warnings, monotonic time differences), the `erlang` module page (`monotonic_time`, `system_time`, `unique_integer` modifiers) and the `timer` page (`tc/1`). Fixed: the old text called `no_time_warp` the safe default; the default changed to `multi_time_warp` in OTP 26. Removed: "deprecated" wording for `erlang:now/0` (the docs say discouraged) and the NTP-jump assertion.
Method: documentation only; no commands were run.
