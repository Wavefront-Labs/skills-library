---
id: computing-software.software-engineering.lua.lua-table-pack-unpack-select
name: lua-table-pack-unpack-select
category: computing-software
field: software-engineering
product: lua
tags: [lua, table-pack-unpack-select]
level: practitioner
status: docs-checked
description: "Handle varargs and nil holes: table.pack with n, table.unpack ranges, select('#') and select(-1)."
sources:
  - https://www.lua.org/manual/5.4/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pack, unpack, select
- `table.pack(...)` returns a table with all arguments in keys 1, 2, ... and a field `n` with the total count; the result may not be a sequence if some arguments are nil.
- `table.unpack(t, i, j)` returns `t[i]..t[j]`; use `table.unpack(t, 1, t.n)` after pack.
- `select('#', ...)` is the argument count; `select(n, ...)` returns args from n; negative n counts from the end.
Verify: `select('#', nil, nil)` is 2.

## Checked
2026-11-02. Confirmed in Lua 5.4 Reference Manual (lua.org/manual/5.4/manual.html) section 6.1 (select) and 6.6 (table.pack, table.unpack). Removed: the 5.1 unpack global and the 'too many results to unpack' message.
Method: documentation only; no commands were run.
