---
id: computing-software.software-engineering.lua.lua-lpeg-parsing
name: lua-lpeg-parsing
category: computing-software
field: software-engineering
product: lua
tags: [lua, lua-lpeg, lpeg-parsing]
level: advanced
status: draft
description: "Write parsers with LPeg, using pattern combinators, captures and grammars instead of Lua patterns."
sources: ["https://www.lua.org/manual/5.4/", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# LPeg patterns, captures and grammars
- `local lpeg = require("lpeg"); local P, R, S, C, Ct = lpeg.P, lpeg.R, lpeg.S, lpeg.C, lpeg.Ct`.
- Operators: `*` sequence, `+` ordered choice, `^n` repetition, `-p` not-predicate, `#p` and-predicate; PEG choice is ordered and does not backtrack into a succeeded alternative.
- Captures: `C(p)` string, `Ct(p)` table, `Cg(p, name)` group, `Cf` fold, `/` function or table replacement.
- Grammars: `P{ "expr"; expr = ..., term = V("term") }`; rule `V"name"` references allow recursion.
- `re` module offers a regex-like syntax; match returns the end position or captures, `nil` on failure (check that the match consumed all input with `* -1`).
Verify: test failing and partial inputs.
