---
id: computing-software.game-programming.godot.shader-uniforms-and-parameters
name: shader-uniforms-and-parameters
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, godot-shaders, shader-parameters, uniforms, global-uniforms, instance-uniforms, game-programming]
level: intro
status: docs-checked
description: "Set Godot shader uniforms from GDScript: set_shader_parameter, hints, global uniforms, per-instance uniforms, and sharing vs duplicating ShaderMaterials."
sources: ["https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shading_language.html#uniforms", "https://docs.godotengine.org/en/stable/classes/class_shadermaterial.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Uniforms and setting shader parameters

**Goal:** drive shader effects (hit flash, dissolve, wind, time of day) from gameplay without
accidentally affecting every object sharing the material.

## Declare
```glsl
uniform float flash : hint_range(0.0, 1.0) = 0.0;
uniform vec4 tint : source_color = vec4(1.0);
uniform sampler2D mask : hint_default_black;
group_uniforms Wind;                       // inspector grouping
uniform float wind_strength = 0.2;
group_uniforms;
```
Hints: `hint_range(min, max, step)`, `source_color`, `hint_normal`, `hint_default_white/black/transparent`,
`hint_screen_texture`, `filter_*`, `repeat_*`, `hint_enum("A", "B")` (int dropdown; `"Slow:30"` assigns a value).

## Set from code
```gdscript
var mat := $Sprite2D.material as ShaderMaterial
mat.set_shader_parameter("flash", 1.0)
create_tween().tween_method(func(v): mat.set_shader_parameter("flash", v), 1.0, 0.0, 0.2)
```

## Shared vs unique
A material resource is **shared** by everything that references it. Changing a parameter changes all.
- Per-object: enable **Resource > Local to Scene** on the material (unique per scene instance), or
  `material = material.duplicate()` in `_ready()` (more unique material instances, which the docs note adds overhead).
- Better for many objects: **per-instance uniforms** (`instance uniform float flash = 0.0;`) set with
  `set_instance_shader_parameter("flash", 1.0)` on a GeometryInstance3D or CanvasItem: no unique material per node.
  They work in both `canvas_item` and `spatial` shaders, take scalars and vectors only (no textures or arrays) and
  have a practical maximum of 16 per shader (`instance_index(n)` pins an index from 0 to 15).
- `modulate` / `self_modulate` (multiplied into the fragment `COLOR`) are another per-sprite channel in 2D.

## Global uniforms
Project Settings > Shader Globals (`global uniform vec3 wind_dir;` in shaders), set at runtime:
`RenderingServer.global_shader_parameter_set("wind_dir", Vector3(1, 0, 0))`. Ideal for time of day, wind,
player position (grass bending). Assigning a global as often as needed does not hurt performance; avoid
`global_shader_parameter_get`, which synchronises with the render thread.

## Gotchas
- Parameter names are strings; a typo silently does nothing. Keep constants: `const FLASH := &"flash"`.

## Verify
- [ ] Hitting one enemy flashes only that enemy.
- [ ] Global wind change affects all foliage materials at once.

## Checked

Checked 2026-10-25 against the Godot 4.7 documentation (godot-docs stable branch, last commit 2026-10-24; latest engine release 4.7.2). Confirmed: `hint_range(min, max[, step])`, `source_color`, `hint_normal`, `hint_default_white/black/transparent`, `hint_screen_texture`, `filter_*`, `repeat_*`, `group_uniforms`; `hint_enum` takes separate strings (the earlier `"A,B"` form was wrong) and an int value is passed to `set_shader_parameter`; per-instance uniforms work in both `canvas_item` and `spatial` shaders (the earlier text said 3D only), exclude textures and arrays and have a practical limit of 16; `CanvasItem.set_instance_shader_parameter` exists; `Resource.resource_local_to_scene` duplicates the resource per scene instance; Project Settings > Shader Globals, `RenderingServer.global_shader_parameter_set`, and the cost of `global_shader_parameter_get`; `set_shader_parameter` names must match exactly. Removed the unconfirmed version gates, AnimationPlayer property path and batching claims.

Method: documentation only; no commands were run.
