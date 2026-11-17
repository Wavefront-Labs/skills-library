---
id: computing-software.software-engineering.crystal.benchmark-ips
name: benchmark-ips
category: computing-software
field: software-engineering
product: crystal
tags: [benchmark-ips, benchmark, ips, performance, microbenchmark, warmup, relative-speed, crystal]
level: practitioner
status: draft
description: "Compare implementations with Benchmark.ips, warmup and calculation times, reading iterations per second and relative speed."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/shards
  - https://crystal-lang.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Benchmark.ips

Goal: measure throughput.

```crystal
require "benchmark"
Benchmark.ips(warmup: 2.seconds, calculation: 5.seconds) do |x|
  x.report("map")  { (1..1000).map { |i| i * 2 } }
  x.report("each") { a = [] of Int32; (1..1000).each { |i| a << i * 2 } }
end
```
- Output lists iterations/second with deviation and `x times slower` comparisons.
- ALWAYS build with `crystal build --release`; debug builds mislead.
- Prevent dead-code elimination by using the result: assign to a variable that is later consumed (`x.report("a") { r = f; r.size }` or use `x.report(..) { sink = f }` and print `sink` at the end).

Gotchas:
- Allocation cost and GC pauses add noise; run longer.
- Machine load, CPU frequency scaling and thermals change results.
- Compare algorithms on realistic data sizes.

Verify: the faster variant shows as baseline with `1.00x`.
