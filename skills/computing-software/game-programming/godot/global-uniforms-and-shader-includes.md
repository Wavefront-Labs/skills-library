---
id: computing-software.game-programming.godot.global-uniforms-and-shader-includes
name: global-uniforms-and-shader-includes
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, global-shader-uniforms, shader-includes, instance-uniforms, shaders, game-programming]
level: practitioner
status: docs-checked
description: "Share data and code across Godot shaders with global uniforms (project settings and RenderingServer), per-instance uniforms, and .gdshaderinc include files."
sources: ["https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shading_language.html", "https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shader_preprocessor.html", "https://docs.godotengine.org/en/stable/classes/class_renderingserver.html#class-renderingserver-method-global-shader-parameter-set"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Global uniforms and shader includes

**Goal:** one wind direction, player position or time-of-day value feeds every shader, and common
functions live in one file.

## Global uniforms
Project Settings > **Shader Globals**: add name, type, default (`wind_dir` vec2, `player_pos` vec3,
`snow_amount` float). Use in any shader:
```glsl
global uniform vec3 player_pos;
global uniform float snow_amount;
```
Update from script whenever the value changes (assignments need no CPU/GPU synchronisation):
```gdscript
RenderingServer.global_shader_parameter_set("player_pos", $Player.global_position)
```
Add or remove at runtime with `global_shader_parameter_add(name, type, default)` and
`global_shader_parameter_remove` (has a performance cost); do not read values back every frame with
`global_shader_parameter_get`. Ideal for grass bending around
the player, global wetness, fog of war textures (sampler2D globals).

## Per-instance uniforms
```glsl
instance uniform vec4 tint : source_color = vec4(1.0);
```
Set per GeometryInstance3D without duplicating the material:
`$Mesh.set_instance_shader_parameter("tint", Color.RED)` (also available on CanvasItem; per-instance uniforms
work in `canvas_item` and `spatial` shaders). Scalars and vectors only, practical maximum of 16 per shader.

## Includes
`.gdshaderinc` files contain shared code:
```glsl
// res://shaders/lib/noise.gdshaderinc
float hash21(vec2 p) { p = fract(p * vec2(123.34, 456.21)); p += dot(p, p + 45.32); return fract(p.x * p.y); }
```
```glsl
shader_type spatial;
#include "res://shaders/lib/noise.gdshaderinc"
```
The preprocessor also supports `#define`, `#ifdef`, `#if` for shader variants (`#define USE_SNOW`).

## Gotchas
- A global uniform must exist in Project Settings when the shader is compiled; a default written in the
  shader (`global uniform vec4 c = ...`) is ignored.
- Only `.gdshaderinc` resources can be included, and an include may include other includes. A `shader_type`
  line is technically allowed in an include but normally omitted; keep includes as function, macro and
  uniform libraries.

## Verify
- [ ] Changing one global updates all relevant materials; per-object tint does not create new materials.

## Checked

Checked 2026-10-25 against the Godot 4.7 documentation (godot-docs stable branch, last commit 2026-10-24; latest engine release 4.7.2). Confirmed: `global uniform` declaration, Project Settings > Shader Globals, `RenderingServer.global_shader_parameter_set/add/remove/get` and their costs; per-instance uniforms (`instance uniform`, `set_instance_shader_parameter`, 16 practical maximum, scalars and vectors only, both shader types); `#include "path"` of `.gdshaderinc` files, include chaining, `#define`, `#ifdef`, `#if` and `#undef`. Removed the unconfirmed "up to 16 per instance in 4.x", 3D-only, batching, recompile and sampler-hint claims; `shader_type` in includes is allowed rather than forbidden.

Method: documentation only; no commands were run.
