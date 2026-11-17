---
id: computing-software.software-engineering.lua.lua-repeat-until-scope-continue
name: lua-repeat-until-scope-continue
category: computing-software
field: software-engineering
product: lua
tags: [lua, repeat-until-scope-continue]
level: practitioner
status: docs-checked
description: "Use repeat-until (condition sees body locals) and emulate continue with goto in Lua."
sources:
  - https://www.lua.org/manual/5.4/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# repeat-until and continue
- The `until` expression can use locals declared in the loop body.
- There is no `continue` statement in the grammar; jump to a label inside the loop body with `goto`, for example `goto continue` with a `::continue::` label at the end of the body.
- A label is visible in the whole block where it is defined except inside nested functions, and a `goto` cannot enter the scope of a local variable.
Verify: skip even numbers with a `goto continue` and print only odds.

## Checked
2026-11-02. Confirmed in Lua 5.4 Reference Manual (lua.org/manual/5.4/manual.html) section 3.3.4 (repeat-until condition sees body locals; goto and label visibility rules; statement grammar). Removed nothing; reworded the goto scope bullet to the manual's rule.
Method: documentation only; no commands were run.
