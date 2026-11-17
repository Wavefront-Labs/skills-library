---
id: computing-software.software-engineering.lua.lua-metatables-metamethods
name: lua-metatables-metamethods
category: computing-software
field: software-engineering
product: lua
tags: [lua, lua-metatables, metatables-metamethods]
level: advanced
status: docs-checked
description: "Use metatables for defaults, proxies and operator overloading and know metamethod rules."
sources:
  - https://www.lua.org/manual/5.4/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# __index, __newindex, __call, __eq and operator overloading
- `setmetatable(t, {__index = defaults})` supplies keys missing from `t`; `__index` may be a function or a table, and indexing a table metavalue is regular (not raw), so it can chain. `rawget`/`rawset` bypass metamethods.
- `__newindex` runs when assigning to an absent key; Lua then does not do the primitive assignment, so the metamethod calls `rawset` itself if needed.
- `__call` makes a non-function value callable (receives the value first, then the call arguments) and is the only metamethod allowed to return multiple results.
- `__eq` is tried only when both values are tables (or both full userdata) and not primitively equal; the result is converted to a boolean. `__lt` is tried when the operands are not both numbers or both strings.
- Since 5.4 `__lt` no longer emulates `__le`: define `__le` explicitly.
- `__gc` only marks an object for finalization if it is present in the metatable when `setmetatable` is called; adding it later does not mark the object. `__mode` makes weak tables, `__close` serves to-be-closed variables, `__name` may be used by `tostring` and error messages.
- `__metatable` in a metatable is returned by `getmetatable`, and `setmetatable` raises an error on such an object.
Verify: an `__index` chain test with `rawget`.

## Checked
2026-11-02. Confirmed in the Lua 5.4 reference manual: section 2.4 (metamethod list: __index, __newindex, __call, __eq, __lt, __le, __gc, __close, __mode, __name), getmetatable and setmetatable (__metatable), section 2.5.3 (__gc marking), section 8.1 (__lt no longer emulates __le). Removed: the claim that finalizers on tables work from 5.2.
Method: documentation only; no commands were run.
