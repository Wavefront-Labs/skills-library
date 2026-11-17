---
id: computing-software.software-engineering.lua.lua-default-named-arguments
name: lua-default-named-arguments
category: computing-software
field: software-engineering
product: lua
tags: [lua, default-named-arguments]
level: practitioner
status: docs-checked
description: "Emulate default and named parameters in Lua with `x = x or d`, single table arguments, and nil/false pitfalls."
sources:
  - https://www.lua.org/manual/5.4/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Defaults and named args
- `x = x or 10` treats `false` as missing; use `if x == nil then x = 10 end` when false is valid.
- Pass options as one table: `f{width=3, height=4}` (call sugar with a table or string literal), and merge with a defaults table.
- Validate with `assert(type(opts.width)=="number", "width must be a number")`.
- Missing arguments are nil; extra arguments are dropped.
Verify: call `f{}` and `f{flag=false}` and confirm each default.

## Checked
2026-11-02. Confirmed in Lua 5.4 Reference Manual (lua.org/manual/5.4/manual.html) section 3.4.10 (f{...} and f'string' call sugar) and the argument adjustment rules in 3.4.12 (extra values thrown away, missing ones are nil). Nothing removed.
Method: documentation only; no commands were run.
