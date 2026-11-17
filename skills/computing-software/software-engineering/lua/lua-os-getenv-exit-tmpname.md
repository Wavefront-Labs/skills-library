---
id: computing-software.software-engineering.lua.lua-os-getenv-exit-tmpname
name: lua-os-getenv-exit-tmpname
category: computing-software
field: software-engineering
product: lua
tags: [lua, os-getenv-exit-tmpname]
level: practitioner
status: docs-checked
description: "Use Lua OS functions: getenv, exit(code, close), rename/remove return values, and the unsafe os.tmpname."
sources:
  - https://www.lua.org/manual/5.4/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# os functions
- `os.getenv("HOME")` returns the variable's value, or `fail` (currently equal to nil) if it is not defined.
- `os.exit(code, true)` closes the Lua state before exiting; it calls the C function `exit`. `code` true or false gives EXIT_SUCCESS or EXIT_FAILURE, a number is used as the status, and the default is true.
- `os.remove`/`os.rename` return `fail` plus an error message and error code on failure, and true on success.
- `os.tmpname()` returns a file name; you must open the file and remove it yourself (on POSIX it also creates the file). Prefer `io.tmpfile()`, which is removed automatically when the program ends.
Verify: `os.remove("missing")` returns `fail` plus a message.

## Checked
2026-11-02. Confirmed in Lua 5.4 Reference Manual (lua.org/manual/5.4/manual.html) section 6.9 (os.getenv, os.exit, os.remove, os.rename, os.tmpname), section 6.8 (io.tmpfile) and the definition of fail in section 6. Fixed: os.tmpname is not 'a name only' on POSIX, where it also creates the file; os.exit 'runs finalizers' replaced by the manual's wording.
Method: documentation only; no commands were run.
