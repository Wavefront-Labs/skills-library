---
id: computing-software.software-engineering.ruby.ruby-ruby-profiling
name: ruby-ruby-profiling
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, ruby-performance, ruby-profiling]
level: advanced
status: draft
description: "Measure with Benchmark/benchmark-ips and profile with stackprof or ruby-prof before optimising."
sources: ["https://docs.ruby-lang.org/en/", "https://www.ruby-lang.org/en/documentation/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Benchmarking and profiling Ruby code
- `require "benchmark"; Benchmark.realtime { }`; `benchmark-ips` gives iterations/second with variance; `stackprof` (sampling, flamegraph output) and `memory_profiler` for allocations.
- Typical wins: avoid N+1 queries, avoid repeated string building, use `each_with_object`, cache results with `||=`; `GC.stat` and `GC.compact`.
Verify: benchmark before and after under identical Ruby versions.
