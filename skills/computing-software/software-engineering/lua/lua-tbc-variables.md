---
id: computing-software.software-engineering.lua.lua-tbc-variables
name: lua-tbc-variables
category: computing-software
field: software-engineering
product: lua
tags: [lua, lua-closing, tbc-variables]
level: advanced
status: docs-checked
description: "Use the 5.4 attribs <const> and <close> for deterministic cleanup."
sources:
  - https://www.lua.org/manual/5.4/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# local x <close> and <const> attribs
- `local x <close> = obj` closes the value (calls its `__close` metamethod) when the variable goes out of scope, including by break, goto, return or an error. Several to-be-closed variables closing together are closed in reverse order of declaration; a list of variables can contain at most one.
- The value must have a `__close` metamethod or be a false value (nil and false are ignored); a to-be-closed variable behaves like a constant local.
- `local N <const> = 10` declares a constant variable that cannot be assigned to after its initialization.
Verify: raise an error inside the scope and check that cleanup ran.

## Checked
2026-11-02. Confirmed in Lua 5.4 Reference Manual (lua.org/manual/5.4/manual.html) section 3.3.7 (attribs const and close) and 3.3.8. Removed: the claim that attribs are unavailable in 5.3 and LuaJIT (not stated by the 5.4 manual); the io.open example (the manual does not say file handles have __close); 'compile-time' wording.
Method: documentation only; no commands were run.
