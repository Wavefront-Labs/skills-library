---
id: computing-software.software-engineering.elixir.schedulers-backpressure-bottlenecks
name: schedulers-backpressure-bottlenecks
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, schedulers, backpressure, mailbox-overload, partitioning, scheduler-utilization, process-count, erl-flags, concurrency-tuning]
level: sme
status: docs-checked
description: "Find and fix concurrency bottlenecks: single hot processes, unbounded mailboxes, missing backpressure and misconfigured VM flags."
sources: ["https://www.erlang.org/doc/apps/erts/erl_cmd.html", "https://hexdocs.pm/elixir/process-anti-patterns.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Schedulers, backpressure and bottlenecks

**Goal:** keep latency flat under load.

```elixir
:erlang.system_info(:schedulers_online) 
GenServer.call(srv, req, 5_000)                # synchronous call = natural backpressure
Task.Supervisor.async_stream_nolink(sup, items, &work/1, max_concurrency: 50)
# shard a hot GenServer: PartitionSupervisor + {:via, PartitionSupervisor, {name, key}}
```
Scheduler flags such as `+S` and `+sbwt` are described in the erl command reference.

## Rules
- A single GenServer processes messages serially; if its queue grows, split the work (partition by key), move reads to ETS, or reduce work per message.
- Prefer `call` (bounded by a timeout) or demand-driven designs (GenStage, Broadway) over unbounded `cast`/`send` floods.
- Limit parallelism explicitly (`max_concurrency`, pool sizes); default unlimited spawning can exhaust memory or downstream services.
- Measure first; do not tune VM flags without evidence.

## Self-check
Flood a slow GenServer with casts in IEx and watch its mailbox grow.

## Checked
2026-11-08: confirmed against the erl command reference (+S, +sbwt, schedulers) and the Elixir process anti-patterns guide (GenServer call timeout, unbounded sends, serial message handling). Removed: :scheduler.utilization, Process.info message_queue_len, the ELIXIR_ERL_OPTIONS example, :recon and the container CPU remark.
Method: documentation only; no commands were run.
