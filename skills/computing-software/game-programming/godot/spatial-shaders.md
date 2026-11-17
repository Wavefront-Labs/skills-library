---
id: computing-software.game-programming.godot.spatial-shaders
name: spatial-shaders
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, godot-shaders, spatial-shader, shading-language, vertex-fragment-light, render-modes, game-programming]
level: practitioner
status: docs-checked
description: "Write Godot 4 spatial shaders: shader_type spatial, render_mode flags, vertex/fragment/light functions and built-ins, screen and depth textures, and performance limits."
sources: ["https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/spatial_shader.html", "https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shading_language.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spatial shaders

**Goal:** custom 3D materials (dissolve, toon, water, hologram) in Godot's shading language.

## Skeleton
```glsl
shader_type spatial;
render_mode blend_mix, depth_draw_opaque, cull_back, diffuse_burley, specular_schlick_ggx;

uniform sampler2D albedo_tex : source_color, filter_linear_mipmap, repeat_enable;
uniform sampler2D noise : hint_default_white;
uniform float dissolve : hint_range(0.0, 1.0) = 0.0;
uniform vec4 edge_color : source_color = vec4(1.0, 0.5, 0.0, 1.0);

void vertex() {
    // VERTEX, NORMAL, UV in model space; MODEL_MATRIX, VIEW_MATRIX available
}

void fragment() {
    float n = texture(noise, UV).r;
    if (n < dissolve) discard;                               // alpha-scissor style cutout
    ALBEDO = texture(albedo_tex, UV).rgb;
    EMISSION = edge_color.rgb * step(n, dissolve + 0.05) * 4.0;
    ROUGHNESS = 0.6; METALLIC = 0.0;
}
```
- `source_color` hint marks sRGB textures/colors (converted to linear). Forgetting it washes out colors.
- Outputs: `ALBEDO`, `ALPHA` (enables transparency), `NORMAL_MAP`, `ROUGHNESS`, `METALLIC`, `EMISSION`, `AO`, `RIM`, `SSS_STRENGTH`.
- Built-ins: `TIME`, `UV`, `UV2`, `COLOR`, `VERTEX` (view space in fragment), `NORMAL`, `VIEW`, `FRAGCOORD`, `INSTANCE_CUSTOM`.

## Render modes worth knowing
`unshaded` (no lighting: holograms, UI in 3D), `cull_disabled` (foliage), `depth_draw_always`,
`depth_test_disabled` (overlays), `blend_add` (glow), `shadows_disabled`, `world_vertex_coords`,
`skip_vertex_transform`, `fog_disabled`, `diffuse_toon`/`specular_toon`.

## light() for custom lighting (toon)
```glsl
void light() {
    float ndl = dot(NORMAL, LIGHT);
    float band = step(0.0, ndl) * 0.7 + step(0.6, ndl) * 0.3;
    DIFFUSE_LIGHT += band * ATTENUATION * LIGHT_COLOR / PI;
}
```
`light()` is called for every light in every pixel; add contributions with `+=` so lights accumulate. It is not run when the `vertex_lighting` render mode or Project Settings > Rendering > Quality > Shading > Force Vertex Shading is on, and `unshaded` skips it.

## Screen and depth
```glsl
uniform sampler2D screen_tex : hint_screen_texture, filter_linear_mipmap;
uniform sampler2D depth_tex : hint_depth_texture;
// refraction: texture(screen_tex, SCREEN_UV + offset); depth: texture(depth_tex, SCREEN_UV).r -> linearise with INV_PROJECTION_MATRIX
```
Screen texture reads only include opaque objects (rendered before transparents).

## Performance
- Reading or writing `ALPHA` sends the material to the transparent pipeline; for hard cut-outs write `ALPHA_SCISSOR_THRESHOLD` instead (values below it are discarded).
- `unshaded` skips lighting and is documented as faster to render.

## Verify
- [ ] Colors match the texture (source_color hints set).
- [ ] Material works in Forward+ and Mobile renderers if you ship both.

## Checked

Checked 2026-10-25 against the Godot 4.7 documentation (godot-docs stable branch, last commit 2026-10-24; latest engine release 4.7.2). Confirmed: render mode names (`blend_mix`, `blend_add`, `depth_draw_opaque`, `depth_draw_always`, `depth_test_disabled`, `cull_back`, `cull_disabled`, `diffuse_burley`, `diffuse_toon`, `specular_schlick_ggx`, `specular_toon`, `unshaded`, `shadows_disabled`, `world_vertex_coords`, `skip_vertex_transform`, `fog_disabled`, `vertex_lighting`); fragment outputs `ALBEDO`, `ALPHA`, `ALPHA_SCISSOR_THRESHOLD`, `NORMAL_MAP`, `ROUGHNESS`, `METALLIC`, `EMISSION`, `AO`, `RIM`, `SSS_STRENGTH`; `VERTEX` is in view space in `fragment()`; the `light()` loop and its `ATTENUATION`, `LIGHT_COLOR`, `DIFFUSE_LIGHT` use; screen texture excludes transparent objects. Removed the unconfirmed early-z and Convert-to-ShaderMaterial claims.

Method: documentation only; no commands were run.
