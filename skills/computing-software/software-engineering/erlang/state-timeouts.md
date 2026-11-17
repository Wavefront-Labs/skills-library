---
id: computing-software.software-engineering.erlang.state-timeouts
name: state-timeouts
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-gen-statem, state-timeouts]
level: advanced
status: docs-checked
description: "OTP gen_statem timers: state_timeout cancelled on state change, event timeout cancelled by any event, and named generic timeouts."
sources:
  - https://www.erlang.org/doc/system/design_principles.html
  - https://www.erlang.org/doc/apps/stdlib/gen_statem.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# State, event and generic timeouts
**Goal:** pick the right timeout for the job.

- `{state_timeout, Time, Msg}` is cancelled by a state change, and a new one belongs to the state being entered; best for "give up in this state". Cancel explicitly with `{state_timeout, cancel}`; `{state_timeout, update, NewContent}` changes the content without changing the expiry time.
- `{timeout, Time, Msg}` (event timeout) is cancelled by any arriving event (retried and inserted events count); use for idle detection. It needs no explicit cancel.
- `{{timeout, Name}, Time, Msg}` generic timers are not cancelled by events or state changes; setting one again with the same name restarts it, and `{{timeout, Name}, cancel}` cancels it.
- Setting any of these with `Time = infinity` starts no timer (and so cancels a running one). `Time = 0` is delivered before any not-yet-received external event, enqueued after already queued inserted and postponed events; it differs subtly from `receive ... after 0`. An event timeout of 0 is only generated if the event queue is empty.
- The explicit cancel actions were added in OTP 22.1.
```erlang
%% requires callback_mode() -> [state_functions, state_enter].
idle(enter, _Old, D) -> {keep_state, D, [{state_timeout, 30000, idle_expired}]};
idle(state_timeout, idle_expired, D) -> {stop, normal, D}.
```

## Gotchas
- Using an event timeout in a state that receives frequent events means it never fires, since any event cancels it.
- Cancelling a generic timeout that is not running inserts a time-out event as if started with Time 0 (noise if the name is misspelled).

## Self-check
Check that leaving and re-entering a state restarts the state_timeout.

## Checked
Read the gen_statem reference (stdlib): state_timeout, event_timeout and generic_timeout semantics, cancel and update actions, infinity, time-out zero ordering, OTP 22.1 note. Removed: the "verify in your OTP" hedge on the cancel form (now confirmed on the page).
Method: docs-only read of cited pages, 2026-11-08
