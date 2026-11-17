---
id: computing-software.software-engineering.lua.lua-lfs-paths
name: lua-lfs-paths
category: computing-software
field: software-engineering
product: lua
tags: [lua, lua-filesystem, lfs-paths]
level: practitioner
status: docs-checked
description: "List directories, read attributes and join paths with LuaFileSystem and penlight."
sources:
  - https://lunarmodules.github.io/luafilesystem/manual.html
  - https://www.lua.org/manual/5.4/manual.html
  - https://lunarmodules.github.io/Penlight/libraries/pl.path.html
  - https://lunarmodules.github.io/Penlight/libraries/pl.dir.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LuaFileSystem directory listing, attributes and path handling
- `local lfs = require("lfs")` (install with `luarocks install luafilesystem`); `for name in lfs.dir(path) do` iterates entry names and raises an error if `path` is not a directory; `dir_obj:close()` closes early.
- `lfs.attributes(p, "mode")` returns a string such as `file`, `directory`, `link`, `socket`, `named pipe`, `char device`, `block device` or `other`; other attributes include `size`, `modification` and `permissions`. It follows symlinks; `lfs.symlinkattributes` describes the link itself (on Windows it is identical to `attributes`). On error it returns `nil`, a message and an error code.
- `lfs.mkdir`, `lfs.rmdir`, `lfs.currentdir()`, `lfs.chdir(path)` return `true` on success or `nil` plus an error message.
- The path separator is the first line of `package.config`: `package.config:sub(1, 1)`.
- penlight wraps common operations: `pl.path` `join(p1, p2, ...)`, `pl.dir` `getfiles([dirname='.'[, mask]])` and `makepath(p)`.
- Check that files exist by trying `io.open` and handling the error rather than a separate check (race conditions).
Verify: list a directory with files and subdirectories and check the modes.

## Checked
2026-11-08. Confirmed in the LuaFileSystem manual (read in full), the Lua 5.4 manual `package.config` entry, and the Penlight pl.path and pl.dir pages (signatures via targeted searches). Removed: the claim that `lfs.dir` yields `.` and `..` and that Windows accepts `/` in most APIs (neither stated in these pages).
Method: documentation only; no commands were run.
