---
id: computing-software.systems-network-administration.linux.perf-profiling
name: perf-profiling
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, perf, perf-events, flame-graph, profiling, cpu-bound, hot-path, sampling, perf-top, perf-stat, perf-record, call-graph, dwarf, frame-pointer, sysadmin, performance-troubleshooting]
level: advanced
status: docs-checked
description: "Profile CPU usage with perf record/report/top and flame graphs to find hot code paths in production, without recompiling or instrumenting."
sources:
  - https://docs.kernel.org/admin-guide/perf-security.html
  - https://github.com/torvalds/linux/tree/master/tools/perf/Documentation
  - https://www.brendangregg.com/perf.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# perf profiling — find the hot code path without touching source

**Goal:** when a process is CPU-bound (confirmed via
`computing-software.systems-network-administration.linux.strace-and-ltrace-debugging`'s
`strace -c` showing little syscall time, or just high `%CPU` in `top`), find
*which function* is burning the time using sampling profiling — on a live
process, in production, with single-digit percent overhead.

## 1. The quickest answer: `perf top`
```bash
sudo perf top                   # live, continuously updating, like `top` but by symbol
sudo perf top -p <PID>           # scoped to one process
```
Good for "what's hot right now" during an active incident — no recording
step, immediate feedback, but nothing to save/share afterward.

## 2. Record and report (for a snapshot you can analyze/share)
```bash
sudo perf record -F 99 -p <PID> -g -- sleep 30    # sample at 99Hz for 30s, -g = capture call graphs
sudo perf report                                   # interactive, shows % time per function, drill into callers
sudo perf report --stdio | head -40                # non-interactive summary
```
`-F` sets the sampling frequency in Hz. `-g` is what makes `perf report` show *who called* the hot
function, not just the function itself — without it a hot `memcpy` tells you
nothing about which caller to fix.

## 3. Flame graphs — the visualization that makes call stacks legible
```bash
git clone https://github.com/brendangregg/FlameGraph
sudo perf record -F 99 -p <PID> -g -- sleep 30
sudo perf script > out.perf
./FlameGraph/stackcollapse-perf.pl out.perf > out.folded
./FlameGraph/flamegraph.pl out.folded > flame.svg
```
Width = proportion of total samples (time), not depth — the widest boxes
are where the time actually goes regardless of how deep in the call stack
they sit. A classic footgun: tall, narrow towers mean deep call chains that
each take little time — not where to optimize; short, wide plateaus are the
real targets.

## 4. Why call graphs are sometimes empty or wrong
```bash
perf record -F 99 --call-graph dwarf -p <PID> -- sleep 30   # DWARF-based unwinding, needs debug info
perf record -F 99 --call-graph fp -p <PID> -- sleep 30       # frame-pointer based, needs -fno-omit-frame-pointer at compile time
```
Per perf-record(1), with binaries compiled using `--fomit-frame-pointer` the
default `fp` method produces bogus call graphs; `dwarf` or `lbr` can be used instead. `--call-graph dwarf` works without
frame pointers but needs DWARF debug info present (install `-dbg`/`-debuginfo`
packages for the binary/libraries involved) and is noticeably slower/heavier
per sample. If neither is available, `perf report`'s call graphs will look
flat or wrong — this is the #1 reason a flame graph comes back useless, not
a perf bug.

## 5. perf stat — the cheap first check before profiling
```bash
perf stat -p <PID> sleep 10
```
Gives instructions-per-cycle (IPC), cache miss rates, branch misses, context
switches — a quick signal for *why* something is CPU-bound before spending
time on a full flame graph. Low IPC with high cache-miss
percentages points at memory-access patterns (cache-unfriendly data
structures) rather than raw instruction count; high context-switch count
points at contention/scheduling rather than the code itself being slow.

## 6. Kernel-side symbols and permissions
```bash
cat /proc/sys/kernel/perf_event_paranoid    # -1 = no restrictions; 2 or higher = unprivileged users get user-space events only (perf-security)
sudo sysctl kernel.perf_event_paranoid=1     # relax for a profiling session if seeing only "[unknown]" kernel frames
```
With `perf_event_paranoid=2` or higher, unprivileged profiling sees
user-space events only, making syscall-heavy workloads
look misleadingly all-userspace. Confirm this setting before concluding a
workload "has no kernel time."

## Gotchas
- Sampling overhead scales with frequency — `-F 999`+ on a production box
  under load can itself become a measurable tax; `-F 99` is a sane default,
  push higher only briefly and only when the signal from 99Hz is too sparse.
- Statically-linked or stripped binaries show raw addresses instead of
  function names (`[unknown]` or hex) — `perf buildid-cache` + the matching
  unstripped binary/debug symbols fixes this; profiling a stripped
  production binary with no debug package installed produces a flame graph
  that's visually convincing but practically unreadable.
- JIT'd languages (Java, Node, anything with a VM) need a perf map
  (see the runtime's documentation) or every hot
  frame shows as the VM's own interpreter loop, hiding the actual
  application code that's slow.
- Profiling under a hypervisor/cloud VM sometimes can't see hardware PMU
  counters (`perf stat` falls back to software events, noisier and less
  precise) — run `perf stat` once and check for events reported as unsupported
  before trusting the numbers.

## Verify
- [ ] `perf report -g` shows non-trivial call graphs (not flat/truncated single-frame stacks) — confirms unwinding actually worked.
- [ ] The flame graph's widest plateaus correspond to a function you can name and reason about, not `[unknown]`.
- [ ] A fix targeting the identified hot path is re-measured with the same `perf record` command/duration before/after, not just "it feels faster."
- [ ] `perf_event_paranoid` and symbol availability were checked before concluding a workload has "no kernel time" or "no hot path."

## Checked

Checked 2026-10-27 against Linux kernel perf documentation (tools/perf/Documentation perf-record, perf-top, perf-report, perf-script, perf-stat; admin-guide/perf-security) and the brendangregg/FlameGraph repository file list, current master, 2026-10-27. Confirmed: perf top -p, perf record -F/-g/--call-graph fp|dwarf|lbr and the frame-pointer caveat, perf report --stdio, perf script, perf stat -p, perf_event_paranoid semantics, FlameGraph stackcollapse-perf.pl and flamegraph.pl names, perf buildid-cache. Removed or softened: rationale for 99 Hz, the claim that modern compilers omit frame pointers by default, hardened-box default claim, Java and Node perf-map tool names, dmesg PMU check, IPC threshold.

Method: documentation only; no commands were run.
