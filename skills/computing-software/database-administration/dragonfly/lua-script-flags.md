---
id: computing-software.database-administration.dragonfly.lua-script-flags
name: lua-script-flags
category: computing-software
field: database-administration
product: dragonfly
tags: [lua, script-flags, allow-undeclared-keys, default-lua-flags, dragonfly]
level: advanced
status: docs-checked
description: "Set Dragonfly Lua script flags such as allow-undeclared-keys via a script header, --default_lua_flags or SCRIPT FLAGS, and know the cost."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/scripting.md
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/flags.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Dragonfly uses Lua version 5.4. By default no script flags are set, and accessing an undeclared key fails with `script tried accessing undeclared key`.

Script flags (from the `--default_lua_flags` reference): `allow-undeclared-keys` allows accessing undeclared keys, `disable-atomicity` allows running scripts non-atomically, `legacy-float` returns floats as integers. Multiple values are separated by a space.

Three ways to set them:

1. In the script source, first line: `--!df flags=allow-undeclared-keys`
2. Default flags applied to all scripts, as an argument to Dragonfly: `./dragonfly --default_lua_flags=allow-undeclared-keys`
3. With the command, by script SHA: `SCRIPT FLAGS <sha> allow-undeclared-keys`. It can be called even before the script is loaded, which makes it possible to patch scripts used by frameworks or side applications: find the SHAs with `SCRIPT LIST`, then call `SCRIPT FLAGS` for each required script before starting the application.

Cost: `allow-undeclared-keys` is disabled by default because unpredictability, atomicity and multithreading do not mix well. If enabled, Dragonfly has to stop all other operations while the script is running.

Sandbox notes: `load()` is restricted to text mode only; the built-in `rawset`, `setmetatable` and `getmetatable` are replaced with protected versions that refuse to modify or read the metatable of the global environment `_G` (they can still be reassigned or shadowed inside a script); `dragonfly.randstr()` validates its size argument and rejects values over the allowed limits.

Related flags: `interpreter_per_thread` (default 10) is the number of Lua interpreters per thread; `lua_auto_async` (default false), if enabled, replaces call/pcall with discarded values by acall/apcall.

## Checked

2026-11-04: confirmed against the Scripting with Lua page and the flags page (`--default_lua_flags`, `--interpreter_per_thread`, `--lua_auto_async`). Corrected the description of `lua_auto_async` (it does not "batch commands"), replaced "per proactor thread" with the page's "per thread", and removed the unstated advice to prefer declaring keys.
Method: documentation only; no commands were run.
