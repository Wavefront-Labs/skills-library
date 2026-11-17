---
id: computing-software.software-engineering.lua.lua-closure-private-state
name: lua-closure-private-state
category: computing-software
field: software-engineering
product: lua
tags: [lua, closure-private-state]
level: practitioner
status: docs-checked
description: "Hide object state in Lua using closures, so fields cannot be reached from outside, at the cost of one closure per method."
sources:
  - https://www.lua.org/manual/5.4/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Private state
- Constructor returns a table of closures sharing local variables: `local count=0; return {inc=function() count=count+1 end, get=function() return count end}`.
- Alternative: keep data in a weak-keyed side table `private[self]`.
Verify: `obj.count` is nil while `obj.get()` returns the state.

## Checked
2026-11-02. Confirmed in Lua 5.4 Reference Manual (lua.org/manual/5.4/manual.html) section 3.5 (local variables used by inner functions are upvalues; each execution of a local statement defines new variables) and 2.5.4 (weak tables). Removed: the memory and metatable trade-off remark.
Method: documentation only; no commands were run.
