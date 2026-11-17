---
id: computing-software.software-engineering.java.jit-compilation-and-warmup
name: jit-compilation-and-warmup
category: computing-software
field: software-engineering
product: java
tags: [java, jit-compilation, tiered-compilation, warmup, c2-compiler, deoptimization, jvm]
level: advanced
status: docs-checked
description: "Understand HotSpot JIT: interpreter, C1/C2 tiers, warmup effects on latency, inspecting compilation and deoptimization, code cache sizing, and options to reduce warmup."
sources: ["https://docs.oracle.com/en/java/javase/21/vm/java-hotspot-virtual-machine-performance-enhancements.html", "https://docs.oracle.com/en/java/javase/21/docs/specs/man/java.html", "https://openjdk.org/jeps/483"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JIT compilation and warmup

**Goal:** explain why a fresh JVM is slow for its first minutes, measure it, and reduce
the impact on users.

## Tiered compilation
1. Code starts **interpreted** while profiling.
2. Hot methods compile with **C1**: quick, lightly optimised, with profiling.
3. Very hot methods recompile with **C2**: inlining, escape analysis, loop
   unrolling, speculative optimisations based on profile data.
Thresholds are invocation/back-edge counters. Result: p99 latency is much worse for the first requests after start.

## Deoptimization
C2 speculates (e.g. "this call site always sees `ArrayList`"). When the assumption breaks
(new type, class loading, uncommon branch), code is deoptimized back to the interpreter and
recompiled later - visible as sudden latency blips.

## Observing
Use the JVM's compilation logging and JFR (see the `java` command reference) to see which methods compile and when deoptimization happens.

## Code cache
If the code cache fills up, compilation stops and everything new runs interpreted (slow). Size it for large applications and watch the logs for code-cache warnings.

## Reducing warmup impact
- **Warm up before taking traffic**: replay representative requests in a readiness check,
  then mark ready (Kubernetes readiness probe).
- **CDS / AppCDS** (startup, class loading) and **JEP 483 AOT class loading & linking** (JDK 24+);
  Project Leyden extends this to AOT profiles and code.
- Avoid megamorphic hot call sites; keep hot methods small enough to inline.
- Benchmarks: use a harness with warmup iterations; never time cold code with a naive timing loop.


## Verify
- [ ] Latency graphs after deploy show warmup handled before traffic (no p99 spike on rollout).
- [ ] No code-cache warnings in logs.

## Checked

- Date: 2026-10-28
- Confirmed: JEP 483 (AOT class loading and linking, delivered in JDK 24) on openjdk.org.
- Removed (not in the fetched Oracle pages): code cache default size and flag names, inlining flags, compiler-thread and CPU-count claims, jcmd/JFR event names, tier numbers, CRaC and native-image claims, JITWatch.
Method: documentation only; no commands were run.
