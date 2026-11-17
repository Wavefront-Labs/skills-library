---
id: computing-software.software-engineering.elixir.nifs-rustler-dirty-schedulers
name: nifs-rustler-dirty-schedulers
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, nif, rustler, dirty-scheduler, native-code, resource-objects]
level: sme
status: docs-checked
description: "NIF risks and dirty schedulers: crashes take down the VM, calls should return in about 1 ms, and long work needs dirty NIFs."
sources: ["https://www.erlang.org/doc/apps/erts/erl_nif.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NIFs and Rustler

**Goal:** decide whether and how to use native code, per the Erlang `erl_nif` documentation (the Rustler crate docs are JavaScript-only and were not readable).

```elixir
defmodule MyApp.Native do
  # stub: called only if the NIF library is not loaded; raises an exception
  def add(_a, _b), do: :erlang.nif_error(:nif_not_loaded)
end
```

## Rules
- A native function that crashes crashes the whole VM, and an erroneously implemented one can corrupt VM internal state, causing a crash or odd behaviour at any later point.
- A well-behaved NIF returns to its caller within about 1 millisecond (the scheduling timeslice is about that long). Longer work must be split up or run as a dirty NIF.
- Dirty NIF flags in the C API: `ERL_NIF_DIRTY_JOB_CPU_BOUND` for CPU-bound jobs and `ERL_NIF_DIRTY_JOB_IO_BOUND` for I/O-bound jobs; `0` for a regular NIF.
- Resource objects are instances of a resource type created with `enif_open_resource_type` when a library loads, which keeps resources from different modules distinguishable.
- Wrappers such as Rustler generate this boilerplate; check their current docs for macro syntax before relying on it.

## Self-check
Why must a 100 ms NIF be marked dirty? A regular NIF should return in about 1 ms; a longer one stalls its scheduler and the processes on it.

## Checked
2026-11-09. Rewritten from and confirmed against the Erlang erts `erl_nif` documentation. Removed because no readable page states them: the Rustler Cargo and Elixir setup and `#[rustler::nif(schedule = "DirtyCpu")]` syntax, version pin, Rust panic handling, `rustler_precompiled`, and the advice to prefer ports or pure Elixir.
Method: documentation only; no commands were run.
