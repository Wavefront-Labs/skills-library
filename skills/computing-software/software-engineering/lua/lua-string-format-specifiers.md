---
id: computing-software.software-engineering.lua.lua-string-format-specifiers
name: lua-string-format-specifiers
category: computing-software
field: software-engineering
product: lua
tags: [lua, string-format-specifiers]
level: practitioner
status: docs-checked
description: "Use string.format correctly: %d vs %s vs %q vs %g, width and precision, and the integer representation error."
sources:
  - https://www.lua.org/manual/5.4/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# string.format
- The format string follows C `sprintf`, except `F`, `n`, `*`, `h`, `L` and `l` are not supported and `q` is added. Width and precision are each limited to two digits.
- `a`, `A`, `e`, `E`, `f`, `g`, `G` expect a number; `c`, `d`, `i`, `o`, `u`, `x`, `X` expect an integer, so a float without an exact integer value is rejected by `%d`.
- `%s` converts a non-string argument as `tostring` does (so `__tostring` is honoured); with any modifier, the string must not contain embedded zeros.
- `%q` writes booleans, nil, numbers and strings as valid Lua constants (floats in hexadecimal; strings in double quotes with escapes, a newline written as backslash-newline). It does not accept modifiers (flags, width, precision).
- `%p` formats the pointer from `lua_topointer`.
- Use `%%` for a literal percent.
Verify: `string.format("%q", "a\nb")` yields a quoted string with a backslash-newline.

## Checked
2026-11-02. Confirmed in the Lua 5.4 reference manual: string.format (sprintf rules, unsupported specifiers, q, two-digit width and precision, integer vs number specifiers, s via tostring, p). Removed: the exact error text for `%d` with 3.5, the `%5.2s` truncation claim and the flag examples (`%-8s`, `%05.1f`, `%+d`), since the manual only refers to C sprintf for them.
Method: documentation only; no commands were run.
