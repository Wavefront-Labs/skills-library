---
id: computing-software.software-engineering.elixir.genserver-init-handle-call-cast-info
name: genserver-init-handle-call-cast-info
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, genserver, handle-call, handle-cast, handle-info, init, start-link, child-spec, genserver-callbacks, elixir-genserver]
level: practitioner
status: docs-checked
description: "Implement a GenServer with a client API and callbacks, reply from handle_call, send async with cast, and receive plain messages in handle_info."
sources: ["https://hexdocs.pm/elixir/GenServer.html", "https://www.erlang.org/doc/apps/stdlib/gen_server.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GenServer callbacks: init, call, cast, info

**Goal:** a correct stateful server module.

```elixir
defmodule Stack do
  use GenServer
  # Client API
  def start_link(init \\ []), do: GenServer.start_link(__MODULE__, init, name: __MODULE__)
  def push(x), do: GenServer.cast(__MODULE__, {:push, x})
  def pop, do: GenServer.call(__MODULE__, :pop)
  # Server callbacks
  @impl true
  def init(list), do: {:ok, list}
  @impl true
  def handle_call(:pop, _from, [h | t]), do: {:reply, {:ok, h}, t}
  def handle_call(:pop, _from, []), do: {:reply, :empty, []}
  @impl true
  def handle_cast({:push, x}, state), do: {:noreply, [x | state]}
  @impl true
  def handle_info(msg, state) do
    require Logger; Logger.warning("unexpected #{inspect(msg)}"); {:noreply, state}
  end
end
```

## Rules
- `start_link` returns only after `init/1` has run; keep it fast and move slow setup to `handle_continue/2` by returning `{:ok, state, {:continue, term}}`.
- Plain messages (including the `:timeout` message) go to `handle_info/2`.
- Keep callbacks small; delegate logic to pure functions in the module.
- `GenServer.call/3` is synchronous with a default timeout of 5000; `cast` is asynchronous.

## Checked
2026-11-03: confirmed against the Elixir GenServer docs (callback return tuples, `{:continue, term}` from `init/1`, `handle_info` receiving `:timeout`, `call` default timeout 5000, `{:already_started, pid}`). Removed: the claim about default `handle_info` logging, back-pressure wording and the self-call deadlock note (not on the pages read).
Method: documentation only; no commands were run.

## Self-check
Start `Stack`, push, pop, and send it a stray message to see the warning.
