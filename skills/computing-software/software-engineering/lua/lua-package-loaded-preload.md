---
id: computing-software.software-engineering.lua.lua-package-loaded-preload
name: lua-package-loaded-preload
category: computing-software
field: software-engineering
product: lua
tags: [lua, package-loaded-preload]
level: advanced
status: docs-checked
description: "Control module loading: package.loaded caching, package.preload for in-memory modules, and custom package.searchers."
sources:
  - https://www.lua.org/manual/5.4/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Module machinery
- `require(name)` checks `package.loaded[name]`, then each of `package.searchers` (preload, Lua file via `package.path`, C library via `package.cpath`, all-in-one).
- Preload: `package.preload["mod"] = function(name, extra) return {} end` for embedded or test stubs.
- Set `package.loaded["mod"]=nil` to reload; `require` also returns a second value, the loader data (file path).
- Add a searcher to load from an archive or network.
Verify: reload after editing a file by clearing `package.loaded`.

## Checked
2026-11-02. Confirmed in Lua 5.4 Reference Manual (lua.org/manual/5.4/manual.html) section 6.3 (require, package.loaded, package.preload, package.searchers; the loader receives the module name and loader data, and require returns the loader data as a second result). Nothing removed.
Method: documentation only; no commands were run.
