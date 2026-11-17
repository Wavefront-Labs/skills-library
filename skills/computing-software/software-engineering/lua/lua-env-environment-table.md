---
id: computing-software.software-engineering.lua.lua-env-environment-table
name: lua-env-environment-table
category: computing-software
field: software-engineering
product: lua
tags: [lua, env-environment-table]
level: advanced
status: docs-checked
description: "Control global scope with _ENV in Lua 5.2+: globals are fields of _ENV, so `local _ENV = {}` sandboxes a chunk."
sources:
  - https://www.lua.org/manual/5.4/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# _ENV
- Any free name `x` is translated to `_ENV.x`, and every chunk is compiled in the scope of an external local variable named `_ENV`; by default it holds the global environment, which `_G` also references.
- `local _ENV = setmetatable({}, {__index=_G})` isolates assignments while still reading standard functions.
- `load(src, name, "t", env)` sets the chunk's first upvalue, its `_ENV`, to `env`.
- Strict mode: add `__newindex`/`__index` on the env that errors for undeclared globals.
Verify: `local _ENV = {}; x = 1` leaves `_G.x` nil.

## Checked
2026-11-02. Confirmed in Lua 5.4 Reference Manual (lua.org/manual/5.4/manual.html) section 2.2 (_ENV and global variables), 6.1 (_G, load). Removed: the setfenv remark.
Method: documentation only; no commands were run.
