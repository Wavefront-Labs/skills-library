---
id: computing-software.software-engineering.elixir.phoenix-channels-pubsub-presence
name: phoenix-channels-pubsub-presence
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, phoenix-channel, pubsub, broadcast, socket, join, handle-in]
level: advanced
status: docs-checked
description: "Phoenix Channels: authorising joins, handling and broadcasting events, token authentication, cluster fan-out and delivery limits."
sources: ["https://hexdocs.pm/phoenix/channels.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Channels and PubSub

**Goal:** real-time fan-out between clients and server processes, per the Phoenix Channels guide.

```elixir
defmodule MyAppWeb.RoomChannel do
  use MyAppWeb, :channel
  def join("room:" <> id, _params, socket) do
    if authorized?(socket, id), do: {:ok, assign(socket, :room, id)}, else: {:error, %{reason: "unauthorized"}}
  end
  def handle_in("new_msg", %{"body" => b}, socket) do
    broadcast!(socket, "new_msg", %{body: b}); {:noreply, socket}
  end
end
# endpoint: socket "/socket", MyAppWeb.UserSocket   # authenticate in UserSocket.connect/3
```

## Rules
- A channel implements `join/3`, `terminate/2`, `handle_in/3` and `handle_out/3`. The first job is authorising clients to join a topic in `join/3`; return `{:error, %{reason: "unauthorized"}}` to refuse.
- Authenticate the connection in the socket's `connect` callback. Token authentication (`Phoenix.Token`, passed with the `:auth_token` socket option) is transport agnostic and suits long-running connections better than sessions.
- `broadcast!/3` notifies all joined clients on the socket's topic and invokes their `handle_out/3` callbacks.
- With a cluster, the local PubSub forwards each message to the PubSubs of other nodes, which send it to their own subscribers; by default this uses `Phoenix.PubSub.PG2` (native Erlang VM messaging).
- Delivery is not guaranteed: a client that is offline misses the message and Phoenix does not resend it, and the server does not persist messages (unsent messages are lost on restart). For stronger guarantees persist messages and let clients request missing ones.

## Self-check
Join a topic from a browser console and confirm a broadcast from one client reaches another.

## Checked
2026-11-09. Rewritten from and confirmed against the Phoenix Channels guide (hexdocs.pm/phoenix/channels.html). Removed because the pages read do not state them: the `Phoenix.PubSub.subscribe/broadcast` and `Endpoint.broadcast` calls, all Presence content (CRDT tracking, `Presence.track/4`, `Presence.list/1`), and the large-payload advice. The `phoenix_pubsub` package page is JavaScript-only and could not be read.
Method: documentation only; no commands were run.
