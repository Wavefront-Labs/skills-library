---
id: computing-software.software-engineering.erlang.schedulers-reductions
name: schedulers-reductions
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-vm, schedulers-reductions]
level: sme
status: draft
description: "BEAM scheduling: one scheduler per core, reductions-based preemption, run queues, dirty schedulers and busy-wait tuning."
sources:
  - https://www.erlang.org/doc/apps/erts/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Schedulers, reductions and fairness
**Goal:** understand how the VM shares CPU.

- By default there is one normal scheduler per logical core; show with `erlang:system_info(schedulers_online)`.
- A process runs until its reduction budget (about 4000 function calls, as documented in the Efficiency Guide) is spent, it waits in `receive`, then is preempted: no process can hog a scheduler, except long-running NIFs or BIFs.
- Dirty schedulers (`+SDcpu`, `+SDio`) run blocking NIFs and file I/O work away from normal schedulers.
- Flags: `+S Schedulers:Online`, `+sbwt none|very_short|short|medium|long|very_long` (busy wait), `+stbt` binding type.
- Check utilisation with `recon:scheduler_usage/1` or `erlang:statistics(scheduler_wall_time)` after `erlang:system_flag(scheduler_wall_time, true)`.

## Gotchas
- In containers with CPU quotas, set `+S` to match the quota or schedulers spin and throttle.

## Self-check
Compare `schedulers_online` with the `+S` flag you pass.
