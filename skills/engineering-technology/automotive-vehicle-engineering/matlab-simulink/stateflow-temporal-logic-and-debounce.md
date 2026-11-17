---
id: engineering-technology.automotive-vehicle-engineering.matlab-simulink.stateflow-temporal-logic-and-debounce
name: stateflow-temporal-logic-and-debounce
category: engineering-technology
field: automotive-vehicle-engineering
product: matlab-simulink
tags: [temporal-logic, debounce, after, timers, stateflow, hysteresis]
level: practitioner
status: verified
description: "Implement debounce, hold and timeout behaviour using Stateflow temporal operators instead of ad-hoc counters, with tick-versus-seconds tradeoffs."
sources:
  - "Stateflow documentation, temporal logic operators (mathworks.com)"
  - "https://www.mathworks.com/help/stateflow/ug/using-temporal-logic-in-state-actions-and-transitions.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Temporal logic and debounce timers

- Operators: `after`, `before`, `at`, `every`, `temporalCount`. Absolute-time units (`sec`, `msec`, `usec`) work with `after`, `before` and `temporalCount` only; `at` and `every` are not supported for absolute time (use `tick` or event counts). Prefer `sec` in model time over tick counts so behaviour is independent of the sample time.
- Debounce a fault: use an intermediate `Pending` state entered when the raw fault is true; leave to `Faulty` on `after(0.5, sec)` and back to `Healthy` immediately if the condition drops. The state-entry timer restart gives a clean debounce.
- Hold timers: `Active` -> `Cooldown` on `after(2, sec)`.
- Hysteresis on analogue thresholds belongs outside the chart (Relay block) to keep charts discrete.
- Check resolution: with a 10 ms task, timers below 10 ms are meaningless, and with a discrete sample time actions occur only at integer multiples of it, and for discrete charts the generated code uses integer counters rather than Simulink time (the docs cite Embedded Coder). `after(x,sec)` can misfire if the state stays active beyond 2147418 of the smallest time unit in use.

**Gotchas:** resetting timers on re-entry; counter overflow; `at`/`every` with `sec` (unsupported); enabled subsystems (held states pause the timer, reset states restart it).

## Verify
- [ ] Test confirms a glitch shorter than the debounce does not trip.
- [ ] Test confirms trip occurs within one step of the specified time.
