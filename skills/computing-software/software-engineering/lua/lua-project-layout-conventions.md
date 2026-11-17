---
id: computing-software.software-engineering.lua.lua-project-layout-conventions
name: lua-project-layout-conventions
category: computing-software
field: software-engineering
product: lua
tags: [lua, lua-style, project-layout-conventions]
level: practitioner
status: docs-checked
description: "Lay out a Lua library or application with src/, spec/, rockspec and clear module names."
sources:
  - https://www.lua.org/manual/5.4/manual.html
  - https://lunarmodules.github.io/busted/
  - https://luacheck.readthedocs.io/en/stable/config.html
  - https://raw.githubusercontent.com/JohnnyMorganz/StyLua/main/README.md
  - https://raw.githubusercontent.com/luarocks/luarocks/main/docs/luarocks_make.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Project layout, rockspec and README conventions
- Library layout: `src/mylib/init.lua`, `src/mylib/util.lua`, `spec/`, a rockspec such as `mylib-dev-1.rockspec`, `.luacheckrc`, `.busted`. `require("mylib")` finds `mylib/init.lua` only when a `package.path` template like `?/init.lua` is present: each `?` is replaced by the module name (dots become directory separators), as in the manual's `package.searchpath` example.
- `.busted` in the project root holds busted configuration, `.luacheckrc` holds luacheck configuration, and `stylua.toml` or `.stylua.toml` holds StyLua configuration (StyLua also falls back to `.editorconfig`).
- Keep one module per file, return a table, no globals, and expose a version string such as `M._VERSION` (project convention, not a language rule).
- Applications: a launcher script sets `package.path` relative to `arg[0]` (the script name, per the stand-alone interpreter), then requires the main module.
- Document public functions with LuaLS annotations or LDoc comments.
Verify: `luarocks make` (builds from the current directory) and `busted` pass from a clean checkout.

## Checked
2026-11-08. Confirmed in the Lua 5.4 manual (`package.searchpath`, `arg`), busted docs (`.busted` file), luacheck config page (`.luacheckrc`), StyLua README (`stylua.toml`, `.stylua.toml`, `.editorconfig` fallback) and LuaRocks `make` page; manual and README pages read via targeted searches. Removed: the `scm` rockspec naming and the `ldoc` command (its docs were not reachable; LDoc comments are kept as an unverified tool mention).
Method: documentation only; no commands were run.
