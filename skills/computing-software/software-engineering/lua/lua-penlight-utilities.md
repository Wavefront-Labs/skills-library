---
id: computing-software.software-engineering.lua.lua-penlight-utilities
name: lua-penlight-utilities
category: computing-software
field: software-engineering
product: lua
tags: [lua, lua-penlight, penlight-utilities]
level: practitioner
status: docs-checked
description: "Use Penlight for collections, string utilities, argument parsing and pretty-printing instead of rewriting them."
sources:
  - https://lunarmodules.github.io/Penlight/
  - https://lunarmodules.github.io/Penlight/libraries/pl.stringx.html
  - https://lunarmodules.github.io/Penlight/libraries/pl.tablex.html
  - https://lunarmodules.github.io/Penlight/libraries/pl.pretty.html
  - https://lunarmodules.github.io/Penlight/classes/pl.List.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Penlight stdlib extensions: List, Map, stringx, pretty and class
- `local List = require("pl.List"); local l = List{1,2,3}:map(function(x) return x * 2 end)` (`List:map(fun, ...)`, a Python-style list class); `pl.Map`, `pl.Set`, `pl.OrderedMap` are sibling classes.
- `pl.tablex` has `copy(t)`, `deepcopy(t)`, `deepcompare(t1, t2[, ignore_mt[, eps]])`, `keys(t)`, `sort(t, f)` and `map(fun, t, ...)`. On Lua 5.1 the length, pairs and ipairs metamethod support does not work, since those metamethods only exist in Lua 5.2 and newer.
- `pl.stringx` is a Python-style extended string library: `split(s[, re[, n]])`, `strip(s[, chrs])`, `startswith(s, prefix)`; `pl.pretty.write(tbl[, space[, not_clever]])` pretty-prints tables; `pl.class` is a reusable framework for creating classes; `pl.lapp` parses command-line flags from a human-readable spec and `pl.app` holds application support functions.
- For lightweight needs prefer small local helpers to avoid a dependency.
Verify: `pretty.write` output matches expectations on nested tables.

## Checked
2026-11-08. Confirmed in the Penlight 1.15.0 LDoc pages: index, pl.stringx, pl.tablex, pl.pretty and pl.List (function signatures read via targeted searches; pl.class, pl.lapp and pl.app only from the index descriptions). Removed: the claim that Penlight runs on Lua 5.1 to 5.4 and LuaJIT (pl.compat documents 5.1/5.2/5.3 only).
Method: documentation only; no commands were run.
