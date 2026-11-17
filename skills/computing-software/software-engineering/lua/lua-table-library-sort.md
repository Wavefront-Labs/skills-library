---
id: computing-software.software-engineering.lua.lua-table-library-sort
name: lua-table-library-sort
category: computing-software
field: software-engineering
product: lua
tags: [lua, lua-tables, table-library-sort]
level: practitioner
status: docs-checked
description: "Sort with table.sort comparators that obey strict weak ordering and know sort is not stable."
sources:
  - https://www.lua.org/manual/5.4/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# table.sort, concat, move and stable ordering
- `table.sort(t, function(a, b) return a.n < b.n end)`; the comparator must define a strict weak order, so use `<`, not `<=`.
- `table.sort` is not stable; add a tie-breaker (index) for stable results.
- `table.concat(t, sep, i, j)` requires all elements to be strings or numbers; `table.move(a1, f, e, t [, a2])` copies a1[f..e] to a2 starting at t (a2 defaults to a1, and the ranges may overlap), so `table.move(a, 1, #a, 1, b)` copies a into b.
Verify: sort a list with equal keys and check the tie-breaker.

## Checked
2026-11-02. Confirmed in Lua 5.4 Reference Manual (lua.org/manual/5.4/manual.html) section 6.6 (table.sort, concat, move). Removed: the exact 'invalid order function' message, the 5.3+ tag and the mixed-types remark.
Method: documentation only; no commands were run.
