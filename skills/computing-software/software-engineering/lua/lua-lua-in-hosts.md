---
id: computing-software.software-engineering.lua.lua-lua-in-hosts
name: lua-lua-in-hosts
category: computing-software
field: software-engineering
product: lua
tags: [lua, lua-embedding-hosts, lua-in-hosts]
level: practitioner
status: draft
description: "Know the Lua dialect and API limits of common hosts such as Neovim, Redis, Nginx/OpenResty and Roblox Luau."
sources: ["https://www.lua.org/manual/5.4/", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Lua in Neovim, Redis, OpenResty and game engines
- Neovim embeds LuaJIT: `vim.api`, `vim.fn`, `vim.keymap.set`, `init.lua`; read `:help lua-guide`.
- Redis `EVAL` runs Lua 5.1 atomically; use `KEYS` and `ARGV` arrays, `redis.call` (errors abort) or `redis.pcall`; scripts must be deterministic where replication matters (check the Redis docs for your version).
- OpenResty (`ngx.*`) runs LuaJIT in nginx; use non-blocking cosockets, never blocking `os.execute` or `io`.
- Roblox Luau is a separate dialect with types (`--!strict`), `continue` and no `goto`; do not assume standard Lua libraries.
- Always check the host's documented Lua version and sandbox.
Verify: run a snippet inside the host to confirm library availability.
