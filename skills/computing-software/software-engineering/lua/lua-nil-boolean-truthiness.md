---
id: computing-software.software-engineering.lua.lua-nil-boolean-truthiness
name: lua-nil-boolean-truthiness
category: computing-software
field: software-engineering
product: lua
tags: [lua, lua-types-values, nil-boolean-truthiness]
level: intro
status: docs-checked
description: "Understand that only nil and false are falsy, and avoid 0 and empty string mistakes."
sources:
  - https://www.lua.org/manual/5.4/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# nil, false and truthiness
- Types: nil, boolean, number, string, function, userdata, thread, table; `type(x)` returns the name.
- Only `nil` and `false` are false; `0` and `""` are true.
- `x = x or default` breaks when `x` can legitimately be `false`; use `if x == nil then x = default end`.
- `a and b or c` fails when `b` is false or nil.
Verify: `print(0 and "yes")` prints `yes`.

## Checked
2026-11-02. Confirmed in Lua 5.4 Reference Manual (lua.org/manual/5.4/manual.html) section 3.3.4 (only nil and false test false; 0 and the empty string test true) and 6.1 (type). Removed: the 'assigning nil removes it' bullet.
Method: documentation only; no commands were run.
