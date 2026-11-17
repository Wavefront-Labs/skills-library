---
id: computing-software.software-engineering.elixir.process-anti-patterns-code-organization
name: process-anti-patterns-code-organization
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, anti-pattern, code-organization-by-process, scattered-process-interfaces, sending-unnecessary-data, unsupervised-process, shared-resource-bottleneck, process-anti-patterns]
level: advanced
status: docs-checked
description: "Do not use processes for code organisation; centralise process interfaces, copy minimal data into messages and supervise every long-lived process."
sources: ["https://hexdocs.pm/elixir/process-anti-patterns.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Process-related anti-patterns

**Goal:** keep concurrency use justified and safe, following the Elixir anti-patterns guide.

```elixir
# Bad: a GenServer that only wraps pure computation (add, subtract) becomes a bottleneck
# Good: plain module functions, called in the caller's process
defmodule Calc do
  def add(a, b), do: a + b
end
```

## Rules
- Documented process smells: code organization by process, scattered process interfaces, sending unnecessary data, unsupervised processes.
- A process is not itself an anti-pattern, but use it to model runtime properties (concurrency, access to shared resources, error isolation), not to organise code; a single process serving all callers can become a bottleneck.
- Scattered interfaces: when many modules call an `Agent`, `GenServer` or other process directly, centralise that interaction in one module with a public API.
- Messages are fully copied to the receiving process (share-nothing). A function passed to `spawn/1`, `Task.async/1` or `Task.async_stream/3` copies every variable it captures, so extract the fields you need before spawning instead of capturing a whole struct such as `conn`. This also applies to `send/2`, `GenServer.call/3` and the initial data in `GenServer.start_link/3`.
- Start every long-running process inside a supervision tree: it gives deterministic start order, shutdown in reverse order, and introspection through tools such as Phoenix LiveDashboard or Erlang's observer.

## Self-check
Identify a GenServer in your code with no state or serialisation need and convert it to a plain module.

## Checked
Date: 2026-11-02. Confirmed against process-anti-patterns (smell list, bottleneck, scattered interfaces, copied messages and captured variables, supervision tree benefits). Removed: 64-byte reference-counted binary note, Counter/Agent sample, Registry/PartitionSupervisor sharding advice, bare spawn rule.
Method: documentation only; no commands were run.
