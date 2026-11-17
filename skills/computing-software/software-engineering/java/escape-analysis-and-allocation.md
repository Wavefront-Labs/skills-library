---
id: computing-software.software-engineering.java.escape-analysis-and-allocation
name: escape-analysis-and-allocation
category: computing-software
field: software-engineering
product: java
tags: [java, java-jvm-internals, escape-analysis, scalar-replacement, allocation-profiling, jit-inlining, object-allocation]
level: advanced
status: docs-checked
description: "Understand when HotSpot's server compiler removes allocations and locks via escape analysis, and how to avoid contorting code or trusting naive benchmarks."
sources: ["https://docs.oracle.com/en/java/javase/21/vm/java-hotspot-virtual-machine-performance-enhancements.html", "https://openjdk.org/projects/code-tools/jmh/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Escape analysis and allocation

## What HotSpot does
Escape analysis lets the Java HotSpot Server Compiler (C2) analyse the scope of a new object's uses and decide whether it must be allocated on the Java heap. It is enabled by default (since Java SE 6u23) and uses a flow-insensitive algorithm. An object ends up in one of three escape states:
- `GlobalEscape`: escapes the method and thread, for example stored in a static field, stored in a field of an escaped object, or returned from the method.
- `ArgEscape`: passed as an argument (or referenced by one) but does not globally escape during the call; determined by analysing the bytecode of the called method.
- `NoEscape`: scalar replaceable, so its allocation can be removed from the generated code.

After the analysis the compiler eliminates allocations of scalar-replaceable objects and the locks tied to them, and also eliminates locks (lock elision) for objects that do not globally escape. It does not turn heap allocation into stack allocation for non-escaping objects.

Documented scenarios: when a method is inlined in a loop and the analysis shows an object is never modified, a defensive copy can be eliminated; synchronized classes such as `StringBuffer` and `Vector` that are used from a single thread can lose their synchronization.

## Practical consequences
- Write clear code with small short-lived objects and profile before contorting it; the optimization applies only in compiled code where the object does not globally escape.
- Because the analysis depends on seeing the object's whole life, keeping hot methods small enough to inline helps (escape-state analysis of called methods is by bytecode analysis for `ArgEscape`).
- Storing the object in a field, static, collection, or returning it makes it `GlobalEscape`; the allocation then stays.

## Measure, don't assume
- Use JMH, the OpenJDK Java harness for building, running and analysing nano, micro, milli and macro benchmarks, rather than hand timing loops.
- Consume benchmark results so the JIT cannot remove the work entirely.
- Compare behaviour with escape analysis disabled (the `-XX:-DoEscapeAnalysis` flag) to confirm the optimization is the cause; this flag is not documented on the cited pages and should be checked against your JDK.

## Checked
Read the Oracle HotSpot performance enhancements page (Escape Analysis section in full) and the OpenJDK JMH project page (which only describes JMH and links elsewhere). The JFR man page was read but supports none of the claims, so it was dropped from sources. Removed as unconfirmed: TLAB description, C2-only versus C1 claims, inlining thresholds (MaxInlineSize, FreqInlineSize, MaxInlineLevel), JMH `-prof gc` and `gc.alloc.rate.norm` details, JFR allocation event names, async-profiler, PrintInlining, PrintEscapeAnalysis, Valhalla status, and the 16-24 B/op expectation.
Method: docs-checked 2026-11-09 against the Oracle JDK 21 HotSpot performance enhancements page and the OpenJDK JMH page.
