---
id: computing-software.software-engineering.lua.lua-luarocks-install-rockspec
name: lua-luarocks-install-rockspec
category: computing-software
field: software-engineering
product: lua
tags: [lua, lua-luarocks, luarocks-install-rockspec]
level: practitioner
status: docs-checked
description: "Install and publish libraries with LuaRocks, write rockspec files and use local trees."
sources:
  - https://raw.githubusercontent.com/luarocks/luarocks/main/docs/luarocks_install.md
  - https://raw.githubusercontent.com/luarocks/luarocks/main/docs/luarocks_path.md
  - https://raw.githubusercontent.com/luarocks/luarocks/main/docs/luarocks_make.md
  - https://raw.githubusercontent.com/luarocks/luarocks/main/docs/luarocks_upload.md
  - https://raw.githubusercontent.com/luarocks/luarocks/main/docs/luarocks_init.md
  - https://raw.githubusercontent.com/luarocks/luarocks/main/docs/luarocks_search.md
  - https://raw.githubusercontent.com/luarocks/luarocks/main/docs/rockspec_format.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Installing rocks, rockspecs and trees
- `luarocks install luasocket` (optionally a version; `--only-deps` installs just the dependencies, `--keep` keeps other versions). `luarocks search socket` queries the remote servers; `luarocks list` queries the rocks you have installed.
- `luarocks path` prints package paths formatted as a shell script that prepends to `LUA_PATH` and `LUA_CPATH`: `eval $(luarocks path)` on Unix; `--append` appends instead, `--bin` also adds script directories to `PATH`.
- A rockspec (`mylib-1.0-1.rockspec`) has mandatory `package`, `version` (with a revision suffix) and `source` (with `source.url`), plus `description`, `dependencies` (strings such as `"lfs >= 1.0, < 2.0"`, with the `~>` pessimistic operator) and `build = {type = "builtin", modules = {...}}`. Other `build.type` back-ends are `make`, `cmake`, `command` and `none`. Use `git+https://` rather than plain `https://` for a Git repository URL.
- `luarocks make` builds and installs the rock from the current directory (it ignores `source.url`); `--pack-binary-rock` produces a `.rock` instead of installing.
- `luarocks upload <rockspec>` publishes to the public repository and needs an API key (`--api-key`, issued on the LuaRocks site Settings page); `--dry-run` validates and checks for conflicts without uploading.
- `luarocks init` makes a local rocktree (`lua_modules`), `lua` and `luarocks` wrapper scripts, a rockspec and a `.gitignore`.
Verify: `lua -e 'require "lpeg"'` after install.

## Checked
2026-11-08. Confirmed in the LuaRocks docs on GitHub: the install, path, make, upload, init and search command pages and the rockspec format page (read in full). Removed: `--local`, `--lua-version` and `luarocks remove` (not on the pages read) and the C-module compiler remark.
Method: documentation only; no commands were run.
