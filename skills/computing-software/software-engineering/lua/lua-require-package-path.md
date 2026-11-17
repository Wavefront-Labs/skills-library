---
id: computing-software.software-engineering.lua.lua-require-package-path
name: lua-require-package-path
category: computing-software
field: software-engineering
product: lua
tags: [lua, lua-modules, require-package-path]
level: practitioner
status: docs-checked
description: "Write modules that return a table, and understand package.path, package.loaded and cyclic dependencies."
sources:
  - https://www.lua.org/manual/5.4/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# require, package.path and module patterns
- A module file returns a table: `local M = {}; function M.f() end; return M`. `require(name)` first checks `package.loaded[name]`, then `package.preload`, then the Lua path `package.path`, then the C path `package.cpath`, then an all-in-one loader.
- `package.path` and `package.cpath` are `;`-separated templates where `?` is replaced by the module name (dots in the name become the directory separator); they are initialised from `LUA_PATH_5_4`/`LUA_PATH` and `LUA_CPATH_5_4`/`LUA_CPATH`, and `;;` in the variable means the default path.
- If the loader returns a non-nil value it is stored in `package.loaded[name]`; if it returns nothing and stores nothing, `true` is stored. `require` returns that value plus the loader data (for files, the file path), or only the value if the module was already loaded. Setting `package.loaded.name = nil` makes the next `require` load it again.
- `package.searchpath(name, path)` returns the file found or fail plus the files tried.
- For a script directory, prepend a template: `package.path = "./?.lua;" .. package.path`.
Verify: `print(package.searchpath("a.b", package.path))`.

## Checked
2026-11-02. Confirmed in the Lua 5.4 reference manual: require, package.path, package.cpath, package.loaded, package.preload, package.searchers, package.searchpath, package.config. Removed: the cyclic-require claim, the `module()` removal note (5.2 history), and the advice to derive the path from `arg[0]` (a convention, not in the manual).
Method: documentation only; no commands were run.
