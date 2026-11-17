---
id: computing-software.software-engineering.elixir.gen-statem-state-machine
name: gen-statem-state-machine
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, gen-statem, state-machine, state-functions, handle-event-function, state-timeout, fsm, statem-callback-mode, elixir-state-machines]
level: sme
status: docs-checked
description: "Model protocols and workflows as gen_statem state machines with state_functions or handle_event_function callback modes and state timeouts."
sources: ["https://www.erlang.org/doc/apps/stdlib/gen_statem.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# gen_statem state machines

**Goal:** implement an explicit finite state machine as an OTP process.

```elixir
defmodule Door do
  @behaviour :gen_statem
  def start_link, do: :gen_statem.start_link({:local, __MODULE__}, __MODULE__, [], [])
  def open, do: :gen_statem.call(__MODULE__, :open)
  @impl true
  def callback_mode, do: :handle_event_function
  @impl true
  def init(_), do: {:ok, :closed, %{}}
  @impl true
  def handle_event({:call, from}, :open, :closed, data), do: {:next_state, :open, data, [{:reply, from, :ok}, {:state_timeout, 5_000, :auto_close}]}
  def handle_event(:state_timeout, :auto_close, :open, data), do: {:next_state, :closed, data}
  def handle_event({:call, from}, _evt, state, data), do: {:keep_state, data, [{:reply, from, {:error, state}}]}
end
```

## Rules
- Return tuples: `{:next_state, new_state, new_data, actions}`, `:keep_state`, `:keep_state_and_data`, `:stop`; actions include `{:reply, from, value}`, timeouts and `:postpone`.
- A state change cancels a `state_timeout`, and a new one belongs to the state being entered.
- Use gen_statem rather than a GenServer with an ad-hoc `:state` field when there are several states with different valid events.
- Call the Erlang `:gen_statem` module directly; the callback shapes are in the OTP `gen_statem` docs.

## Checked
2026-11-03: confirmed against the OTP gen_statem docs (callback_mode `handle_event_function`, `{next_state, ...}` and `{keep_state, ...}` returns, `keep_state_and_data`, `{reply, From, Reply}` and `postpone` actions, `{stop, Reason}`, state change cancelling `state_timeout`). Removed: the `event_timeout` cancellation claim and the claim that Elixir has no wrapper module.
Method: documentation only; no commands were run.

## Self-check
Open the door and confirm it closes itself after the state timeout.
