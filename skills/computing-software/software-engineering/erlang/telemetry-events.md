---
id: computing-software.software-engineering.erlang.telemetry-events
name: telemetry-events
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-logging, telemetry-events]
level: advanced
status: draft
description: "Erlang telemetry library: execute events, attach handlers, span, and wiring metrics reporters."
sources:
  - https://www.erlang.org/doc/apps/kernel/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Telemetry events and metrics
**Goal:** emit metrics events that any backend can consume.

```erlang
telemetry:execute([myapp, request, stop], #{duration => D}, #{route => Route}),
telemetry:attach(<<"log-slow">>, [myapp, request, stop], fun ?MODULE:handle_event/4, #{}),
handle_event(_Event, #{duration := D}, Meta, _Config) when D > 1000000 -> ?LOG_WARNING(Meta);
handle_event(_, _, _, _) -> ok.
telemetry:span([myapp, db, query], #{table => users}, fun() -> {run(), #{}} end).
```
- Event names are lists of atoms; handler functions have arity 4 `(Event, Measurements, Metadata, Config)`.
- Handlers run in the emitting process, so keep them fast; a crashing handler is detached automatically.
- Use module function captures, not anonymous funs, for handlers (performance and reload).
- `telemetry` is a third-party dependency from the BEAM telemetry project, not part of OTP.

## Gotchas
- High-cardinality metadata labels explode time-series backends.

## Self-check
Attach a handler and count events in an ETS counter.
