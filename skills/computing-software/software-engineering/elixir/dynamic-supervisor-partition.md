---
id: computing-software.software-engineering.elixir.dynamic-supervisor-partition
name: dynamic-supervisor-partition
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, dynamicsupervisor, start-child, partitionsupervisor, max-children, dynamic-children, dynamic-supervisor]
level: advanced
status: docs-checked
description: "Start children at runtime with DynamicSupervisor and spread supervisor load with PartitionSupervisor."
sources: ["https://hexdocs.pm/elixir/DynamicSupervisor.html", "https://hexdocs.pm/elixir/PartitionSupervisor.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DynamicSupervisor and PartitionSupervisor

**Goal:** supervise processes created on demand (sessions, rooms, connections).

```elixir
{DynamicSupervisor, name: MyApp.DynSup, strategy: :one_for_one, max_children: 10_000}

spec = {MyApp.Room, room_id}
{:ok, pid} = DynamicSupervisor.start_child(MyApp.DynSup, spec)
DynamicSupervisor.terminate_child(MyApp.DynSup, pid)
DynamicSupervisor.which_children(MyApp.DynSup) ; DynamicSupervisor.count_children(MyApp.DynSup)

{PartitionSupervisor, child_spec: DynamicSupervisor, name: MyApp.DynSups}
DynamicSupervisor.start_child({:via, PartitionSupervisor, {MyApp.DynSups, room_id}}, spec)
```

## Rules
- Only `:one_for_one` is supported; a DynamicSupervisor starts with no children and starts them on demand via `start_child/2`, with no ordering between children.
- A DynamicSupervisor is a single process and may become a bottleneck; start several through a `PartitionSupervisor` and route with `{:via, PartitionSupervisor, {name, key}}`.
- `max_children` limits the number of children; `start_child` then returns `{:error, :max_children}`.
- Set `restart: :transient` or `:temporary` in the child spec for session-like processes.

## Self-check
Start 3 children, kill one and check `count_children`.

## Checked
2026-11-03: confirmed against the Elixir DynamicSupervisor and PartitionSupervisor docs (`:one_for_one` only, children started on demand, `max_children`, `start_child`, `terminate_child`, `which_children`, `count_children`, bottleneck note, `child_spec:` option and `{:via, PartitionSupervisor, {name, key}}`). Removed: the Registry `via` advice and the default-restart claim (restart values are in the Supervisor child spec docs).
Method: documentation only; no commands were run.
