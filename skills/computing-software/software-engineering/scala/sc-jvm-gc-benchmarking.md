---
id: computing-software.software-engineering.scala.sc-jvm-gc-benchmarking
name: sc-jvm-gc-benchmarking
category: computing-software
field: software-engineering
product: scala
tags: [scala, sc-jvm-performance, jvm-gc-benchmarking]
level: advanced
status: draft
description: "Benchmark Scala code with sbt-jmh and read GC logs to tune the collector."
sources: ["https://docs.scala-lang.org/", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# JMH benchmarking and GC tuning for Scala
- `sbt-jmh`: `@Benchmark` methods in `src/main`, run `sbt "Jmh/run -i 5 -wi 3 -f 1"`; return values or use `Blackhole` to avoid dead-code elimination.
- Boxing is the common Scala cost: `List[Int]` boxes, use `Array[Int]` in hot paths.
- GC logs: `-Xlog:gc*:file=gc.log`; G1 is the default, ZGC (`-XX:+UseZGC`) for low-latency heaps.
- `lazy val` and by-name parameters allocate closures; use sparingly in hot loops.
Verify: compare against a baseline and re-run to see variance.
