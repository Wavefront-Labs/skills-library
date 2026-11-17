---
id: computing-software.software-engineering.assembly.perf-annotate
name: perf-annotate
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, perf-annotate, asm-profiling]
level: practitioner
status: draft
description: "Profile with Linux perf and read instruction-level hot spots: perf stat counters, record, report, annotate in Intel syntax, precise events and skid."
sources:
  - https://man7.org/linux/man-pages/man2/syscall.2.html
  - https://sourceware.org/gdb/documentation/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# perf annotate and counters
**Goal:** find which instructions burn cycles.

```sh
perf stat -e cycles,instructions,branches,branch-misses,cache-misses ./prog
perf record -e cycles:pp -F 5000 ./prog          # sample; :pp requests precise events
perf record -g ./prog                            # include call graph (needs frame pointers or --call-graph dwarf)
perf report --stdio | head -40
perf annotate --stdio -M intel -s prog my_func   # instruction-level view, Intel syntax
perf list | grep -i branch                        # discover events
```
- `perf annotate` shows percentage of samples per instruction. The hottest instruction is often the one after the slow one because of sampling skid; precise modifiers (`:p`, `:pp`) reduce it on supporting CPUs.
- Needs symbol information (and `-g` for source lines) and permissions: `kernel.perf_event_paranoid` may restrict unprivileged use.
- IPC (instructions / cycles) from `perf stat` indicates stalls: low IPC suggests cache misses or dependency chains, high IPC suggests compute-bound.
- Virtual machines may not expose hardware counters; use `-e cpu-clock` as a software fallback.
- Pin the process (`taskset -c 2`) and repeat runs for stable numbers.

## Gotchas
- Sampling needs enough runtime (hundreds of milliseconds or more) to give meaningful counts.
- Inlined and optimised code attributes samples to approximate lines.

## Self-check
Annotate a function that loops over an array and explain where the samples concentrate.
