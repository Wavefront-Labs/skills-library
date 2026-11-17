---
id: computing-software.software-engineering.elixir.phoenix-liveview-mount-events
name: phoenix-liveview-mount-events
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, liveview, mount, handle-event, handle-params, assigns, streams, push-patch, live-component, phx-click, connected, phoenix-liveview]
level: advanced
status: draft
description: "Build LiveViews: mount/3, handle_params, handle_event, assigns, streams for large lists and understand the disconnected-then-connected double mount."
sources: ["https://hexdocs.pm/phoenix_live_view"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# LiveView lifecycle and events

**Goal:** write interactive server-rendered UI correctly.

```elixir
defmodule MyAppWeb.CounterLive do
  use MyAppWeb, :live_view
  def mount(_params, _session, socket) do
    if connected?(socket), do: Process.send_after(self(), :tick, 1000)
    {:ok, assign(socket, count: 0) |> stream(:items, list_items())}
  end
  def handle_event("inc", %{"by" => by}, socket), do: {:noreply, update(socket, :count, &(&1 + String.to_integer(by)))}
  def handle_info(:tick, socket), do: {:noreply, socket}
  def handle_params(params, _uri, socket), do: {:noreply, assign(socket, :q, params["q"])}
  def render(assigns) do
    ~H"""
    <button phx-click="inc" phx-value-by="1">Count: {@count}</button>
    <ul id="items" phx-update="stream"><li :for={{id, i} <- @streams.items} id={id}>{i.name}</li></ul>
    """
  end
end
```

## Rules
- `mount/3` runs twice for a page load (HTTP render, then WebSocket); do expensive work behind `connected?/1` or in `assign_async`.
- All assigns are held in server memory per connection and diffed on change; use `stream/3` for large collections and `temporary_assigns`-style patterns instead of big lists.
- Always authorise in `handle_event` too, since clients can send any event.
- Clients can tamper with `phx-value-*` params; validate them.
- HEEx interpolation syntax `{@count}` is newer; older versions use `<%= @count %>` (check your LiveView version).

## Self-check
Log in `mount` and note the two calls with `connected?` false then true.
