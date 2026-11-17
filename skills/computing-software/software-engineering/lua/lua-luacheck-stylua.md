---
id: computing-software.software-engineering.lua.lua-luacheck-stylua
name: lua-luacheck-stylua
category: computing-software
field: software-engineering
product: lua
tags: [lua, lua-linting, luacheck-stylua]
level: practitioner
status: docs-checked
description: "Lint with luacheck, format with StyLua and add type annotations with LuaLS."
sources:
  - https://luacheck.readthedocs.io/en/stable/warnings.html
  - https://luacheck.readthedocs.io/en/stable/config.html
  - https://luacheck.readthedocs.io/en/stable/cli.html
  - https://raw.githubusercontent.com/JohnnyMorganz/StyLua/main/README.md
  - https://luals.github.io/wiki/annotations/
  - https://raw.githubusercontent.com/LuaLS/lua-language-server/master/doc/en-us/config.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Luacheck, StyLua and Lua Language Server
- `luacheck src/` reports warning codes: 211 unused local, 212 unused argument, 111/113 setting/accessing an undefined global, 421/431 shadowing. `--codes` shows them. Configure `.luacheckrc` (a Lua script found by walking up from the current directory): `std = "lua54"` (also `lua51`, `lua52`, `lua53`, `luajit`, `max`, `min`), `globals = {...}`, `read_globals`, `max_line_length`, and `files["**/spec/**/*_spec.lua"].std = "+busted"`.
- StyLua: `stylua src/` formats in place; `stylua --check` prints a diff and exits 1 if files need formatting (use in CI); `--output-format` is `standard`, `unified`, `json` or `summary`. Config is `stylua.toml` or `.stylua.toml` with `column_width` (default 120), `indent_type` (default `Tabs`), `indent_width` (4), `quote_style` (`AutoPreferDouble`), `call_parentheses`. The `syntax` option (`All`, `Lua51`..`Lua54`, `LuaJIT`, `Luau`) disambiguates dialects, or use `--syntax`. Skip code with `-- stylua: ignore` or `-- stylua: ignore start` / `-- stylua: ignore end`; `.styluaignore` works like `.gitignore`.
- LuaLS (lua-language-server) reads `.luarc.json` in the workspace (`runtime.version`, `diagnostics.globals`, `workspace.library`) and uses `---@param`, `---@return` and `---@class` annotations.
Verify: the CI job fails on a new warning.

## Checked
2026-11-08. Confirmed in luacheck warnings, config and CLI pages, the StyLua README and the LuaLS annotation page and config.md (config read via targeted searches for the named keys). Removed: unverified style-guide advice on indent width and naming, and the note that StyLua dialect follows only cargo features (README says release binaries include all syntaxes).
Method: documentation only; no commands were run.
