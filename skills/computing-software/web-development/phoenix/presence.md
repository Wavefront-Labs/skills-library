---
id: computing-software.web-development.phoenix.presence
name: presence
category: computing-software
field: web-development
product: phoenix
tags: [phoenix, presence, track, phx-gen-presence, channel, liveview, online-users]
level: advanced
status: docs-checked
description: "Track online users with Phoenix Presence: phx.gen.presence, track and list in a channel, the JS Presence client, and a LiveView variant using handle_metas."
sources:
  - https://hexdocs.pm/phoenix/presence.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: show who is online, replicated across a cluster, via Channels or LiveView.

## Setup

```console
mix phx.gen.channel Room
mix phx.gen.presence
```

The generator creates `lib/hello_web/channels/presence.ex` (`use Phoenix.Presence, otp_app: :hello, pubsub_server: Hello.PubSub`). Add `HelloWeb.Presence` to the `children` list in `lib/hello/application.ex`.

## Channel

```elixir
def join("room:lobby", %{"name" => name}, socket) do
  send(self(), :after_join)
  {:ok, assign(socket, :name, name)}
end

def handle_info(:after_join, socket) do
  {:ok, _} =
    Presence.track(socket, socket.assigns.name, %{
      online_at: inspect(System.system_time(:second))
    })

  push(socket, "presence_state", Presence.list(socket))
  {:noreply, socket}
end
```

(with `alias HelloWeb.Presence`)

## JavaScript client

`phoenix.js` includes a Presence library that listens for `"presence_state"` and `"presence_diff"` and calls `onSync`:

```javascript
import {Socket, Presence} from "phoenix"
let socket = new Socket("/socket", {authToken: window.userToken})
let channel = socket.channel("room:lobby", {name: window.location.search.split("=")[1]})
let presence = new Presence(channel)

presence.onSync(() => {
  let response = ""
  presence.list((id, {metas: [first, ...rest]}) => {
    response += `<br>${id} (count: ${rest.length + 1})</br>`
  })
  document.querySelector("main").innerHTML = response
})

socket.connect()
channel.join()
```

`presence.list` calls back per presence id with its list of metas (one per connection). Opening `/?name=Alice` in two tabs and `/?name=Bob` in one shows `Alice (count: 2)` and `Bob (count: 1)`; closing tabs lowers the count and eventually removes the user.

Making it safe: passing the name in the URL is only a demo. Use token authentication (see channels-token-auth) and read `socket.assigns.user_id` instead of `socket.assigns.name`.

## LiveView

Each LiveView is a stateful process, so keep the online list in the Presence process and send events to the LiveView, which uses a stream. In `presence.ex` add:

- `init(_opts)` returning `{:ok, %{}}`.
- `fetch(_topic, presences)` to reshape each entry (the guide adds `id` and `user`).
- `handle_metas(topic, %{joins: joins, leaves: leaves}, presences, state)` which, for each join/leave, calls `Phoenix.PubSub.local_broadcast(Hello.PubSub, "proxy:#{topic}", {__MODULE__, {:join | :leave, user_data}})` and returns `{:ok, state}`. A "proxy" topic is used so the LiveView does not receive presence events directly.
- Helpers: `list_online_users()` (`list("online_users")`), `track_user(name, params)` (`track(self(), "online_users", name, params)`), `subscribe()` (`Phoenix.PubSub.subscribe(Hello.PubSub, "proxy:online_users")`).

The LiveView, in `mount/3` when `connected?(socket)`, calls `track_user`, `subscribe`, and seeds `stream(socket, :presences, ...)`. `handle_info({HelloWeb.Presence, {:join, presence}}, socket)` does `stream_insert`; for `:leave` it does `stream_delete` when `presence.metas == []`, else `stream_insert`. Render with `<ul id="online_users" phx-update="stream">` and `:for` over `@streams.presences`. Route: `live "/online/:name", OnlineLive, :index`.

Related: computing-software.web-development.phoenix.channels-token-auth

## Checked

Date: 2026-11-07

Confirmed: read each cited page in full, including embedded code snippets and command output, and matched every claim, command, option, function name and default line by line against the page text. Where a source is a repository guide, the guide markdown on the main branch was read.

Removed or changed: Nothing needed removal; every claim matched the page text.

Method: documentation only; no commands were run.
