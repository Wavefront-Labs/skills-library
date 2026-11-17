---
id: computing-software.web-development.phoenix.channels-basics
name: channels-basics
category: computing-software
field: web-development
product: phoenix
tags: [phoenix, channel, topic, pubsub, websocket, socket, real-time]
level: practitioner
status: docs-checked
description: "Phoenix Channels architecture: transports, endpoint socket, UserSocket channel routes, topics, messages, PubSub, and the phx.gen.socket generator."
sources:
  - https://hexdocs.pm/phoenix/channels.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: understand and wire up the pieces of a Phoenix channel before writing channel logic.

## Concepts

- Clients connect over a transport (WebSocket or long polling), then join topics such as `public_chat` or `product_updates:7`. Clients push to joined topics; the server can push to and broadcast to subscribers.
- One lightweight channel server process exists per client, per topic. Each holds a `%Phoenix.Socket{}` and keeps state in `socket.assigns`.
- Broadcasts go to local PubSub, which forwards one message per extra node, so clients on different nodes subscribed to the same topic all receive it.
- A `Phoenix.Socket.Message` has `topic`, `event`, `payload`, `ref`.
- Topics are strings; `"topic:subtopic"` is the convention, often with record IDs (`"users:123"`).
- PubSub (`Phoenix.PubSub`) defaults to `Phoenix.PubSub.PG2` (native Erlang messaging); a Redis adapter exists if distributed Elixir is unavailable.
- Channels differ from controllers: events flow both directions and connections outlive one request/response. A channel implements clauses of `join/3`, `terminate/2`, `handle_in/3`, `handle_out/3`.

## Endpoint

```elixir
socket "/socket", HelloWeb.UserSocket,
  websocket: true,
  longpoll: false
```

Two default transports exist: websocket and longpoll, configured on the `socket` declaration. On connect Phoenix calls `HelloWeb.UserSocket.connect/2`, where you can authenticate, identify the connection and set default assigns. The socket module also holds channel routes.

## Generate a socket

```console
mix phx.gen.socket User
```

Creates `assets/js/user_socket.js` and `lib/hello_web/channels/user_socket.ex`, and asks you to add the `socket` line above to `lib/hello_web/endpoint.ex`.

## Channel routes

`*` is a wildcard on the topic string:

```elixir
channel "room:*", HelloWeb.RoomChannel
```

`room:lobby` and `room:123` both dispatch to `RoomChannel`.

## Client

```javascript
let socket = new Socket("/socket", {authToken: window.userToken})
```

The JavaScript client ships with new projects (docs at https://phoenix.hexdocs.pm/js/). Import `./user_socket.js` from `assets/js/app.js` (uncomment `import "./user_socket.js"`). Other-language clients exist (Swift, Java, Kotlin, C#, Elixir, GDScript).

Related: computing-software.web-development.phoenix.channels-join-events

## Checked

Date: 2026-11-07

Confirmed: read each cited page in full, including embedded code snippets and command output, and matched every claim, command, option, function name and default line by line against the page text. Where a source is a repository guide, the guide markdown on the main branch was read.

Removed or changed: Nothing needed removal; every claim matched the page text.

Method: documentation only; no commands were run.
