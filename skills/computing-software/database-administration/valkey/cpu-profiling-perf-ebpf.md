---
id: computing-software.database-administration.valkey.cpu-profiling-perf-ebpf
name: cpu-profiling-perf-ebpf
category: computing-software
field: database-administration
product: valkey
tags: [profiling, perf, flamegraph, bcc, ebpf, funccount, pmc, on-cpu, cpu-bottleneck]
level: advanced
status: docs-checked
description: "Profile Valkey on-CPU bottlenecks with perf record, flame graphs, bcc profile and funccount, and perf stat PMCs for stalls and cache misses."
sources:
  - https://valkey.io/topics/performance-on-cpu/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Use a methodology such as the USE method (utilisation, saturation, errors) first to confirm the CPU is the bottleneck; if time goes to I/O, locks, timers or swapping, this guide does not apply.

Build: keep `-O3` for realistic timings, and keep frame pointers (`-fno-omit-frame-pointer` is the default) so tracers can walk stacks. Build with symbols: `make SERVER_CFLAGS="-g"`. Modules need stack traces too.

Tools: Linux `perf`, bcc/BPF tools, and the FlameGraph repo (`stackcollapse-perf.pl`, `flamegraph.pl`).

Hotspots with perf (60 s at 999 Hz):
```
perf record -g --pid $(pgrep valkey-server) -F 999 -- sleep 60
perf report -g "graph,0.5,caller"
perf script > valkey.perf.stacks
stackcollapse-perf.pl valkey.perf.stacks > valkey.folded.stacks
flamegraph.pl valkey.folded.stacks > valkey.svg
```
To analyse elsewhere, run `perf-archive.sh perf.data` and untar the result into `~/.debug` on the other machine.

With bcc on kernel 4.9 or newer, stacks are counted in the kernel (lower overhead) and output folded directly: `/usr/share/bcc/tools/profile -F 999 -f --pid $(pgrep valkey-server) --duration 60 > valkey.folded.stacks`, then `flamegraph.pl`.

Call counts distinguish slow functions from hot ones: `funccount 'valkey-server:(call*|*Read*|*Write*)' --pid ... --duration 60`.

Hardware counters: `perf stat -e cpu-cycles,instructions,cache-misses,cycle_activity.stalls_mem_any,...` for 60 s gives instructions per cycle and memory stall cycles (the page sample showed 2.30 IPC and 3.537% cache misses). Available events are CPU-specific; check `perf list`. This is counting, not sampling.

## Checked
2026-11-03. Confirmed against the Valkey CPU profiling page (valkey.io/topics/performance-on-cpu/): USE method advice, `-O3` and `-fno-omit-frame-pointer` defaults, `make SERVER_CFLAGS="-g"`, the perf record/report/script and FlameGraph commands at 999 Hz for 60 s, `perf-archive.sh`, bcc `profile` (kernel 4.9 and newer) and `funccount` invocations, and the `perf stat` counters with the 2.30 IPC and 3.537% cache-miss sample. Nothing removed.
Method: documentation only; no commands were run.
