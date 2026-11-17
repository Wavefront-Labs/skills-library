---
id: computing-software.software-engineering.erlang.cowboy-websocket
name: cowboy-websocket
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-web, cowboy-websocket]
level: advanced
status: draft
description: "Cowboy websocket handler: upgrade from init, websocket_init, websocket_handle, websocket_info and frames."
sources:
  - https://ninenines.eu/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cowboy WebSocket handlers
**Goal:** add a WebSocket endpoint.

```erlang
init(Req, State) -> {cowboy_websocket, Req, State}.
websocket_init(State) -> {[], State}.
websocket_handle({text, Msg}, State) -> {[{text, <<"echo: ", Msg/binary>>}], State};
websocket_handle(_Frame, State) -> {[], State}.
websocket_info({push, Text}, State) -> {[{text, Text}], State};
websocket_info(_, State) -> {[], State}.
```
- Actions are returned as a list; `{close, Code, Reason}` closes; ping/pong are handled by Cowboy unless overridden.
- The handler process is the connection process: send it messages with `Pid ! {push, ...}`.
- Set `idle_timeout` and `max_frame_size` in the options to prevent resource exhaustion.

## Gotchas
- Calling `websocket_init` slow work blocks the handshake; spawn or continue later.

## Self-check
Connect with a WebSocket client and send a text frame.
