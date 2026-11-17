---
id: computing-software.game-programming.gameplay-programming.embedding-lua-for-gameplay
name: embedding-lua-for-gameplay
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, lua-scripting, lua, scripting-bindings, game-programming]
level: practitioner
status: draft
description: "Embed Lua for gameplay scripting: C API stack discipline, binding with sol2, coroutines for scripted sequences, error handling and hot reload."
sources: ["https://www.lua.org/manual/5.4/manual.html", "https://sol2.readthedocs.io/en/latest/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Embedding Lua for gameplay scripting

**Goal:** designers write quests, AI and abilities in Lua; the engine stays C++.

## Raw C API essentials
```c
lua_State* L = luaL_newstate();
luaL_openlibs(L);                         // or open only the safe subset
if (luaL_dofile(L, "scripts/door.lua") != LUA_OK) {
    log_error("%s", lua_tostring(L, -1)); lua_pop(L, 1);
}
lua_getglobal(L, "on_open");              // push function
lua_pushinteger(L, entity_id);            // push arg
if (lua_pcall(L, 1, 0, 0) != LUA_OK) { log_error("%s", lua_tostring(L, -1)); lua_pop(L, 1); }
```
- Every call balances the stack; check `lua_gettop` in debug builds after each binding.
- Always `lua_pcall`, never `lua_call`, at the engine boundary; an error otherwise longjmps through
  C++ frames and skips destructors.

## Binding with sol2 (C++17)
```cpp
sol::state lua; lua.open_libraries(sol::lib::base, sol::lib::math, sol::lib::coroutine);
lua.new_usertype<Entity>("Entity", "health", &Entity::health, "damage", &Entity::damage);
lua["spawn"] = [&](std::string type) { return world.spawn(type); };
sol::protected_function f = lua["on_open"]; auto r = f(id); if (!r.valid()) { sol::error e = r; }
```
Expose entity *handles* (generational ids), not raw pointers; a destroyed entity then fails
gracefully instead of crashing.

## Coroutines for sequences
```lua
function cutscene()
  move_to(npc, door); wait(1.5); say(npc, "Locked."); wait_for_event("key_found")
end
```
Run each script sequence as a coroutine; `wait` yields with a wake condition, the engine resumes it
each frame when satisfied. This replaces callback chains.

## Hot reload and performance
- Reload by re-running the file into the same state; keep persistent data in tables keyed by
  entity so functions can be swapped.
- Avoid per-frame Lua calls for thousands of entities; batch or call only on events. Consider
  LuaJIT (5.1 semantics) when profiling shows interpreter time.

## Verify
- Fuzz scripts that error at every line: engine logs and continues.
