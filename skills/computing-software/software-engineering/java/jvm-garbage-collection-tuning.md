---
id: computing-software.software-engineering.java.jvm-garbage-collection-tuning
name: jvm-garbage-collection-tuning
category: computing-software
field: software-engineering
product: java
tags: [java, jvm, garbage-collection, g1gc, zgc, shenandoah, gc-tuning, heap-sizing, gc-logs, stop-the-world, jfr, pause-time, allocation-rate, java-garbage-collection]
level: sme
status: docs-checked
description: "Diagnose JVM GC pauses and pick a collector (G1, ZGC, Shenandoah): heap sizing, reading GC logs, and when the fix is allocation rate, not GC flags."
sources: ["https://docs.oracle.com/en/java/javase/21/gctuning/available-collectors.html", "https://docs.oracle.com/en/java/javase/21/gctuning/garbage-first-g1-garbage-collector1.html", "https://docs.oracle.com/en/java/javase/21/docs/specs/man/java.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# JVM garbage collection tuning — fix the allocation rate before the flags

**Goal:** reduce GC pause time and frequency for a latency-sensitive service, using
the actual collector logs as evidence instead of copy-pasted flag combinations.

## 1. Before touching GC flags: is this an allocation-rate problem?
The most common "GC tuning" fix is not a flag — it's reducing how much garbage the
app creates per request (eliminating unnecessary boxing, avoiding string
concatenation in hot loops, reusing buffers, streaming instead of building huge
intermediate collections). A collector tuned perfectly for a wasteful allocation rate
still pauses more than necessary. Use async-profiler or JFR's allocation profiling
to find the actual top allocators before changing any JVM flag.

## 2. Pick the collector for the actual constraint
- **G1**: selected by default on most hardware and OS configurations (`-XX:+UseG1GC` to force
  it). Set a pause-time goal with the option described in the G1 tuning guide; it is a goal,
  not a guarantee.
- **ZGC** (`-XX:+UseZGC -XX:+ZGenerational` for the generational version in JDK 21): pause
  times under a millisecond, independent of heap size, at the cost of some throughput. Aimed
  at applications that need low latency.
- **Shenandoah**: another low-pause collector in builds that include it. Not covered by the
  Oracle JDK 21 tuning guide; check your vendor's documentation and benchmark against ZGC.
- **Parallel GC** (`-XX:+UseParallelGC`): the throughput collector. Oracle suggests it when
  peak throughput matters and pauses of a second or more are acceptable; wrong for a
  latency-sensitive service.
- **Serial GC**: for small data sets (up to about 100 MB) or single-processor machines.
- If the recommended collector misses the goal, first adjust heap and generation sizes, then
  try a different collector.

## 3. Heap sizing
For server deployments `-Xms` and `-Xmx` are often set to the same value (the java command
documentation says so). Measure the actual live set (a heap histogram or heap dump) rather
than sizing by guesswork or "just give it all the RAM."

## 4. Reading GC logs
```
-Xlog:gc*:file=gc.log:time,uptime,level,tags
```
Key numbers per GC event: pause duration, heap occupancy before/after (shows how much
was actually reclaimed — a GC that frees almost nothing means the heap is near-full
of live objects, and more frequent GCs won't help; you need more heap or less
retained data), and for G1 specifically, evacuation failure (the application keeps so much
memory alive that G1 cannot find room to copy to — a strong signal the heap is undersized or
there's a leak).

## Gotchas
- Flags from an old blog post may be defaults now, or deprecated, obsolete or removed in
  current JDKs: the java command page lists them per release. Check against the JDK in use.
- Container memory limits: the JVM's container support is enabled by default
  (`-XX:-UseContainerSupport` turns it off), but a container limit set too close to `-Xmx`
  with no room for non-heap memory (metaspace, thread stacks, native buffers) gets OOM-killed
  by the container runtime, which looks like a crash, not a GC issue.
- Changing the collector without a load test under representative traffic is testing
  a guess, not a fix — always validate pause/throughput numbers before and after under
  the same load profile.

## Verify
- [ ] Allocation profiling identified the actual top allocators before any GC flag
      was changed.
- [ ] Heap sized from a measured live-set, not a guess.
- [ ] GC logs from before and after a change were compared on pause duration AND
      occupancy-after, not just "it feels faster."
- [ ] Container memory limit leaves explicit headroom above `-Xmx` for non-heap
      memory, verified by checking actual RSS under load.

## Checked
2026-11-01. Confirmed against the JDK 21 Garbage Collector Implementation (available collectors) and
G1 pages and the java command page: G1 default, ZGC pause and heap-size claims and flags, Parallel and
Serial guidance, -Xms/-Xmx note, evacuation failure, container support default. Replaced the
non-URL sources with those pages. Removed unconfirmed claims: the MaxGCPauseMillis value, ZGC
release history and CPU-overhead wording, Shenandoah specifics, the JFR command, cgroup version
number, and the GC visualiser tools. Removed the leak-diagnosis section (general practice, not
document-confirmed).
Method: documentation only; no commands were run.

Related: computing-software.software-engineering.java.spring-boot-services,
computing-software.software-engineering.concurrency.profiling-before-optimising
