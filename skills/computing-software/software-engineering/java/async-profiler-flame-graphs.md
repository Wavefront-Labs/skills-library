---
id: computing-software.software-engineering.java.async-profiler-flame-graphs
name: async-profiler-flame-graphs
category: computing-software
field: software-engineering
product: java
tags: [java, java-performance, async-profiler, flame-graph, cpu-profiling, allocation-profiling, wall-clock-profiling, perf-events]
level: advanced
status: docs-checked
description: "Profile a live JVM with async-profiler: CPU, wall-clock, alloc and lock modes, HTML flame graph and JFR output, and choosing the right mode."
sources: ["https://github.com/async-profiler/async-profiler", "https://github.com/async-profiler/async-profiler/blob/master/docs/ProfilingModes.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# async-profiler flame graphs

Low-overhead sampling profiler for HotSpot-based JVMs that avoids safepoint bias. It also samples non-Java threads (GC, JIT) and shows native and kernel frames. Official builds: Linux x64/arm64 and macOS x64/arm64.

## Run
```bash
# attach to a running JVM, 30 s CPU profile, interactive HTML flame graph
asprof -d 30 -f flamegraph.html <PID>
asprof -e wall -t -i 50ms -f wall.html <PID>     # wall-clock, per thread: samples running, sleeping and blocked threads
asprof -e lock -t -i 5ms -f lock.html <PID>      # Java monitor contention; top frame is the lock class, counter is nanoseconds
asprof -e alloc -f alloc.html <PID>              # heap allocation sites; top frame is the allocated class
asprof -e cpu,alloc,lock -f profile.jfr <PID>    # several events at once: JFR is the only output that supports this
asprof --loop 1h -f profile-%t.jfr <PID>         # continuous: dump every hour; include %t or each dump overwrites the last
# as an agent at launch
java -agentpath:/path/to/libasyncProfiler.so=start,event=cpu,alloc=2m,lock=10ms,file=profile.jfr -jar app.jar
```
The launcher is `asprof` (built to `build/bin/asprof`). Allocation sampling is TLAB-driven; set the interval with `--alloc` (for example `--alloc 500k` takes about one sample per 500 KB allocated). Counters are heap pressure, so they show relative volume, and only real heap allocations are measured.

## Choosing a mode
- `cpu` (default): CPU time across Java, native, JVM and kernel frames; use for high CPU.
- `wall` with `-t`: where threads spend elapsed time regardless of state; use for slow requests that mostly wait (and for start-up time).
- `alloc`: which call sites allocate the most heap.
- `lock`: Java monitor contention. `--nativelock` covers pthread mutexes and rwlocks.
- `nativemem`: malloc/free tracking for native leaks (convert with `jfrconv --total --nativemem --leak`).
- `--all` enables cpu, wall, alloc, live, lock and nativemem together; the docs advise against it in production, especially for continuous profiling.

## Reading a flame graph
Width is the share of samples, so wide frames cost the most. Look for wide plateaus at the top of the stack. The x-axis is not time. Start with the mode that matches the symptom (above), and compare against a profile from a known-good run.

## Gotchas
- Profile a warmed-up JVM and long enough to collect enough samples; a cold start mostly profiles class loading and the JIT.
- The profiler's own docs have separate pages for container setup, kernel/perf_events permissions and stack-walking options; read them before profiling inside a container.
- JFR is the built-in alternative (`jfr-recordings-with-jcmd-and-jmc`).

## Verify
Run a known busy-loop method for 20 s and confirm it is the widest top frame in the CPU graph.

## Checked

Date: 2026-11-08

Read in full: the async-profiler README and the Profiling Modes page (both from GitHub). Confirmed: asprof usage and `-d`/`-f`, the `wall`, `lock`, `alloc`, `nativemem`, `--all`, `--loop` and multi-event JFR behaviour, the agent option syntax, TLAB-driven sampling and `--alloc`, and supported platforms. Removed because the cited pages do not state them: the overhead percentage, perf_event_paranoid and capability setup, the itimer fallback, DebugNonSafepoints, `--cstack`, include/exclude filters, differential graphs and the Windows remark.

Method: documentation only; no commands were run.
