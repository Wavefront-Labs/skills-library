---
id: computing-software.software-engineering.lua.lua-error-levels-traceback
name: lua-error-levels-traceback
category: computing-software
field: software-engineering
product: lua
tags: [lua, error-levels-traceback]
level: practitioner
status: docs-checked
description: "Raise errors with correct position info using error(msg, level), assert messages, and xpcall with debug.traceback."
sources:
  - https://www.lua.org/manual/5.4/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# error, levels and tracebacks
- If the message is a string, `error` adds position information at its start: level 1 (the default) is where `error` was called, level 2 is where the function that called `error` was called, and level 0 adds nothing.
- `assert(v, msg)` raises an error with `msg` as the error object (default "assertion failed!") if v is nil or false; otherwise it returns all its arguments.
- `xpcall(f, debug.traceback)` captures a stack at the error point; the handler runs before unwinding.
Verify: the traceback lists the erroring function and its callers.

## Checked
2026-11-02. Confirmed in Lua 5.4 Reference Manual (lua.org/manual/5.4/manual.html) section 6.1 (error, assert, xpcall) and 2.3 (message handler is called before the stack unwinds). Removed: the `file:line:` format and 'not position-annotated' wording.
Method: documentation only; no commands were run.
