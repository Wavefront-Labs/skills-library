---
id: computing-software.software-engineering.elixir.profilers-eprof-fprof-tprof
name: profilers-eprof-fprof-tprof
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, eprof, fprof, tprof, mix-profile, cpu-profile, flame-graph, profiling-hot-paths, profilers]
level: advanced
status: docs-checked
description: "Find hot functions with mix profile.eprof/fprof (or tprof in newer Elixir/OTP) and read call counts and time."
sources: ["https://hexdocs.pm/mix/Mix.Tasks.Profile.Eprof.html", "https://hexdocs.pm/mix/Mix.Tasks.Profile.Fprof.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# eprof, fprof, tprof and flame graphs

**Goal:** locate the CPU time sink before optimising.

```bash
mix profile.eprof -e "MyApp.work()"                 # function call counts + time
mix profile.fprof -e "MyApp.work()"                 # call timing detail
mix profile.tprof -e "MyApp.work()"                 # unified profiler (see the Mix.Tasks.Profile.Tprof page)
mix profile.cprof -e "MyApp.work()"                 # call counts only
```
```elixir
:eprof.start(); :eprof.profile(fn -> work() end); :eprof.analyze(:total)
```

## Rules
- Profilers add overhead and change timing; use for relative ranking, then benchmark fixes with Benchee.
- Start with measurement of the whole request (Telemetry spans) to know whether CPU, I/O or the database dominates.
- Typical wins: fewer database round trips (preload), avoiding repeated list traversal, ETS for lookups, iodata instead of string concatenation.
- For concurrency problems check scheduler utilisation and message queues.

## Self-check
Profile a function that calls `Enum.at/2` in a loop and see it dominate.

## Checked
2026-11-08: confirmed against Mix.Tasks.Profile.Eprof, Mix.Tasks.Profile.Fprof and Mix.Tasks.Profile.Tprof pages and the Erlang eprof page (start, profile, analyze). Removed: the fprof trace and slowness remark, the tprof version numbers and :scheduler.utilization.
Method: documentation only; no commands were run.
