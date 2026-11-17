---
id: computing-software.software-engineering.lua.lua-luasocket-luv
name: lua-luasocket-luv
category: computing-software
field: software-engineering
product: lua
tags: [lua, lua-networking, luasocket-luv]
level: advanced
status: draft
description: "Use LuaSocket for blocking sockets and timeouts, and luv for async IO; handle partial reads."
sources: ["https://www.lua.org/manual/5.4/", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# LuaSocket and libuv (luv) networking
- LuaSocket: `local socket = require("socket"); local c = socket.tcp(); c:settimeout(5); c:connect(host, port); c:send(data); local line, err = c:receive("*l")`; check `err` ("timeout", "closed").
- `socket.select` multiplexes sockets; `socket.http` / `ssl.https` (LuaSec) for HTTP(S) requests.
- luv binds libuv (used by Neovim): `uv.new_tcp()`, `uv.run()`; callbacks, not coroutines; wrap with coroutines to get async/await style.
- Always set timeouts and handle partial sends.
- TLS requires LuaSec and valid certificates; do not disable verification.
Verify: connect to a local echo server in a test.
