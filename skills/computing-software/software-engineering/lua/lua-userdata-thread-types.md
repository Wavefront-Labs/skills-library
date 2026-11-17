---
id: computing-software.software-engineering.lua.lua-userdata-thread-types
name: lua-userdata-thread-types
category: computing-software
field: software-engineering
product: lua
tags: [lua, userdata-thread-types]
level: advanced
status: docs-checked
description: "Know Lua's eight types: how type() reports userdata, thread and function, and how lightuserdata differs from full userdata."
sources:
  - https://www.lua.org/manual/5.4/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# userdata and thread values
- `type(x)` returns one of "nil", "boolean", "number", "string", "table", "function", "thread", "userdata" (a thread is a coroutine).
- Full userdata is a block of memory managed by Lua and can have its own metatable; light userdata is a C pointer value with no individual metatable, equal to any light userdata with the same address. Userdata can only be created or modified through the C API.
- Only tables and full userdata have individual metatables; every other type shares one metatable per type (the string library sets the metatable for strings).
- `math.type(x)` returns "integer" or "float" for numbers and fail for non-numbers.
Verify: `type(io.stdout)` is "userdata"; `type(coroutine.create(print))` is "thread".

## Checked
2026-11-02. Confirmed in the Lua 5.4 reference manual: section 2.1 (eight types, userdata, thread), section 2.4 (individual vs shared metatables), lua_pushlightuserdata, type, math.type. Removed: the claim that full userdata has `__gc` per se beyond the documented finalizer rule (kept in the metatables skill).
Method: documentation only; no commands were run.
