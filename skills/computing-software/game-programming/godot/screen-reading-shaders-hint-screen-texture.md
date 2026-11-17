---
id: computing-software.game-programming.godot.screen-reading-shaders-hint-screen-texture
name: screen-reading-shaders-hint-screen-texture
category: computing-software
field: game-programming
product: godot
tags: [godot, godot-shaders, hint_screen_texture, depth-texture, screen-space-effects, game-programming]
level: practitioner
status: docs-checked
description: "Write Godot 4 screen-reading shaders with hint_screen_texture, hint_depth_texture and hint_normal_roughness_texture: distortion, outlines, BackBufferCopy and costs."
sources: ["https://docs.godotengine.org/en/stable/tutorials/shaders/screen-reading_shaders.html", "https://docs.godotengine.org/en/stable/tutorials/shaders/advanced_postprocessing.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Screen-reading shaders

**Goal:** heat haze, water refraction, blur panels, depth-based fog and outlines using the rendered
screen.

## Declaring screen textures (Godot 4)
```glsl
shader_type canvas_item;   // or spatial
uniform sampler2D screen_tex : hint_screen_texture, repeat_disable, filter_linear_mipmap;
void fragment() {
    vec2 offset = vec2(sin(UV.y * 40.0 + TIME * 3.0), 0.0) * 0.005;
    COLOR = textureLod(screen_tex, SCREEN_UV + offset, 0.0);
}
```
Declare a uniform with the `hint_screen_texture` hint (the `SCREEN_TEXTURE` built-in was removed in Godot 4). Use a
filter with `mipmap` in its name to get blur via `textureLod(screen_tex, uv, lod)`; without a mipmap
filter an LOD above 0.0 looks the same as 0.0.

## 3D extras
```glsl
shader_type spatial;
render_mode unshaded;
uniform sampler2D depth_tex : hint_depth_texture;
uniform sampler2D nr_tex : hint_normal_roughness_texture;   // Forward+ only; normal in .xyz (0..1), roughness in .w
void fragment() {
    float d = texture(depth_tex, SCREEN_UV).r;
    vec4 ndc = vec4(SCREEN_UV * 2.0 - 1.0, d, 1.0);          // depth is non-linear; Forward+/Mobile use 0..1 reverse-Z
    vec4 view = INV_PROJECTION_MATRIX * ndc; view.xyz /= view.w;
    float linear_depth = -view.z;
    ...
}
```
Full-screen post effect: a MeshInstance3D quad with `POSITION = vec4(VERTEX.xy, 1.0, 1.0);` in
`vertex()` (as in the "Advanced post-processing" docs page) with extra cull margin, or a
`CompositorEffect` for proper post-processing.

## What the screen texture contains
- 3D: the screen is copied after the opaque pass and before the transparent pass, so transparent
  objects are not captured. Materials using `hint_screen_texture` count as transparent themselves and do
  not appear in other materials' screen texture.
- 2D: when `hint_screen_texture` is first met, the whole screen is copied to a back buffer; later items
  reuse that copy unless a (non-disabled) `BackBufferCopy` node earlier in tree order copies again
  (it can copy the whole screen or a region; reading outside the region is undefined).

## Cost
The first screen-reading item in 2D triggers a full-screen copy; a mipmap filter also makes Godot
compute the blurred mip chain. Prefer a `BackBufferCopy` region when only part of the screen is read.

## Gotchas
- The normal-roughness texture is Forward+ only (not Mobile or Compatibility). The Compatibility
  renderer uses OpenGL NDC with a Z range of -1 to 1, so reconstruction code must differ there.
- Since Godot 4.3 the depth buffer is reverse-Z (near plane at 1.0): depth reconstruction code from older
  tutorials is wrong; follow the current Advanced post-processing page.
- Clamp offset UVs so distortion does not sample outside the screen.

## Verify
- [ ] Effect correct in both editor and exported build at different resolutions.
- [ ] Stacked 2D screen-reading items show each other's result (BackBufferCopy placed between them).

## Checked

Checked 2026-10-25 against the Godot 4.7 documentation (godot-docs stable branch, last commit 2026-10-24; latest engine release 4.7.2). Confirmed: `hint_screen_texture`, `hint_depth_texture`, `hint_normal_roughness_texture` (Forward+ only, normal in `.xyz` and roughness in `.w`); the mipmap-filter requirement for blurred `textureLod`; 3D copy happens after the opaque and before the transparent pass; 2D first-use copy and `BackBufferCopy` rules; the quad post-process uses `POSITION = vec4(VERTEX.xy, 1.0, 1.0)` with a large `extra_cull_margin`; reverse-Z since 4.3 and OpenGL NDC in Compatibility (Advanced post-processing page). The example's `NOISE` built-in does not exist and was replaced. `SCREEN_TEXTURE` is documented as removed in Godot 4. Removed the unconfirmed copy-cost and profiler claims.

Method: documentation only; no commands were run.
