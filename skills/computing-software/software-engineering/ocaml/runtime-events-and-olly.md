---
id: computing-software.software-engineering.ocaml.runtime-events-and-olly
name: runtime-events-and-olly
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, runtime-events, olly, gc-trace, perfetto]
level: advanced
status: docs-checked
description: "Collect GC and custom runtime events with Runtime_events and the olly tool (trace and latency subcommands)."
sources: ["https://erratique.ch/software/logs", "https://ocaml.org/manual/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Runtime_events and olly

```bash
olly trace trace.json ./main.exe           # writes a trace file
olly latency ./main.exe                    # histogram of GC pause durations
OCAML_RUNTIME_EVENTS_START=1 ./main.exe    # start runtime events at program start, without olly
```

## Notes
- OCaml 5.0+ feature: the runtime logs events to a ring buffer, so old events are overwritten by new ones; a program can monitor itself or an external process can read the buffer.
- Custom events are registered with `Runtime_events.User.register` and emitted with `Runtime_events.User.write`.
- `OCAML_RUNTIME_EVENTS_DIR` sets the directory for the `.events` ring buffer files, `OCAML_RUNTIME_EVENTS_PRESERVE` keeps them after exit, and the buffer size is set through `OCAMLRUNPARAM` (`e`).
- Tool names and flags may change; check `olly --help` on your installed version.

## Self-check
- [ ] `olly trace` writes a trace file for the program.

## Checked

2026-11-03. Confirmed against the OCaml 5.5 manual: the runtime tracing chapter (ring buffer, OCAML_RUNTIME_EVENTS_START/DIR/PRESERVE, olly trace and olly latency, Runtime_events.User.register and write) and the ocamlrun page (e option).

Removed or corrected: the opam package name, the non-existent `olly gc-stats` subcommand (replaced by `olly latency`), the 5.1 version claim, Perfetto and chrome://tracing viewer advice, and the perf/memtrace remark.

Method: documentation only; no commands were run.
