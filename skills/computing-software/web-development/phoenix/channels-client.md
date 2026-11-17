---
id: computing-software.web-development.phoenix.channels-client
name: channels-client
category: computing-software
field: web-development
product: phoenix
tags: [phoenix, channel, websocket, vsn, client, phx-join, heartbeat, protocol]
level: practitioner
status: docs-checked
description: "Write or hand-test a Phoenix Channels client: websocket URL with vsn=2.0.0, V2 JSON message list format, phx_join, phx_leave and heartbeat."
sources:
  - https://hexdocs.pm/phoenix/writing_a_channels_client.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: speak the Phoenix Channels wire protocol from any WebSocket client (also useful for manual testing).

## Connect

Find the `socket` declaration in the app's Endpoint. For `socket "/mobile", MyAppWeb.MobileSocket` the initial HTTP request goes to:

```
[host]:[port]/mobile/websocket?vsn=2.0.0
```

`vsn=2.0.0` selects the built-in V2 JSON serializer, whose messages are lists. Send the standard HTTP-to-WebSocket upgrade headers (or use a library that does; `mint_web_socket` is an Elixir example). The socket module's `connect/3` may require other params or headers.

## Message format (V2)

```
[join_reference, message_reference, topic_name, event_name, payload]
```

- `join_reference`: client-chosen unique value; required on `"phx_join"`. Send the current one on later messages so the server can discard stale messages from a previous join (server accepts `null` for backwards compatibility). Also used as the reference for server pushes that are not replies.
- `message_reference`: client-chosen unique value; echoed in the server's reply.
- `topic_name`: must be a known topic, and joined before use.
- `event_name`: matches the first argument of a server `handle_in`.
- `payload`: serializable value, passed as second argument to `handle_in`.

## Built-in events

```json
["0", "0", "miami:weather", "phx_join", {"some": "param"}]
["0", "1", "miami:weather", "phx_leave", {}]
[null, "2", "phoenix", "heartbeat", {}]
```

Heartbeats are only needed when no other messages are sent; they stop Phoenix closing the connection. The exact `:timeout` is set in the Endpoint.

## App events

Given `def handle_in("report_emergency", payload, socket)` in the channel, send:

```json
["0", "3", "miami:weather", "report_emergency", {"category": "sharknado"}]
```

Because WebSockets are bidirectional, use callbacks for incoming messages. A client must join at least one topic and may join many over one connection.

## Checked

Date: 2026-11-07

Confirmed: read each cited page in full, including embedded code snippets and command output, and matched every claim, command, option, function name and default line by line against the page text. Where a source is a repository guide, the guide markdown on the main branch was read.

Removed or changed: Nothing needed removal; every claim matched the page text.

Method: documentation only; no commands were run.
