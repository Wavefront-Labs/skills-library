---
id: computing-software.software-engineering.lua.lua-io-seek-buffering-popen
name: lua-io-seek-buffering-popen
category: computing-software
field: software-engineering
product: lua
tags: [lua, io-seek-buffering-popen]
level: advanced
status: docs-checked
description: "Control Lua file position and flushing with seek and setvbuf, and run subprocess pipes with io.popen."
sources:
  - https://www.lua.org/manual/5.4/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# seek, setvbuf, popen
- `f:seek("set"|"cur"|"end", offset)` returns the position; `f:seek("end")` gives size.
- `f:setvbuf("no"|"full"|"line")`, `f:flush()`; close files promptly with `f:close()` or `<close>`.
- `io.popen(cmd, "r")` returns a file you read the program's output from (mode "w" writes to it); it is system dependent and not available on all platforms. `f:close()` on it returns the same values as `os.execute`: a success flag, then "exit" or "signal", then the exit status or signal number.
Verify: popen `echo hi` and read "hi".

## Checked
2026-11-02. Confirmed in Lua 5.4 Reference Manual (lua.org/manual/5.4/manual.html) section 6.8 (file:seek, file:setvbuf, io.popen, file:close) and 6.9 (os.execute). Removed: the '5.2+' version tag and the shell injection remark (not on the page).
Method: documentation only; no commands were run.
