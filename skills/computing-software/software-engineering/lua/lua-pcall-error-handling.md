---
id: computing-software.software-engineering.lua.lua-pcall-error-handling
name: lua-pcall-error-handling
category: computing-software
field: software-engineering
product: lua
tags: [lua, lua-errors, pcall-error-handling]
level: practitioner
status: docs-checked
description: "Raise and catch errors with error(), pcall, xpcall tracebacks, and use table error objects."
sources:
  - https://www.lua.org/manual/5.4/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# error, pcall, xpcall and error objects
- `error(msg, level)`: level 1 (default) adds the position where `error` was called, level 2 points at where the function that called `error` was called, level 0 adds no position. Position is added only if the message is a string.
- `local ok, err = pcall(f, ...)` returns `true` plus results, or `false` plus the error object; the error object can be any value, including a table like `{code = 404}`. Errors caught by `pcall` do not call a message handler.
- `xpcall(f, msgh, ...)` sets a message handler (for example `debug.traceback`) and passes extra arguments to `f`.
- `assert(v, msg)` returns all its arguments when `v` is truthy; otherwise it raises `msg` as the error object (default "assertion failed!"), which need not be a string.
- Convention: return `nil, errmsg` for expected failures (like `io.open`) and `error` for bugs.
Verify: test that an error object keeps its fields through pcall.

## Checked
2026-11-02. Confirmed in the Lua 5.4 reference manual: error (levels), pcall, xpcall (msgh and extra arguments), assert, section 2.3 (any value as error object). Removed: the '5.2+' qualifier on xpcall extra arguments (the manual covers 5.4 only).
Method: documentation only; no commands were run.
