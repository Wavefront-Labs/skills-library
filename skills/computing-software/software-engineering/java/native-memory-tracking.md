---
id: computing-software.software-engineering.java.native-memory-tracking
name: native-memory-tracking
category: computing-software
field: software-engineering
product: java
tags: [java, native-memory-tracking, nmt, jvm-rss, off-heap-memory, jcmd, jvm]
level: advanced
status: docs-checked
description: "Explain JVM RSS beyond the heap with Native Memory Tracking: enabling NMT, reading jcmd VM.native_memory summaries, baselines and diffs, and malloc arenas outside NMT."
sources: ["https://docs.oracle.com/en/java/javase/21/vm/native-memory-tracking.html", "https://docs.oracle.com/en/java/javase/21/troubleshoot/diagnostic-tools.html#GUID-1F53A50E-86FF-491D-A023-8EC4F1D1AC77", "https://docs.oracle.com/en/java/javase/21/docs/specs/man/jcmd.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Native Memory Tracking

**Goal:** answer "-Xmx is 2 GB, why is the container using 3.5 GB?" with numbers per
JVM subsystem.

## Enable
```bash
java -XX:NativeMemoryTracking=summary -jar app.jar      # off (default) | summary | detail; Oracle documents 5-10% overhead
```
`summary` aggregates by subsystem; `detail` collects by call site. Set at startup: jcmd can stop NMT (`shutdown`) but
cannot start or restart it. For a report at JVM exit add `-XX:+UnlockDiagnosticVMOptions -XX:+PrintNMTStatistics`.

## Read
```bash
jcmd <pid> VM.native_memory summary scale=MB
```
```
Total: reserved=4100MB, committed=2900MB
-                 Java Heap (reserved=2048MB, committed=2048MB)
-                     Class (reserved=1100MB, committed=120MB)      # metaspace + class space
-                    Thread (reserved=310MB, committed=310MB)       # stacks: threads x Xss
-                      Code (reserved=250MB, committed=80MB)        # JIT code cache
-                        GC (reserved=150MB, committed=150MB)       # card tables, remembered sets
-                  Internal / Other (...)                           # incl. direct ByteBuffers
-                    Symbol, Arena, Native Memory Tracking ...
```
Focus on **committed**; reserved is address space only.

## Find growth over time
```bash
jcmd <pid> VM.native_memory baseline
# ... wait under load ...
jcmd <pid> VM.native_memory summary.diff scale=MB
```
The category with a steadily growing `+` delta is your leak: Thread (thread leak), Class
(classloader leak), Other (direct buffers), GC (heap regions growth / G1 remembered sets).

## What NMT does not see
NMT tracks only memory the JVM itself uses, not third-party native code (JNI libraries, RocksDB, some
compression libs) or the user's own native memory, and it is incomplete for the CDS archive. Allocator
fragmentation (glibc malloc arenas) is also outside it. If `RSS - NMT committed` is large, tune the allocator
(for example `MALLOC_ARENA_MAX`), try jemalloc with profiling, and inspect large anonymous mappings with `pmap`.

## Sizing containers
Container limit >= heap + metaspace + code cache + (threads x stack) + direct memory + GC
structures + malloc overhead. Validate with NMT under peak load, not at idle.

## Checked
2026-11-01. Confirmed against Oracle JDK 21 Troubleshooting Guide chapter Native Memory Tracking: -XX:NativeMemoryTracking
values, 5-10% overhead, jcmd VM.native_memory options (summary, detail, baseline, summary.diff, detail.diff,
shutdown, scale), cannot start NMT via jcmd, exit statistics flags, what NMT does not track. Removed: heap 60-75%
sizing figure, glibc arena count, MALLOC_ARENA_MAX=2 value, command pipeline.
The example output block is illustrative, not real data.
Method: documentation only; no commands were run.

## Verify
- [ ] NMT summary committed total approximately matches RSS (`ps -o rss`), gap explained.
- [ ] summary.diff over hours of load shows no monotonically growing category.
