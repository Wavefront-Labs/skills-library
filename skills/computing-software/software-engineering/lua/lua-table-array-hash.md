---
id: computing-software.software-engineering.lua.lua-table-array-hash
name: lua-table-array-hash
category: computing-software
field: software-engineering
product: lua
tags: [lua, lua-tables, table-array-hash]
level: practitioner
status: docs-checked
description: "Use tables as arrays and dictionaries and avoid holes that break the # operator."
sources:
  - https://www.lua.org/manual/5.4/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Arrays, hash parts and the length operator
- Tables are the only data-structuring mechanism; array indices conventionally start at 1. `#t` returns a border: for a sequence it is the length, but for a table with holes it can return any border, e.g. `{10,20,30,nil,50}` has borders 3 and 5.
- `table.insert(t, v)` appends (position defaults to `#t + 1`); `table.remove(t)` removes the last element; `table.remove(t, pos)` shifts later elements down.
- `table.unpack(list [, i [, j]])`; `table.pack(...)` stores `n`, the total argument count; `select("#", ...)` counts all arguments including trailing nils.
- `ipairs` stops at the first absent index; the order of `pairs`/`next` is not specified; you may modify or clear existing fields during traversal but must not assign to a non-existent field.
- Assignment copies the reference, not the table; write a copy function when needed.
Verify: `#({10, 20, 30, nil, 50})` may be 3 or 5; test with explicit counts.

## Checked
2026-11-02. Confirmed in the Lua 5.4 reference manual: section 2.1 (tables), section 3.4.7 (borders and sequences), table.insert, table.remove, table.unpack, table.pack, select, ipairs, next, pairs. Removed: the 'table.remove(t, 1) is O(n)' complexity statement (the manual only says elements are shifted), and the Lua 5.1 `unpack` note.
Method: documentation only; no commands were run.
