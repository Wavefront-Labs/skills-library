---
id: computing-software.software-engineering.java.diagnosing-outofmemoryerror-variants
name: diagnosing-outofmemoryerror-variants
category: computing-software
field: software-engineering
product: java
tags: [java, metaspace, direct-memory-oom, outofmemoryerror, unable-to-create-native-thread, gc-overhead-limit, jvm]
level: advanced
status: docs-checked
description: "Tell OutOfMemoryError variants apart and fix each: Java heap, GC overhead, Metaspace, Direct buffer memory, unable to create native thread, and container OOM kills."
sources: ["https://docs.oracle.com/en/java/javase/21/troubleshoot/troubleshooting-memory-leaks.html", "https://docs.oracle.com/en/java/javase/21/docs/specs/man/java.html", "https://docs.oracle.com/en/java/javase/21/vm/native-memory-tracking.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Diagnosing OutOfMemoryError variants

**Goal:** read the OOM message, go straight to the right memory pool, and fix the cause
rather than just raising -Xmx.

## Always-on flags
```bash
-XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/dumps/
-XX:+ExitOnOutOfMemoryError        # die fast; let the orchestrator restart instead of limping
```

## The variants
**`java.lang.OutOfMemoryError: Java heap space`**
Live objects exceed `-Xmx`. Heap dump -> Eclipse MAT dominator tree / leak suspects. Leak
(growth across Full GCs) vs undersized heap (spiky load, large requests) - see heap dump skill.

**`GC overhead limit exceeded`**
>98% time in GC recovering <2% heap (Parallel GC). Same diagnosis as heap space; the heap is
effectively full.

**`Metaspace`**
Class metadata. Causes: classloader leaks (redeploys in app servers, dynamic proxies,
Groovy/scripting, bytecode generation per request), or a genuinely large app with a low
`-XX:MaxMetaspaceSize`.
```bash
jcmd <pid> VM.metaspace         # per-classloader usage
jcmd <pid> VM.classloader_stats
```
A loaded class count that keeps rising points to a class loader leak.

**`Direct buffer memory`**
NIO direct buffers beyond the direct memory limit (`-XX:MaxDirectMemorySize`; see the java tool
reference for its default). Buffers are freed only when their Java objects are GC'd, so a quiet heap with
busy NIO can exhaust it. Check native memory with NMT and fix leaks of pooled buffers.

**`unable to create native thread`**
Not heap at all: OS or container thread limit, or native memory for
thread stacks exhausted. Thread dump - usually an unbounded thread pool or thread leak.
Reduce `-Xss` only after fixing the leak.

**`Requested array size exceeds VM limit`** / **`Compressed class space`**: bug allocating
a huge array; class space sizing (`CompressedClassSpaceSize`).

## No Java error, process just disappears
Container OOM kill (`OOMKilled`): total RSS (heap + metaspace + code cache +
thread stacks + direct + malloc) exceeded the cgroup limit. Size the heap with
`-XX:MaxRAMPercentage` below 100 and measure non-heap with Native Memory Tracking.

## Checked
2026-10-28: Confirmed in the Oracle JDK 21 troubleshooting guide, jcmd reference and NMT page: the GC overhead limit message (about 98% of time in GC, under 2% of heap recovered), Metaspace, Direct buffer memory, unable to create native thread, Requested array size exceeds VM limit, jcmd VM.classloader_stats, NMT. Removed GC.class_stats (not in the jcmd reference), jstat, ulimit/pids.max, exit code 137, the Netty flag, a gc log flag line and the fixed 70 percent figure.
Method: documentation only; no commands were run.

## Verify
- [ ] Heap dumps are written to a volume that survives the restart.
- [ ] Each incident's OOM message type is recorded and matched to the right tool.
