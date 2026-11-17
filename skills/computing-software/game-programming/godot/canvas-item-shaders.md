---
id: computing-software.game-programming.godot.canvas-item-shaders
name: canvas-item-shaders
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, godot-shaders, canvas-item-shader, 2d-shaders, hit-flash, outline-shader, dissolve, screen-texture, godot-shading-language, game-programming]
level: practitioner
status: docs-checked
description: "Write Godot canvas_item shaders for 2D effects: hit flash, outline, dissolve; built-ins like TEXTURE/UV/COLOR, screen reading and instance uniforms."
sources: ["https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/canvas_item_shader.html", "https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shading_language.html", "https://docs.godotengine.org/en/stable/tutorials/shaders/screen-reading_shaders.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# canvas_item shaders

**Goal:** common 2D sprite effects as small, reusable shaders driven from gameplay code.

## Skeleton
```glsl
shader_type canvas_item;

uniform vec4 flash_color : source_color = vec4(1.0);
uniform float flash_amount : hint_range(0.0, 1.0) = 0.0;

void fragment() {
    vec4 tex = COLOR;   // input COLOR = vertex color * modulate * self_modulate * TEXTURE sample
    COLOR = vec4(mix(tex.rgb, flash_color.rgb, flash_amount), tex.a);
}
```
Assign via the CanvasItem's Material > New ShaderMaterial > Shader. Built-ins: `TEXTURE`, `UV`,
`COLOR`, `TEXTURE_PIXEL_SIZE`, `TIME`, `SCREEN_UV`, `VERTEX` (in `vertex()`), `FRAGCOORD`.
`render_mode unshaded;` ignores 2D lights; `blend_add` for additive glow.

## Hit flash from code
```gdscript
func flash() -> void:
    var mat := $Sprite2D.material as ShaderMaterial
    mat.set_shader_parameter("flash_amount", 1.0)
    var tw := create_tween()
    tw.tween_method(func(v): mat.set_shader_parameter("flash_amount", v), 1.0, 0.0, 0.15)
```
Each sprite needs its own material instance (Material > Resource > Local To Scene, or duplicate) or
use **instance uniforms** (`instance uniform float flash_amount;`) set with
`set_instance_shader_parameter` (available on CanvasItem and GeometryInstance3D), which keeps one
shared material instead of a unique material per node.

## Outline (sample neighbours by pixel size)
```glsl
uniform vec4 outline_color : source_color = vec4(0,0,0,1);
uniform float width = 1.0;
void fragment() {
    vec4 c = texture(TEXTURE, UV);
    vec2 px = TEXTURE_PIXEL_SIZE * width;
    float a = texture(TEXTURE, UV + vec2(px.x, 0)).a + texture(TEXTURE, UV - vec2(px.x, 0)).a
            + texture(TEXTURE, UV + vec2(0, px.y)).a + texture(TEXTURE, UV - vec2(0, px.y)).a;
    COLOR = mix(vec4(outline_color.rgb, min(a, 1.0) * outline_color.a), c, c.a);
}
```
Outlines at sprite edges need transparent padding in the texture (or in atlas regions), otherwise
they are clipped by the quad.

## Dissolve
```glsl
uniform sampler2D noise;               // NoiseTexture2D
uniform float progress : hint_range(0, 1);
void fragment() {
    float n = texture(noise, UV).r;
    if (n < progress) discard;
    COLOR = COLOR + vec4(1.0, 0.5, 0.0, 0.0) * step(n, progress + 0.05);  // COLOR already includes the texture; burning edge
}
```

## Screen-reading effects
`uniform sampler2D screen_tex : hint_screen_texture, filter_linear_mipmap;` and
`texture(screen_tex, SCREEN_UV)` for distortion/blur behind a node. Use a `BackBufferCopy` node to
control when the screen is copied when several such effects stack.

## Gotchas
- `source_color` hint for colors so sRGB conversion is correct.
- Texture filtering: pixel art needs Nearest (project default texture filter or `filter_nearest`
  hint on samplers).
- The first argument of `set_shader_parameter()` must match the uniform name exactly.

## Verify
- [ ] Flash on one enemy does not flash all enemies sharing the scene.
- [ ] Outline visible on all sides of atlas sprites (padding present).

## Checked

Checked 2026-10-25 against the Godot 4.7 documentation (godot-docs stable branch, last commit 2026-10-24; latest engine release 4.7.2). Confirmed: in `fragment()` the input `COLOR` is the vertex colour times `modulate` times `self_modulate` times the `TEXTURE` sample (the earlier flash and dissolve examples multiplied the texture in twice and were corrected); `TEXTURE_PIXEL_SIZE`, `SCREEN_UV`, `FRAGCOORD`, `unshaded` and `blend_add`; per-instance uniforms are available in both `canvas_item` and `spatial` shaders and `set_instance_shader_parameter` exists on CanvasItem; `source_color` guidance; `BackBufferCopy` behaviour for stacked screen-reading items. Removed the unconfirmed batching and draw-call claims.

Method: documentation only; no commands were run.
