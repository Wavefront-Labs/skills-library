---
id: computing-software.software-engineering.d.d-gc-behavior-and-tuning
name: d-gc-behavior-and-tuning
category: computing-software
field: software-engineering
product: d
tags: [d-gc-behavior-and-tuning, memory-management, gc, garbage-collector, core-memory, gc-collect, drt-gcopt, gc-tuning, conservative-gc, d]
level: practitioner
status: docs-checked
description: "Know when the D GC collects, what it scans, control it with core.memory GC.disable/collect/minimize/reserve and --DRT-gcopt options (profile, initReserve, gc=conservative)."
sources:
  - https://dlang.org/spec/garbage.html
  - https://dlang.org/phobos/core_memory.html
  - https://dlang.org/dmd-linux.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# How the D garbage collector works and tuning it

Goal: keep GC pauses and memory under control.

- API (`import core.memory;`): `GC.disable()` (reentrant: call `GC.enable()` once per `disable()`; it halts collections across all threads but still allows allocation), `GC.enable()`, `GC.collect()`, `GC.minimize()`, `GC.reserve(bytes)`, `GC.stats()` (its `usedSize` field), `GC.free`, `GC.addRoot`, `GC.removeRoot`, `GC.addRange`, `GC.removeRange` for memory the collector cannot see.
- Runtime options (since 2.067): `app "--DRT-gcopt=profile:1 minPoolSize:16" args`; `--DRT-gcopt=help` lists them. Options: `disable:0|1`, `profile:0|1`, `gc:conservative|precise|manual` (default conservative), `initReserve:N` (MB), `minPoolSize:N`, `maxPoolSize:N`, `incPoolSize:N`, `parallel:N`, `heapSizeFactor:N`, `cleanup:none|collect|finalize`.
- Embed defaults: `extern(C) __gshared string[] rt_options = [ "gcopt=initReserve:100 profile:1" ];`. Evaluation order is `rt_options`, then the `DRT_GCOPT` environment variable (needs `rt_envvars_enabled`), then the command line (can be disabled with `rt_cmdline_enabled = false`).
- Allocation report: compile with `-profile=gc` and read `profilegc.log`; `-vgc` lists allocations at compile time.
- Pattern: `GC.disable()` around a latency-critical section, `GC.collect()` at a quiet point.
- `GC.BlkAttr.NO_SCAN` marks a block as holding no pointers (see core.memory).
- By default the collector marks with all available CPU cores (`parallel:N` sets additional threads).

Gotchas:
- Memory the GC cannot see (for example `malloc`'d blocks holding GC pointers) must be registered with `addRoot`/`addRange`.
- Non-D threads need attaching to the runtime (`thread_attachThis` in `core.thread`).

Verify: compare `GC.stats().usedSize` before and after a workload and run with `--DRT-gcopt=profile:1`.

## Checked

2026-11-03. Confirmed against: the garbage collection spec page (options list, `rt_options`, precise scanning) and core.memory.

Removed because the pages read did not confirm it: mark-sweep/stop-the-world description, `GC.free`/`GC.addRoot` usage details beyond names, `NO_SCAN` false-retention explanation, `thread_attachThis` advice kept only as a pointer.

Method: documentation only; no commands were run.
