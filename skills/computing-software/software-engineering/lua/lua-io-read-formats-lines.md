---
id: computing-software.software-engineering.lua.lua-io-read-formats-lines
name: lua-io-read-formats-lines
category: computing-software
field: software-engineering
product: lua
tags: [lua, io-read-formats-lines]
level: practitioner
status: docs-checked
description: "Read files in Lua with the l, L, n and a read formats and byte counts, and io.lines with automatic close."
sources:
  - https://www.lua.org/manual/5.4/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reading
- `f:read("l")` line without newline (default), `"L"` with it, `"n"` a number, `"a"` the rest, a number reads up to that many bytes; `read(0)` reads nothing and returns an empty string, or `fail` at end of file.
- `for line in io.lines(path) do ... end` closes the file when the loop ends.
- A `b` at the end of the mode string (`"rb"`) opens the file in binary mode, which some systems need; use `"l"` and `"L"` only on text files.
- Check the `io.open` result: `local f, err = io.open(p)`.
Verify: on an empty file `read("a")` is "" and `read("l")` returns `fail` (currently nil).

## Checked
2026-11-02. Confirmed in Lua 5.4 Reference Manual (lua.org/manual/5.4/manual.html) section 6.8 (file:read formats, io.lines, io.open modes). Fixed: read(0) result and the Windows-specific text mode remark replaced by the manual's wording.
Method: documentation only; no commands were run.
