---
id: computing-software.software-engineering.lua.lua-os-library-time-exec
name: lua-os-library-time-exec
category: computing-software
field: software-engineering
product: lua
tags: [lua, lua-os, os-library-time-exec]
level: practitioner
status: docs-checked
description: "Use os.time/os.date for dates, os.getenv, os.execute return values and portability limits."
sources:
  - https://www.lua.org/manual/5.4/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# os.time, os.date, os.getenv, os.execute and os.remove
- `os.time{year=2026, month=11, day=2, hour=12}` returns a time for that local date (year, month, day required; hour defaults to 12); out-of-range fields are normalised. `os.date("!%Y-%m-%d", t)` with a leading `!` formats in UTC; `os.date("*t", t)` returns a table with year, month, day, hour, min, sec, wday, yday, isdst; other formats follow C `strftime`.
- `os.clock()` is approximate CPU time used by the program; `os.difftime(t2, t1)` is seconds from t1 to t2.
- `os.execute(cmd)` passes the command to a shell and returns `true` or fail, then `"exit"` or `"signal"`, then the status or signal number; with no command it reports whether a shell is available. `io.popen(cmd):read("a")` captures output (system dependent); `close` on that handle returns the same values as `os.execute`.
- `os.remove` (a file, or an empty directory on POSIX), `os.rename`, `os.tmpname` (on POSIX it also creates the file), `os.exit(code, close)`, `os.getenv(name)` (fail if undefined).
Verify: test `os.execute("exit 3")` return values.

## Checked
2026-11-02. Confirmed in the Lua 5.4 reference manual: os.time, os.date, os.clock, os.difftime, os.execute, os.remove, os.rename, os.tmpname, os.exit, os.getenv, io.popen, file:close. Removed: the claim that the standard library has no directory listing and the LuaFileSystem recommendation, and the shell-quoting advice as a manual statement.
Method: documentation only; no commands were run.
