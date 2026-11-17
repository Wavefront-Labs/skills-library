---
id: computing-software.software-engineering.lua.lua-pairs-ipairs-next-order
name: lua-pairs-ipairs-next-order
category: computing-software
field: software-engineering
product: lua
tags: [lua, pairs-ipairs-next-order]
level: practitioner
status: docs-checked
description: "Iterate Lua tables safely: ipairs stops at first nil, pairs order is unspecified, and assigning nil to existing fields during traversal is allowed."
sources:
  - https://www.lua.org/manual/5.4/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Table traversal
- `ipairs(t)` iterates the pairs (1,t[1]), (2,t[2]), ... up to the first absent index.
- The order in which `pairs`/`next` enumerate is not specified, even for numeric indices; use a numeric `for` for numeric order, or sort the keys if output must be stable.
- During traversal you may modify existing fields (including setting them to nil), but you should not assign any value to a non-existent field.
Verify: collect keys, `table.sort` them, and compare across two runs.

## Checked
2026-11-02. Confirmed in Lua 5.4 Reference Manual (lua.org/manual/5.4/manual.html) section 6.1 (ipairs, next, pairs). Removed: the 5.3+ __index claim, run-to-run variation, and the iterate-backwards advice.
Method: documentation only; no commands were run.
