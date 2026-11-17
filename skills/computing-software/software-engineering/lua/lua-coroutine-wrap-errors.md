---
id: computing-software.software-engineering.lua.lua-coroutine-wrap-errors
name: lua-coroutine-wrap-errors
category: computing-software
field: software-engineering
product: lua
tags: [lua, coroutine-wrap-errors]
level: advanced
status: docs-checked
description: "Understand that resume returns false plus the error, wrap propagates the error, and a dead coroutine cannot resume."
sources:
  - https://www.lua.org/manual/5.4/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Coroutine errors
- `coroutine.resume(co)` catches errors: returns `false, err`; the coroutine is then dead.
- `coroutine.wrap(f)` returns a function that, on error, closes the coroutine and propagates the error.
- A coroutine that finished its body or stopped with an error has status `dead` (`coroutine.status`).
Verify: after an error, `coroutine.status(co)` is `dead`.

## Checked
2026-11-02. Confirmed in Lua 5.4 Reference Manual (lua.org/manual/5.4/manual.html) section 6.2 (coroutine.resume, wrap, status). Removed: the 5.4 position-prefix claim, the exact 'cannot resume dead coroutine' message and the 5.1 yield-across-pcall note (none on the page).
Method: documentation only; no commands were run.
