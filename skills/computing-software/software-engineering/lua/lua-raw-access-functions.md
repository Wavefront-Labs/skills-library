---
id: computing-software.software-engineering.lua.lua-raw-access-functions
name: lua-raw-access-functions
category: computing-software
field: software-engineering
product: lua
tags: [lua, raw-access-functions]
level: advanced
status: docs-checked
description: "Bypass metamethods with rawget, rawset, rawequal and rawlen, and know when you must (__index recursion, proxies)."
sources:
  - https://www.lua.org/manual/5.4/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Raw access
- `rawget(t,k)` / `rawset(t,k,v)` skip `__index` / `__newindex`; use them inside those handlers to avoid infinite recursion.
- `rawequal(a,b)` skips `__eq`; `rawlen(t)` skips `__len`.
- `pairs(t)` calls the `__pairs` metamethod if there is one; otherwise it returns `next, t, nil`.
- `rawset(t, k, v)` needs an index `k` other than nil and NaN, and returns `t`.
Verify: set `__newindex` to count writes and confirm `rawset` does not trigger it.

## Checked
2026-11-02. Confirmed in Lua 5.4 Reference Manual (lua.org/manual/5.4/manual.html) section 6.1 (rawequal, rawget, rawlen, rawset, pairs). Removed: the '5.2+' tag and the unstated 'errors' wording for rawset.
Method: documentation only; no commands were run.
