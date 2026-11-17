---
id: computing-software.software-engineering.java.heap-dump-and-memory-leak-analysis
name: heap-dump-and-memory-leak-analysis
category: computing-software
field: software-engineering
product: java
tags: [java, jvm, heap-dump, eclipse-mat, jcmd, memory-leak, outofmemoryerror, dominator-tree, gc-roots, heapdumponoutofmemoryerror, class-histogram]
level: advanced
status: docs-checked
description: "Find Java memory leaks: capture heap dumps with jcmd or on OOM, read the dominator tree and GC-root paths in Eclipse MAT, and spot classic leak patterns."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/specs/man/jcmd.html", "https://docs.oracle.com/en/java/javase/21/troubleshoot/troubleshooting-memory-leaks.html", "https://help.eclipse.org/latest/topic/org.eclipse.mat.ui.help/welcome.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Heap dumps and memory leak analysis

**Goal:** go from "old gen keeps growing / OutOfMemoryError" to the exact object graph
holding the memory.

## 1. Confirm it is a leak
GC logs or metrics: heap after full/old GC rising steadily across hours = leak. A high
but flat post-GC baseline is sizing, not a leak. Also check which OOM message:
`Java heap space` (heap), `Metaspace` (class loader leak), `Direct buffer memory`
(off-heap NIO), `unable to create native thread` (threads/ulimit).

## 2. Capture
```bash
# Always set in production:
-XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/dumps/

jcmd <pid> GC.class_histogram | head -30          # cheap first look, top classes by bytes
jcmd <pid> GC.heap_dump /dumps/app.hprof           # full dump (pauses the JVM; live objects only by default)
```
- Dump size is roughly used heap; ensure disk space. In containers write to a mounted
  volume, not the ephemeral layer that disappears with the pod.
- Take two dumps some time apart to compare growth.
- Dumps contain secrets and PII; treat them as sensitive data.

## 3. Analyse in Eclipse MAT
1. Open dump, run "Leak Suspects" report.
2. **Dominator tree**: objects sorted by retained size (memory freed if that object
   were collected). The top entries usually are the leak.
3. On a suspect: "Path to GC Roots" (excluding weak and soft references) shows WHO keeps it
   alive (a static field, a thread local, a listener list).
4. Histogram compare between two dumps to see what grows.
For very large dumps, give MAT more heap or run it headless (see the MAT documentation).

## Classic leak patterns
- Static `Map` caches without eviction (use Caffeine with max size/expiry).
- `ThreadLocal` values in pooled threads never removed (`remove()` in finally).
- Listeners/callbacks registered and never unregistered.
- Unbounded queues fed faster than consumed.
- Class-loader leaks on redeploy (Metaspace): threads or JDBC drivers started by the
  webapp holding its loader.
- Hibernate first-level cache in a long-running batch session (clear periodically).

## Checked
2026-10-28: Confirmed in the jcmd reference (GC.class_histogram, GC.heap_dump with an -all option for unreachable objects) and the JDK 21 troubleshooting guide (OOM messages, leak diagnosis). Removed ParseHeapDump.sh and the MemoryAnalyzer.ini hint (not in fetched pages).
Method: documentation only; no commands were run.

## Verify
- [ ] After the fix, post-GC heap is flat under the same load for several hours.
- [ ] HeapDumpOnOutOfMemoryError is set with a persistent path in every environment.
