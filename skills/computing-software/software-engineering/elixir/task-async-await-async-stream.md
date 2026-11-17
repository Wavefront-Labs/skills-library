---
id: computing-software.software-engineering.elixir.task-async-await-async-stream
name: task-async-await-async-stream
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, task, task-async, task-await, async-stream, max-concurrency, timeout, elixir-task]
level: practitioner
status: docs-checked
description: "Run work concurrently with Task.async/await and bounded parallelism with Task.async_stream, handling timeouts and linked crashes."
sources: ["https://hexdocs.pm/elixir/Task.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Task.async, await and async_stream

**Goal:** parallelise independent calls with bounded concurrency.

```elixir
t = Task.async(fn -> slow_call() end)
result = Task.await(t, 10_000)          # default timeout 5000 ms; exits on timeout

urls
|> Task.async_stream(&fetch/1, max_concurrency: 8, timeout: 15_000, on_timeout: :kill_task, ordered: true)
|> Enum.map(fn {:ok, res} -> res; {:exit, reason} -> {:error, reason} end)   # {:exit, _} only if the caller traps exits

Task.yield_many(tasks, timeout: 5000) ; Task.yield(task, 100) || Task.shutdown(task)
Task.start(fn -> fire_and_forget() end)
```

## Rules
- `Task.async` spawns a process linked to and monitored by the caller; the result comes back as a message that `Task.await/2` receives.
- `async_stream` defaults to `max_concurrency: System.schedulers_online()` and a per-task `timeout` of 5000; `on_timeout` is `:exit` or `:kill_task`; `ordered` controls result order.
- A task crash kills the linked caller; for isolation use `Task.Supervisor.async_nolink/3`.
- Do not pass huge structs into closures; they are copied into the task process.

## Failure modes
- `Task.await/2` exits the caller when the timeout (default 5000) passes before the reply.

## Self-check
Run `Task.async_stream(1..20, fn _ -> Process.sleep(100) end, max_concurrency: 5) |> Stream.run()` and time it: 20 items at 5 in parallel is four rounds of 100 ms.

## Checked
2026-11-03: confirmed against the Elixir Task docs (`await/2` default 5000, `async_stream` options and defaults, `{:exit, reason}` only when trapping exits, `yield/2`, `shutdown/2`, `start/1` for fire-and-forget, linked and monitored tasks, data copied into tasks). Fixed: `yield_many` takes `timeout:` in its options; noted `{:exit, _}` needs trapped exits. Removed: the mailbox claim and the printed exit text.
Method: documentation only; no commands were run.
