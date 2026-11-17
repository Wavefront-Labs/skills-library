---
id: computing-software.software-engineering.lua.lua-numeric-for-semantics
name: lua-numeric-for-semantics
category: computing-software
field: software-engineering
product: lua
tags: [lua, numeric-for-semantics]
level: practitioner
status: docs-checked
description: "Know numeric for rules in Lua 5.4: evaluated once, loop variable is a copy, float steps accumulate error, and overflow-safe integer loops."
sources:
  - https://www.lua.org/manual/5.4/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Numeric for
- `for i = a, b, step` evaluates the three control expressions once; the manual says you should not change `i` inside the body.
- A step of zero raises an error. If the initial value and step are integers the loop uses integers (the limit need not be an integer) and the control variable never wraps around: the loop ends on overflow.
- Otherwise all three values are converted to floats; beware of floating-point accuracy, and prefer an integer counter times a step.
Verify: `for i=math.maxinteger-1, math.maxinteger do n=n+1 end` terminates with n=2.

## Checked
2026-11-02. Confirmed in Lua 5.4 Reference Manual (lua.org/manual/5.4/manual.html) section 3.3.5. Removed: the exact 'for' step message, the 'count precomputed' mechanism and the 11-or-10 iteration claim (not on the page).
Method: documentation only; no commands were run.
