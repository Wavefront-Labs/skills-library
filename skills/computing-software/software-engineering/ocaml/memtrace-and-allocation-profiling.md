---
id: computing-software.software-engineering.ocaml.memtrace-and-allocation-profiling
name: memtrace-and-allocation-profiling
category: computing-software
field: software-engineering
product: ocaml
tags: [ocaml, memtrace, allocation-profiling, memtrace-viewer]
level: advanced
status: docs-checked
description: "Record allocations with memtrace (MEMTRACE and MEMTRACE_RATE env vars) and inspect them in the Memtrace viewer."
sources: ["https://github.com/janestreet/memtrace", "https://raw.githubusercontent.com/janestreet/memtrace/master/src/memtrace.mli"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Memtrace

```lisp
(executable (name main) (libraries memtrace))
```
```ocaml
let () = Memtrace.trace_if_requested ~context:"main" ()
```
```bash
opam install memtrace
MEMTRACE=trace.ctf ./main.exe
```

## Notes
- Memtrace is a streaming client for OCaml's Memprof that writes compact traces of a program's memory use. No special compiler or runtime configuration is needed: link the `memtrace` library and call `Memtrace.trace_if_requested`.
- If the `MEMTRACE` environment variable is set, tracing begins to the file it names and continues until the process exits; if it is absent nothing happens. The optional `~context` string is logged in the trace and can identify trace files.
- If the program daemonises, call `trace_if_requested` after the fork so the right process is traced.
- Sampling: `~sampling_rate` (or the `MEMTRACE_RATE` environment variable, which takes precedence) is the proportion of allocated words sampled. Values above about 1e-4 have some performance impact.
- `trace_if_requested` may raise `Unix.Unix_error` if the file cannot be opened and `Invalid_argument` if `MEMTRACE_RATE` is ill-formed. Manual control: `start_tracing`, `stop_tracing`, `currently_tracing`.
- The Memtrace viewer analyses the trace and shows graphical views with interactive filters; traces record when (if ever) a sample is collected, which helps find leaks.
- `Memtrace.External.alloc` / `free` report non-GC-heap allocations in a trace.

## Self-check
- [ ] The viewer lists your top allocation sites.

## Checked

2026-11-08. Read in full: memtrace README and src/memtrace.mli.
Removed: the viewer command name and install package, the OCaml 4.11+ requirement, allocation-reduction tips and Gc.quick_stat advice (not in the cited pages).
Method: documentation only; no commands were run.
