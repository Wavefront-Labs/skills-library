---
id: computing-software.software-engineering.lua.lua-readonly-proxy-metatable-field
name: lua-readonly-proxy-metatable-field
category: computing-software
field: software-engineering
product: lua
tags: [lua, readonly-proxy-metatable-field]
level: advanced
status: docs-checked
description: "Build read-only tables via proxy plus __newindex errors, and lock metatables with the __metatable field."
sources:
  - https://www.lua.org/manual/5.4/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Read-only and protected metatables
- Proxy pattern: an empty table `p` with `__index = real` and `__newindex = function() error("read-only", 2) end`; add `__len` and `__pairs` so `#p` and `pairs(p)` expose the real contents (`__pairs` is called by `pairs` with the table and its first three results are used).
- A `__metatable` field in the metatable is what `getmetatable` returns, and `setmetatable` raises an error when the existing metatable has that field.
- The VM does not enforce immutability: `rawset(p, k, v)` writes straight into the proxy, bypassing `__newindex`, and `rawset(real, k, v)` changes the real table.
Verify: assigning to the proxy raises the error; `rawset(real, k, v)` still works.

## Checked
2026-11-02. Confirmed in the Lua 5.4 reference manual: section 2.4 (__index, __newindex, __len), pairs (__pairs), getmetatable and setmetatable (__metatable), rawset, error levels. Removed: the exact error text 'cannot change a protected metatable' and the claim that any value works for __metatable beyond the documented getmetatable behaviour.
Method: documentation only; no commands were run.
