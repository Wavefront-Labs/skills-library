---
id: computing-software.software-engineering.lua.lua-debug-library-traceback
name: lua-debug-library-traceback
category: computing-software
field: software-engineering
product: lua
tags: [lua, lua-debug, debug-library-traceback]
level: advanced
status: docs-checked
description: "Debug with debug.traceback, debug.getinfo, hooks and external debuggers such as ZeroBrane Studio."
sources:
  - https://www.lua.org/manual/5.4/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# debug.traceback, debug.getinfo and hooks
- `debug.traceback([thread,] [message [, level]])` returns a traceback string (message prepended; level defaults to 1); if `message` is neither a string nor nil it is returned unchanged. It is usable as an `xpcall` message handler.
- `debug.getinfo(2, "Sl")` returns `short_src` and `currentline` of the caller (level 0 is `getinfo` itself, level 1 the function that called it); option `"n"` gives a name, `"u"` fills `nups`, `nparams` and `isvararg`.
- `debug.sethook(f, mask [, count])`: mask characters `c` (call), `r` (return), `l` (line); with a nonzero count the hook also runs every count instructions. Called with no arguments it turns the hook off. Inside a hook, `getinfo` level 2 describes the running function.
- `debug.getlocal(level, n)` inspects locals, parameters and temporaries; `debug.setmetatable(value, t)` sets a metatable on any type.
Verify: an error raised in a nested call shows the full traceback.

## Checked
2026-11-02. Confirmed in the Lua 5.4 reference manual: debug.traceback, debug.getinfo and lua_Debug field options, debug.sethook, debug.getlocal, debug.setmetatable, xpcall. Removed: the list of external debuggers (ZeroBrane Studio, VS Code adapters, mobdebug) and `inspect.lua`, which the manual does not document.
Method: documentation only; no commands were run.
