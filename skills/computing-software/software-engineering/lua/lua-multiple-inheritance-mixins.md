---
id: computing-software.software-engineering.lua.lua-multiple-inheritance-mixins
name: lua-multiple-inheritance-mixins
category: computing-software
field: software-engineering
product: lua
tags: [lua, multiple-inheritance-mixins]
level: advanced
status: docs-checked
description: "Implement multiple inheritance in Lua with an __index function that searches parent classes, or copy mixin methods into a class."
sources:
  - https://www.lua.org/manual/5.4/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multiple inheritance
- `setmetatable(Class, {__index = function(t,k) for _,p in ipairs(parents) do local v=p[k]; if v then return v end end end})`. An `__index` function is called with the table and the key, and its first result is the result of the lookup.
- Cache found methods into the class with `rawset(Class, k, v)` (sets without invoking metamethods) so later lookups are direct.
- Mixins: copy functions from a mixin table into the class once at definition time (flatter, faster, but later changes to the mixin are not seen).
- Resolve conflicts with an explicit parent order and document it.
Verify: class C(A,B) calls A's `foo` when both define it.

## Checked
2026-11-08. Confirmed in the Lua 5.4 Reference Manual: section 2.4 (`__index` as a function or table) and `rawset` in the basic functions, read via targeted searches rather than a full read.
Method: documentation only; no commands were run.
