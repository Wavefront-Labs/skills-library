---
id: computing-software.software-engineering.elixir.spawn-send-receive-mailbox
name: spawn-send-receive-mailbox
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, spawn, send, receive, mailbox, self, pid, process-flag, process-info, spawn-send-receive, elixir-processes]
level: practitioner
status: docs-checked
description: "Spawn processes, send messages, receive with pattern matching and timeouts and inspect mailboxes; know messages are copied and delivery is asynchronous."
sources: ["https://hexdocs.pm/elixir/processes.html", "https://hexdocs.pm/elixir/Process.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# spawn, send and receive

**Goal:** understand the primitives that tasks and other process abstractions build on, following the Elixir processes guide.

```elixir
parent = self()
spawn(fn -> send(parent, {:hello, self()}) end)
receive do
  {:hello, pid} -> "Got hello from #{inspect(pid)}"
end

receive do
  {:hello, msg} -> msg
after
  1_000 -> "nothing after 1s"
end

pid = spawn(fn -> 1 + 2 end)
Process.alive?(pid)                # false: the process already finished
spawn_link(fn -> raise "oops" end) # linked: the failure propagates to the parent
Task.start(fn -> raise "oops" end) # {:ok, pid}; better error reports and introspection
flush()                            # IEx helper: print and clear the shell mailbox
```

## Rules
- All Elixir code runs in processes; they are isolated, concurrent, lightweight (not OS processes) and communicate by message passing.
- `spawn/1` runs a function in another process and returns its PID; the process exits when the function finishes. `self/0` returns the current PID.
- `send/2` does not block: it puts the message in the recipient's mailbox (a process can send to itself). `receive/1` searches the mailbox for a message matching any clause (guards and many clauses are supported) and waits if none matches; add an `after` timeout, and a timeout of 0 when the message is expected to be there already.
- A process started with `spawn/1` that fails only logs an error; the parent keeps running because processes are isolated. `spawn_link/1` (or `Process.link/1`) propagates the failure.
- Most of the time use abstractions built on the primitives: `Task.start/1` and `Task.start_link/1` return `{:ok, pid}` and can be used in supervision trees.
- State is kept in processes that loop, calling themselves after handling each message (private `loop/1` receiving `{:get, key, caller}` or `{:put, key, value}`).
- "Fail fast" / "let it crash": rely on supervisors to restart failed processes rather than catching everything.

## Self-check
Send yourself a message with `send(self(), :hello)` and `flush()` in IEx to see it.

## Checked
Date: 2026-11-02. Confirmed against the Elixir processes guide (spawn, self, send, receive, after, spawn_link, Task.start, flush, state loop, let it crash). Removed: mailbox growth and catch-all advice, make_ref pattern, Process.info and Process.exit(:kill), dead-process message and GenServer.call claims.
Method: documentation only; no commands were run.
