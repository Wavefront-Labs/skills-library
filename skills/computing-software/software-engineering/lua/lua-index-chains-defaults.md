---
id: computing-software.software-engineering.lua.lua-index-chains-defaults
name: lua-index-chains-defaults
category: computing-software
field: software-engineering
product: lua
tags: [lua, index-chains-defaults]
level: practitioner
status: docs-checked
description: "Use __index as a table or function for inheritance chains and default field values, and avoid costly deep chains."
sources:
  - https://www.lua.org/manual/5.4/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# __index
- `setmetatable(t, {__index = defaults})` falls back to `defaults[k]` on a missing key.
- `__index` as a function receives `(t, k)` and can compute lazily and cache with `rawset`.
- Indexing the `__index` value is a regular, not raw, access, so it can trigger another `__index` and form a chain.
Verify: `t.missing` returns the default and `rawget(t,'missing')` is nil.

## Checked
2026-11-02. Confirmed in Lua 5.4 Reference Manual (lua.org/manual/5.4/manual.html) section 2.4 (__index event: function receives table and key; a table is indexed with the key, non-raw). Removed: the performance remark about deep chains and the 'never errors' claim, neither stated on the page.
Method: documentation only; no commands were run.
