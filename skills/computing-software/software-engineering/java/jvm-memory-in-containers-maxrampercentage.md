---
id: computing-software.software-engineering.java.jvm-memory-in-containers-maxrampercentage
name: jvm-memory-in-containers-maxrampercentage
category: computing-software
field: software-engineering
product: java
tags: [java, jvm-containers, maxrampercentage, containers, kubernetes, oomkilled, jvm-ergonomics]
level: practitioner
status: gated
description: "Size the JVM heap inside containers with MaxRAMPercentage, container limits and non-heap memory, avoiding OOMKilled pods."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/specs/man/java.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# JVM memory in containers

**Goal:** heap sized from the container limit, with headroom for everything that is not heap.

## Behaviour
On Linux the JVM is container-aware by default (`-XX:-UseContainerSupport` disables it) and takes the available memory as the smaller of physical memory and the container limit. `-XX:MaxRAMPercentage` defaults to 25, applied to that amount (`-XX:MaxRAM` defaults to the available memory or 128 GB, whichever is lower), so the default max heap is usually too small for a dedicated service. For small heaps (about 125 MB) `-XX:MinRAMPercentage` (default 50) applies instead.

## Set it
```
-XX:MaxRAMPercentage=70 -XX:InitialRAMPercentage=50
```
- Prefer percentages over fixed `-Xmx` so the same image works with different limits. `-XX:InitialRAMPercentage` defaults to 1.5625.
- Leave room: metaspace, thread stacks, code cache, direct/NIO buffers, GC structures, native libs. A common rule of thumb is 60-75% for heap (not from the JDK docs); lower for many threads or large direct buffers (cap with `-XX:MaxDirectMemorySize`, which is ignored if unset and left to the JVM).
- Set both Kubernetes request and limit memory equal for predictable behaviour; the container memory limit is what the JVM reads (Kubernetes behaviour: see the Kubernetes docs) (gated: unconfirmed, source is paywalled or blocked).
- CPU: override the processor count the VM uses to size thread pools with `-XX:ActiveProcessorCount` when needed (honoured even without container support). G1 is the default collector; `-XX:+UseSerialGC` suits small simple applications.
- Pass flags via `JDK_JAVA_OPTIONS` in the container env; it prepends its content to the command-line options (`JAVA_TOOL_OPTIONS` also exists but is not described on the java man page).

## Diagnose
```
java -XX:+PrintFlagsFinal -version | grep -E 'MaxHeapSize|MaxRAMPercentage|UseContainerSupport'   # (gated: unconfirmed, source is paywalled or blocked)
jcmd <pid> VM.native_memory summary        # needs -XX:NativeMemoryTracking=summary (modes off, summary, detail)
```
OOMKilled with a healthy heap means off-heap growth: check NMT and direct memory. A Java `OutOfMemoryError: Java heap space` means raise the percentage or fix the leak.

## Verify
Under load, container RSS stays under the limit with margin and no restarts; GC logs show stable heap after full collections.

## Checked

2026-11-02. Checked against the Oracle JDK 21 `java` command man page (read in full via two fetches). Confirmed: container support default true and `-XX:-UseContainerSupport`, `MaxRAMPercentage` default 25, `InitialRAMPercentage` 1.5625, `MinRAMPercentage` 50 for ~125 MB heaps, `MaxRAM` definition, `ActiveProcessorCount`, `MaxDirectMemorySize`, `NativeMemoryTracking` modes, `JDK_JAVA_OPTIONS`, G1 default and SerialGC description. Removed: 1 MB thread stack figure, the CPU rounding and serial-GC-below-1-CPU claims, `-Xmx` precedence sentence, exit 137, and `JAVA_TOOL_OPTIONS` as a documented option. Gated: `PrintFlagsFinal` usage and the Kubernetes limit/request advice, not on the fetched page.

Method: documentation only; no commands were run.
