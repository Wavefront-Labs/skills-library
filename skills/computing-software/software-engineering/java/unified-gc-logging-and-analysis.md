---
id: computing-software.software-engineering.java.unified-gc-logging-and-analysis
name: unified-gc-logging-and-analysis
category: computing-software
field: software-engineering
product: java
tags: [java, gc-logging, xlog, gc-pauses, gceasy, gc-analysis, jvm]
level: advanced
status: docs-checked
description: "Enable and read JVM unified GC logs (-Xlog:gc*): rotation, decorators, pause times, allocation rate, humongous allocations and to-space exhaustion, plus analysis tools."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/specs/man/java.html#enable-logging-with-the-jvm-unified-logging-framework", "https://openjdk.org/jeps/158", "https://docs.oracle.com/en/java/javase/21/gctuning/garbage-first-g1-garbage-collector1.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unified GC logging and analysis

**Goal:** always-on GC logs in production so that pause, throughput and memory
questions can be answered from data.

## Enable
```bash
-Xlog:gc*,safepoint:file=/var/log/app/gc.log:time,uptime,level,tags:filecount=10,filesize=50m
```
- Syntax: `-Xlog[:[what][:[output][:[decorators][:output-options[,...]]]]]`. Output options include
  `filecount` and `filesize` (K, M or G suffix) for rotation, so disk use stays bounded.
- `gc*` selects all GC tags; plain `gc` is the basic GC log.
- The `safepoint` tag carries the old application stopped/concurrent time messages.
- Decorators: omitting them defaults to uptime, level and tags. `time` (`t`) and `uptime` (`u`) make
  lines correlatable with app logs.
- `-Xloggc:file` is replaced by `-Xlog:gc:file`; `PrintGCDetails` maps to `-Xlog:gc*`.

## What to read in G1 logs
- Heap before and after each collection and pause duration per event.
- **Evacuation failure**: the application keeps so much memory alive that an evacuation cannot find
  room to copy to; G1 finishes the collection by leaving moved objects in place. Treat it as a sign of
  an undersized heap or a leak.
- **Humongous allocations**: objects at least half a region are allocated directly in the old
  generation as contiguous regions. They can trigger an early initial-mark collection when occupancy
  exceeds the Initiating Heap Occupancy threshold. Reduce huge buffers or set `-XX:G1HeapRegionSize`
  (the region size is otherwise chosen ergonomically).
- `-XX:InitiatingHeapOccupancyPercent` is only the starting point: G1 adapts the threshold by default
  (Adaptive IHOP).
- After-GC occupancy trending up across Full GCs suggests a leak: take a heap dump.

## Key numbers to extract
- Pause time distribution against your SLO.
- Allocation rate and promotion rate: high allocation drives frequent young collections.
- Live set after full or mixed collections, for sizing the heap.

## Verify
- [ ] Every production JVM writes rotated GC logs with time decorators.
- [ ] No Full GC events under normal load; pause times within SLO.

## Checked
2026-11-01. Confirmed against the JDK 21 java command page (Xlog syntax, rotation options, default
decorators, Xloggc and PrintGCDetails mappings, safepoint tag) and the JDK 21 G1 tuning guide
(evacuation failure, humongous objects, Adaptive IHOP, region size option). Removed unconfirmed
claims: the sample log lines, the runtime `jcmd VM.log` command, overhead and 5% targets, the 3-4x
live-set rule, the removed-flags-fail-startup claim, and the named analysis tools.
Method: documentation only; no commands were run.
