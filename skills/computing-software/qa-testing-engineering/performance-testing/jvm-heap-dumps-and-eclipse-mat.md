---
id: computing-software.qa-testing-engineering.performance-testing.jvm-heap-dumps-and-eclipse-mat
name: jvm-heap-dumps-and-eclipse-mat
category: computing-software
field: qa-testing-engineering
product: performance-testing
tags: [jvm-heap-dump, eclipse-mat, dynamic-analysis, memory-leak, java]
level: practitioner
status: draft
description: "Capture JVM heap dumps (jcmd, OOM flags) and find leaks with Eclipse MAT: leak suspects, dominator tree, paths to GC roots and comparing dumps."
sources:
  - https://docs.oracle.com/en/java/javase/21/troubleshoot/diagnostic-tools.html
  - https://eclipse.dev/mat/
  - https://help.eclipse.org/latest/topic/org.eclipse.mat.ui.help/welcome.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# JVM heap dumps and leak analysis (Eclipse MAT)

**Goal:** prove and locate memory leaks found in soak/endurance tests or production OOMs.

## Detecting a leak
During a soak test, watch old-gen usage after full GCs (JFR, GC logs `-Xlog:gc*:file=gc.log`, or JMX metrics). A rising floor after each full GC = leak; a sawtooth returning to the same floor = normal.

## Capturing dumps
```bash
jcmd <pid> GC.heap_dump /dumps/heap-1.hprof       # live objects only by default (forces full GC)
jmap -dump:live,format=b,file=/dumps/heap.hprof <pid>   # older equivalent
```
Always run with:
```text
-XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/dumps/
```
Take two or three dumps at intervals during the soak (e.g. after 1 h, 3 h) for comparison. Dumps are roughly heap-sized and contain sensitive data (tokens, PII): store and share them securely.

## Analysing in Eclipse MAT
1. Open the dump; run **Leak Suspects** report (also headless: `ParseHeapDump.sh heap.hprof org.eclipse.mat.api:suspects`).
2. **Dominator tree:** objects by *retained* heap (memory freed if this object were collected). Large retained sizes in caches, maps, ThreadLocals, listeners are typical.
3. **Path to GC Roots** (exclude weak/soft references): shows who keeps the object alive (static field, thread, classloader).
4. **Histogram compare** between dump 1 and dump 2: classes whose instance count grows steadily.
5. OQL for specifics: `SELECT * FROM java.util.HashMap WHERE size > 10000`.

## Common culprits
Unbounded caches/maps keyed by request data, listeners never removed, ThreadLocals in thread pools, classloader leaks on redeploy, session objects held too long, connection/statement objects not closed.

## Gotchas
- Container memory limits: give the JVM headroom; a dump needs disk space and time (the JVM pauses).
- Large dumps need MAT with more memory (`-Xmx` in `MemoryAnalyzer.ini`).

## Verify
The leak report names the retaining path, the fix is followed by a repeat soak where post-GC heap stays flat.
