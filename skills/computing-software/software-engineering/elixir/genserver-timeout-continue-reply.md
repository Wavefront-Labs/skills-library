---
id: computing-software.software-engineering.elixir.genserver-timeout-continue-reply
name: genserver-timeout-continue-reply
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, handle-continue, genserver-reply, call-timeout, hibernate, idle-timeout, deadlock, genserver-timeouts]
level: advanced
status: docs-checked
description: "Use handle_continue, delayed replies with GenServer.reply/2, idle timeouts and hibernation, and avoid call timeouts and deadlock."
sources: ["https://hexdocs.pm/elixir/GenServer.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GenServer timeouts, continue and calling pitfalls

**Goal:** avoid blocked servers and cryptic exits.

```elixir
def init(arg), do: {:ok, %{}, {:continue, {:load, arg}}}
def handle_continue({:load, arg}, state), do: {:noreply, load(arg, state)}

def handle_call(:slow, from, state) do
  Task.start(fn -> GenServer.reply(from, compute()) end)   # reply later from another process
  {:noreply, state}
end
def init(_), do: {:ok, %{}, 30_000}                        # timeout message :timeout via handle_info after 30s idle
GenServer.call(pid, :req, 15_000)                          # per-call timeout
GenServer.call(pid, :req, :infinity)
```

## Rules
- The idle timeout fires `handle_info(:timeout, state)` when no message arrives within the interval; use `Process.send_after/3` for periodic work.
- `GenServer.reply/2` sends a reply to a client later, after `handle_call` returned `{:noreply, state}`.
- Return `{:stop, reason, reply, state}` to shut down: `terminate/2` is called, then the reply is sent and the process exits with `reason`.
- On an exit signal from the parent, `terminate/2` runs only if the GenServer traps exits.

## Failure modes
- A `GenServer.call` whose reply does not arrive within the timeout exits the caller; calling an unregistered name exits with `noproc`.

## Self-check
Make `handle_call` sleep 6 s and observe the 5000 ms default timeout exit.

## Checked
2026-11-03: confirmed against the Elixir GenServer docs (`handle_continue` via `{:continue, term}`, init timeout value delivering `:timeout` to `handle_info`, `call` default 5000, `:hibernate`, `{:stop, reason, reply, state}`, trapping exits and `terminate/2`) and Process docs (`send_after`). Removed: late-reply/alias behaviour and the mutual-call deadlock claim (not on the pages read).
Method: documentation only; no commands were run.
