---
id: computing-software.software-engineering.lua.lua-love2d-game-loop
name: lua-love2d-game-loop
category: computing-software
field: software-engineering
product: lua
tags: [lua, lua-game-scripting, love2d-game-loop]
level: practitioner
status: draft
description: "Structure a LOVE (LÖVE) game with love.load, love.update and love.draw and manage assets and delta time."
sources: ["https://www.lua.org/manual/5.4/", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# LOVE callbacks and game loop structure
- `main.lua` defines `love.load()`, `love.update(dt)`, `love.draw()`; input via `love.keypressed(key)`, `love.mousepressed`.
- Use `dt` to scale movement so speed does not depend on frame rate; clamp large `dt` after pauses.
- Load assets once in `love.load` (`love.graphics.newImage`), never per frame.
- `conf.lua` sets window and modules via `love.conf(t)`; LÖVE uses LuaJIT.
- Package a game by zipping to a `.love` file.
Verify: run with a window resize and a slow frame and check movement.
