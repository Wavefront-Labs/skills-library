---
id: computing-software.software-engineering.lua.lua-locals-globals
name: lua-locals-globals
category: computing-software
field: software-engineering
product: lua
tags: [lua, lua-scope, locals-globals]
level: practitioner
status: docs-checked
description: "Prefer local, detect accidental globals and understand _ENV."
sources:
  - https://www.lua.org/manual/5.4/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# local versus global variables
- A global name `x` is translated to `_ENV.x`; assigning without `local` writes into the current environment (normally the table `_G` refers to). Each chunk is compiled with an external local `_ENV`.
- Local variables are lexically scoped, from the statement after the declaration to the end of the innermost block; locals can have attributes `<const>` and `<close>`.
- Strict mode: `setmetatable(_G, {__newindex = function(_, k) error("global " .. k, 2) end, __index = function(_, k) error("undefined " .. k, 2) end})` turns accidental globals into errors.
- Caching a hot global in a local (`local floor = math.floor`) avoids repeated environment lookups; measure before relying on it.
- `local function f` is sugar for `local f; f = function ... end`, so `f` can call itself; `local f = function` does not see `f` inside the body.
- `_ENV` is a regular name: you can declare a local or parameter named `_ENV` to change how free names resolve.
Verify: assign to an undeclared name under strict mode and confirm the error.

## Checked
2026-11-02. Confirmed in the Lua 5.4 reference manual: sections 2.2 and 3.2 (_ENV and globals), section 3.3.7 (attributes), section 3.4.11 (local function), section 3.5 (visibility), setmetatable and the __index/__newindex events. Removed: the 200-locals and 255-upvalues limits (the manual states 255 only for C closures), the luacheck advice and the `setfenv` remark.
Method: documentation only; no commands were run.
