---
id: computing-software.software-engineering.lua.lua-io-library-files
name: lua-io-library-files
category: computing-software
field: software-engineering
product: lua
tags: [lua, lua-io, io-library-files]
level: practitioner
status: docs-checked
description: "Read and write files with io.open, read formats, line iterators and error returns."
sources:
  - https://www.lua.org/manual/5.4/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# io.open, read formats and file handles
- `local f, err = io.open(path, "rb")`: modes `r`, `w`, `a`, `r+`, `w+`, `a+`, optionally with `b`, which some systems need for binary mode. Check `f` for nil.
- `f:read` formats: `"a"` whole rest of file (empty string at EOF), `"l"` next line without end of line (default), `"L"` keeps the end of line, `"n"` a numeral, or a number of bytes. `"l"` and `"L"` are for text files.
- `for line in io.lines(path) do` closes the file when iteration ends, even on error or break; `f:lines()` does not close the file.
- `f:seek("end")` returns the file size; `f:seek()` returns the current position; `f:close()` closes explicitly (collection closes eventually but at an unpredictable time).
- `io.write` adds no newline; `f:setvbuf("no" | "full" | "line")`; `io.stderr:write` for errors.
- File handles have `__close`, so `local f <close> = io.open(path)` works (5.4); `io.open` returns fail plus a message on failure.
Verify: read a file with CRLF line endings on both platforms.

## Checked
2026-11-02. Confirmed in the Lua 5.4 reference manual: io.open modes, file:read formats, io.lines, file:lines, file:seek, file:close, file:setvbuf, io.write, section 3.3.8 and the file metatable (__close). Removed: the claim that mode `b` 'matters on Windows' (the manual says only 'some systems'), and the 5.3 version note on `*`-less formats.
Method: documentation only; no commands were run.
