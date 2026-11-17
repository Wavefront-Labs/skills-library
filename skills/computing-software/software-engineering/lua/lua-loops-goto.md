---
id: computing-software.software-engineering.lua.lua-loops-goto
name: lua-loops-goto
category: computing-software
field: software-engineering
product: lua
tags: [lua, lua-control-flow, loops-goto]
level: practitioner
status: docs-checked
description: "Write numeric and generic for loops, avoid float step errors and use goto continue."
sources:
  - https://www.lua.org/manual/5.4/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# for loops, generic for, goto and break
- Numeric `for i = 1, 10, 2`: the three expressions are evaluated once; with integer start and step the loop uses integers (the limit need not be an integer), otherwise floats, with floating-point accuracy caveats. A zero step raises an error. For integer loops the control variable never wraps around. Do not assign to the control variable.
- Generic for: `for k, v in pairs(t)`, `for i, v in ipairs(t)`, `for w in s:gmatch("%a+")`; `explist` yields an iterator function, a state, an initial control value and a closing value (5.4), which acts like a to-be-closed variable.
- There is no `continue` statement; use `goto continue` with `::continue::` placed where the goto can see it. A goto may jump to any visible label as long as it does not enter the scope of a local variable. A label cannot be declared where a same-named label is visible.
- `break` ends the innermost loop. `return` must be the last statement of a block (use `do return end`).
Verify: loop with a float step and print the count.

## Checked
2026-11-02. Confirmed in the Lua 5.4 reference manual: sections 3.3.4 (goto, labels, break, return) and 3.3.5 (numerical and generic for, closing value), section 8.1 (integer for loop never wraps). Removed: the claim that the iteration count is precomputed (not stated), the label-at-block-end exception wording, and the repeat-until scope sentence (covered by another skill).
Method: documentation only; no commands were run.
