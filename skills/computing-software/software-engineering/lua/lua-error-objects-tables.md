---
id: computing-software.software-engineering.lua.lua-error-objects-tables
name: lua-error-objects-tables
category: computing-software
field: software-engineering
product: lua
tags: [lua, error-objects-tables]
level: advanced
status: docs-checked
description: "Throw tables as errors in Lua, with code and message fields, plus __tostring so uncaught errors print cleanly."
sources:
  - https://www.lua.org/manual/5.4/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Error objects
- `error(setmetatable({code=404, msg="not found"}, E))` where `E.__tostring` formats it for the standalone interpreter.
- `local ok, e = pcall(f)`; test `type(e)=="table" and e.code`. A non-string error object is passed through as is; for string messages, level 0 avoids adding position information.
- Memory-allocation errors (LUA_ERRMEM) do not call the message handler; an error while running the message handler gives status LUA_ERRERR.
Verify: pcall returns false and the same table instance.

## Checked
2026-11-02. Confirmed in Lua 5.4 Reference Manual (lua.org/manual/5.4/manual.html) section 2.3 (error object may be any value; message handler), 6.1 (error, pcall), 4.4.1 (status codes) and the lua standalone section (__tostring used for unprotected error objects). Removed: the 'not enough memory' string, which is not on the page.
Method: documentation only; no commands were run.
