---
id: computing-software.software-engineering.lua.lua-embed-c-api
name: lua-embed-c-api
category: computing-software
field: software-engineering
product: lua
tags: [lua, lua-c-api, embed-c-api]
level: advanced
status: docs-checked
description: "Embed Lua in C and write C modules following stack discipline with luaL_ helpers."
sources:
  - https://www.lua.org/manual/5.4/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# lua_State, stack discipline and registering C functions
- `lua_State *L = luaL_newstate(); luaL_openlibs(L); luaL_dofile(L, "x.lua"); lua_close(L);`.
- The stack is the interface between C and Lua: `lua_pushnumber`, `lua_getglobal`, `lua_call`, `lua_pcall` (protected: returns an error status instead of long-jumping), `lua_tostring`, `lua_gettop`.
- C functions have the signature of `lua_CFunction`, `int f(lua_State *L)`, and return the number of results. `luaL_newlib` creates a library table from an array of functions. `luaL_error` raises an error; internally Lua uses C `longjmp` for errors.
- Userdata with metatables for objects: `lua_newuserdatauv`, `luaL_newmetatable`, `luaL_checkudata`, and `__gc` for cleanup.
- `luaL_ref(L, t)` creates a reference in table `t` for the value on top of the stack (and pops it), so a C library can hold a Lua value.
Verify: compare `lua_gettop` before and after a call to check the stack is balanced.

## Checked
2026-11-02. Confirmed in the Lua 5.4 reference manual: luaL_newstate, luaL_openlibs, luaL_dofile, lua_close, lua_pushnumber, lua_getglobal, lua_call, lua_pcall, lua_tostring, lua_gettop, lua_CFunction, luaL_newlib, luaL_error, lua_newuserdatauv, luaL_newmetatable, luaL_checkudata, luaL_ref, section 4.4 (longjmp). Removed: Valgrind/ASAN advice and the unanchored-value GC claim beyond what luaL_ref documents.
Method: documentation only; no commands were run.
