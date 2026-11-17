---
id: computing-software.software-engineering.erlang.timer-bifs
name: timer-bifs
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-time, timer-bifs]
level: practitioner
status: docs-checked
description: "Erlang timers: erlang:send_after, start_timer, cancel_timer, abs option and how the timer module compares."
sources:
  - https://www.erlang.org/doc/apps/erts/erlang.html
  - https://www.erlang.org/doc/apps/stdlib/timer.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# send_after, start_timer and the timer module
**Goal:** schedule work without bottlenecks.

```erlang
Ref = erlang:send_after(5000, self(), tick),                 % sends tick
TRef = erlang:start_timer(5000, self(), data),               % sends {timeout, TRef, data}
Left = erlang:cancel_timer(Ref),                             % remaining ms or false
%% flush a possibly delivered message after cancel:
receive tick -> ok after 0 -> ok end.
timer:sleep(100).
```
- The `timer` module docs say timers created with `erlang:send_after/3` and `erlang:start_timer/3` are more efficient than those of the `timer` module, which was improved in OTP 25 to be more efficient and less susceptible to overload.
- For repeating work, rearm in the handler: `handle_info(tick, S) -> erlang:send_after(1000, self(), tick), ...`.
- `send_after/4` and `start_timer/4` take `{abs, true}` so Time is an absolute Erlang monotonic time in milliseconds; the default `{abs, false}` is relative.

## Gotchas
- `cancel_timer` returns `false` when the timer could not be found (expired, already cancelled or never existed); even then the time-out message may not yet have arrived, so flush if it matters. An integer result is the milliseconds that were left.

## Self-check
Start and cancel a timer and check the returned remaining time.

## Checked

2026-11-03. Confirmed in the `erlang` module page (`send_after`, `start_timer`, `cancel_timer` results, `{abs, Abs}`, the `{timeout, TimerRef, Msg}` message) and the `timer` page (efficiency note, `sleep/1`). Removed: the claim that `timer:` functions all go through one central server process, and the `timer:apply_interval/4` comparison.
Method: documentation only; no commands were run.
