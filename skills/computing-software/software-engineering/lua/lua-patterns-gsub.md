---
id: computing-software.software-engineering.lua.lua-patterns-gsub
name: lua-patterns-gsub
category: computing-software
field: software-engineering
product: lua
tags: [lua, lua-strings, patterns-gsub]
level: practitioner
status: docs-checked
description: "Write Lua patterns (not regex) with character classes, captures, anchors and gsub replacement functions."
sources: ["https://www.lua.org/manual/5.4/manual.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lua patterns, find, match and gsub
- `%f[set]` is the frontier pattern; `%bxy` matches balanced pairs, so `%b()` matches balanced parentheses; `-` matches zero or more characters, shortest sequence.
- The pattern items in the manual include no alternation operator.
- In a gsub replacement string `%1`-`%9` insert captures, `%0` the whole match, and `%%` a literal `%`.
Verify: assert match results on edge cases like empty strings.

## Checked

Date: 2026-11-02. Confirmed on Lua 5.4 manual section 6.4.1 (frontier, %b, '-', no alternation) and string.gsub (replacement `%` handling). Removed as not confirmed: class letters, escape character list, `{n,m}` remark, gmatch/match examples, table and function replacement detail.

Method: documentation only; no commands were run.
