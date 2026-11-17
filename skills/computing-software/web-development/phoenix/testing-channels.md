---
id: computing-software.web-development.phoenix.testing-channels
name: testing-channels
category: computing-software
field: web-development
product: phoenix
tags: [phoenix, testing, channelcase, channels, websocket, subscribe-and-join, assert-reply, exunit]
level: practitioner
status: docs-checked
description: "Test Phoenix channels with ChannelCase: generate a channel, subscribe_and_join in setup, and assert replies, broadcasts and server pushes."
sources:
  - https://hexdocs.pm/phoenix/testing_channels.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: integration-test a channel (route, module, callbacks, PubSub, transport) using `Phoenix.ChannelTest`.

## Generate an example
`mix phx.gen.channel Room` creates `lib/hello_web/channels/room_channel.ex`, `test/hello_web/channels/room_channel_test.exs` and `test/support/channel_case.ex`. If `HelloWeb.UserSocket` is missing it offers to create it (plus `assets/js/user_socket.js`). Then:

- add `socket "/socket", HelloWeb.UserSocket, websocket: true, longpoll: false` to `lib/hello_web/endpoint.ex`
- `import "./user_socket.js"` in `assets/js/app.js`
- add the channel route in `lib/hello_web/channels/user_socket.ex`; without it the channel will not function.

## ChannelCase
Tests use `use HelloWeb.ChannelCase`, a case template that imports `Phoenix.ChannelTest`, sets `@endpoint HelloWeb.Endpoint` and starts the SQL Sandbox in `setup`.

## Join in setup
```elixir
setup do
  {:ok, _, socket} =
    HelloWeb.UserSocket
    |> socket("user_id", %{some: :assign})
    |> subscribe_and_join(HelloWeb.RoomChannel, "room:lobby")

  %{socket: socket}
end
```
`subscribe_and_join/3` emulates a client joining and subscribes the test process to the topic; clients must join before they can send or receive events.

## Three test shapes
- Synchronous reply (channel has `handle_in("ping", payload, socket)` returning `{:reply, {:ok, payload}, socket}`):
  ```elixir
  ref = push(socket, "ping", %{"hello" => "there"})
  assert_reply ref, :ok, %{"hello" => "there"}
  ```
- Broadcast (`handle_in("shout", ...)` calls `broadcast/3`): `push(socket, "shout", %{"hello" => "all"})` then `assert_broadcast "shout", %{"hello" => "all"}`. `assert_broadcast/3` checks the PubSub broadcast; to test that a client receives a message use `assert_push/3`.
- Server push (the default `handle_out/3` forwards to the client): call `broadcast_from!(socket, "broadcast", %{"some" => "data"})` then `assert_push "broadcast", %{"some" => "data"}`. `broadcast_from` and `broadcast_from!` differ only in that the bang version raises when the broadcast fails.

For other helpers, see the `Phoenix.ChannelTest` docs.

## Checked

2026-11-08. Read the Phoenix guide Testing Channels in full. Confirmed the generator output, ChannelCase contents, subscribe_and_join/3, and the three test shapes (assert_reply, assert_broadcast, assert_push). Nothing removed.

Method: documentation only; no commands were run.
