---
id: computing-software.software-engineering.elixir.agent-get-update-state
name: agent-get-update-state
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, agent, agent-get, agent-update, agent-get-and-update, agent-state, start-link, elixir-agent]
level: practitioner
status: docs-checked
description: "Wrap small pieces of state in an Agent with get/update/get_and_update, keeping the logic in a module and the functions short."
sources: ["https://hexdocs.pm/elixir/Agent.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Agent for simple shared state

**Goal:** a simple mutable cell with a clean API.

```elixir
defmodule Counter do
  use Agent
  def start_link(initial \\ 0), do: Agent.start_link(fn -> initial end, name: __MODULE__)
  def value, do: Agent.get(__MODULE__, & &1)
  def inc, do: Agent.update(__MODULE__, &(&1 + 1))
  def next, do: Agent.get_and_update(__MODULE__, fn n -> {n, n + 1} end)
end
# supervisor: children = [{Counter, 10}]
```

## Rules
- The function passed to `get/update` runs inside the Agent process; slow work there blocks all callers. Do heavy computation in the caller and only read/write state in the Agent.
- `use Agent` defines `child_spec/1` so it can sit in a supervision tree.
- Outgrown Agents (needing messages, timeouts, handle_info) should become a GenServer.

## Failure modes
- Agent calls have a timeout (see the Agent docs for the default and how to change it).

## Self-check
Run `Counter.next/0` from many concurrent tasks and verify no duplicate values.

## Checked
2026-11-02: confirmed against Agent module docs (functions run inside the agent; use Agent defines child_spec/1; supervision). Removed: ETS/persistent_term advice, timeout default.
Method: documentation only; no commands were run.
