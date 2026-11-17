---
id: computing-software.software-engineering.crystal.http-websocket-params
name: http-websocket-params
category: computing-software
field: software-engineering
product: crystal
tags: [http-websocket-params, http-server-client, websocket, http-params, uri, cookies, multipart, query-string, url-encode, ws, crystal]
level: advanced
status: draft
description: "Use HTTP::WebSocket server and client, URI parsing and HTTP::Params, cookies and multipart parsing."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/shards
  - https://crystal-lang.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# WebSockets, query params, cookies and URI

Goal: handle web details.

- WebSocket server: `ws_handler = HTTP::WebSocketHandler.new { |ws, ctx| ws.on_message { |m| ws.send m }; ws.on_close { } }` placed in the handler chain; client `HTTP::WebSocket.new("wss://host/path")`, `ws.on_message`, `ws.run` (blocks).
- `URI.parse(url)` gives scheme, host, port, path, query; `URI.encode_www_form_component`, `URI.decode_www_form_component`.
- `HTTP::Params.parse("a=1&b=2")`, `params["a"]`, `HTTP::Params.encode({"a" => "1"})`.
- Cookies: `ctx.request.cookies["sid"]?`, `ctx.response.cookies << HTTP::Cookie.new("sid", v, http_only: true, secure: true, samesite: :lax)`.
- Multipart: `HTTP::FormData.parse(ctx.request) { |part| ... }`.

Gotchas:
- Origin checking for WebSockets is your job.
- Always `ws.close` and handle the `on_close` event.
- Set `Secure` and `HttpOnly` on session cookies.

Verify: echo test with two fibers.
