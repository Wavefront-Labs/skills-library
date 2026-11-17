---
id: computing-software.qa-testing-engineering.performance-testing.jvm-gc-and-thread-monitoring
name: jvm-gc-and-thread-monitoring
category: computing-software
field: qa-testing-engineering
product: performance-testing
tags: [gc-analysis, jvm-monitoring, gc-logs, thread-dumps, jfr]
level: practitioner
status: draft
description: "Monitor JVM services during load tests: GC logs and pauses, heap-after-GC trends, JFR recordings, thread dumps for blocked threads and metrics to correlate with latency."
sources:
  - https://docs.oracle.com/en/java/javase/21/gctuning/
  - https://docs.oracle.com/en/java/javase/21/jfapi/
  - https://docs.oracle.com/en/java/javase/21/troubleshoot/diagnostic-tools.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# JVM GC and thread monitoring under load

## Turn on before the test
```bash
-Xlog:gc*,safepoint:file=/logs/gc.log:time,uptime,level,tags:filecount=5,filesize=50m
-XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/dumps
-XX:StartFlightRecording=duration=0,filename=/dumps/run.jfr,settings=profile    # or start via jcmd later
```
Low overhead; safe in performance environments.

## What to look for in GC logs (GCeasy, GCViewer, JDK Mission Control)
- **Pause times** (p99, max) vs latency SLO: G1 young pauses in tens of ms are normal; full GCs of seconds are not.
- **GC throughput** (% time not in GC): below ~95% under load is a problem.
- **Heap after GC trend:** rising old-gen floor over a soak test = leak.
- Allocation rate (MB/s) climbing with load: object churn hotspots.
- `to-space exhausted` / evacuation failures (G1) or `Allocation Stall` (ZGC) = heap too small for the load.

## JFR on demand
```bash
jcmd <pid> JFR.start name=load duration=5m filename=/dumps/peak.jfr settings=profile
jcmd <pid> JFR.dump name=load
```
Open in JDK Mission Control: hot methods, allocation by class, lock contention (Java Monitor Blocked), socket I/O, thread states.

## Threads
```bash
jcmd <pid> Thread.print > td1.txt; sleep 5; jcmd <pid> Thread.print > td2.txt
```
Three dumps a few seconds apart: many threads `BLOCKED` on the same monitor, or all pool threads `WAITING` on a connection pool, explain throughput plateaus.

## Metrics to graph alongside the test
Heap used/committed, GC pause time per interval, GC count, thread count by state, connection pool active/pending (HikariCP), executor queue sizes. Micrometer/Prometheus JVM metrics make this cheap.

## Gotchas
- Container memory limits vs `-Xmx`: JVM uses heap + metaspace + threads + direct buffers; set `-XX:MaxRAMPercentage` sensibly or the container is OOM-killed with no Java error.
- Heap dumps of large heaps take long and pause the JVM: don't take them mid-measurement.

## Verify
Latency spikes in the load test timeline line up (or don't) with GC pauses; findings name the cause.
