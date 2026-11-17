---
id: computing-software.software-engineering.elixir.benchee-benchmark-compare
name: benchee-benchmark-compare
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, benchee, benchmark, microbenchmark, warmup, memory-time, inputs, timer-tc, elixir-profiling]
level: practitioner
status: draft
description: "Compare implementations with Benchee, supplying realistic inputs, warmup and memory measurement, and interpret results."
sources: ["https://hexdocs.pm/benchee"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Benchmarking with Benchee

**Goal:** measure, do not guess.

```elixir
# mix.exs: {:benchee, "~> 1.3", only: :dev}
Benchee.run(
  %{"enum_map" => fn input -> Enum.map(input, &(&1 * 2)) end,
    "for" => fn input -> for x <- input, do: x * 2 end},
  inputs: %{"small" => Enum.to_list(1..100), "large" => Enum.to_list(1..100_000)},
  warmup: 2, time: 5, memory_time: 2, parallel: 1
)
{micros, result} = :timer.tc(fn -> work() end)     # quick one-off timing
```
```bash
MIX_ENV=prod mix run bench/my_bench.exs     # benchmark compiled in prod-like settings
```

## Rules
- Benchmark with realistic input sizes; micro-differences on tiny data are noise.
- Run outside of IEx and (ideally) with `MIX_ENV=prod` / consolidated protocols.
- Watch the deviation column; a high deviation means a noisy machine or GC effects.
- Setup that should not be timed goes in `before_scenario`/`before_each`.
- The JIT (OTP 24+, on supported platforms) changes the relative speed of some code; re-measure after upgrades.

## Self-check
Benchmark `Enum.at` in a loop against `Enum.reduce` to see the O(n) effect.
