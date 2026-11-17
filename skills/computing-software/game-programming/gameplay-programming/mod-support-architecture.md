---
id: computing-software.game-programming.gameplay-programming.mod-support-architecture
name: mod-support-architecture
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, modding-support, mods, data-driven, game-programming]
level: practitioner
status: draft
description: "Add mod support: data overrides with load order, a sandboxed scripting API, asset mounting, version checks and Steam Workshop distribution."
sources: ["https://partner.steamgames.com/doc/features/workshop", "https://www.lua.org/manual/5.4/manual.html#6"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mod support

**Goal:** let players change content without shipping your source, without crashing or compromising
their machines.

## Layers of moddability
1. **Data overrides:** mods ship files that override or patch base data (json/yaml tables, assets).
   Use a virtual file system where each mod is a mount with a priority; later mounts win.
2. **Patching instead of replacing:** support "merge" operations on tables (add an item to a loot
   table) so two mods touching the same file can coexist.
3. **Scripting:** expose a curated API to Lua or another embedded language, never raw engine pointers.
4. **Native plugins:** DLLs give full power and full risk; only if the community demands it.

## Load order and manifest
```json
{ "id": "better_swords", "version": "1.2.0", "game_version": ">=1.4",
  "depends": ["core_lib>=2.0"], "load_after": ["ui_overhaul"] }
```
Topologically sort by dependencies, detect cycles, refuse incompatible game versions with a clear
message, and record the active mod list in save files.

## Sandboxing scripts
- Load only safe Lua libraries (no `io`, `os.execute`, `package.loadlib`, `debug`); build the
  environment table explicitly.
- Instruction-count hooks (`lua_sethook` with `LUA_MASKCOUNT`) to kill runaway scripts.
- Mods cannot write outside a per-mod data directory.

## Distribution
Steam Workshop: `ISteamUGC` creates and updates items, subscribed items download to a path given by
`GetItemInstallInfo`; mount from there at startup.

## Verify
- Ship your own content as a "mod" through the same pipeline; if base content loads that way, the
  API is real.
- Load two conflicting mods and confirm the conflict report names both.
