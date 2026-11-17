---
id: computing-software.game-programming.godot.sky-shaders
name: sky-shaders
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, sky-shader, environment, procedural-sky, shaders, game-programming]
level: practitioner
status: docs-checked
description: "Write Godot sky shaders (shader_type sky): EYEDIR and light built-ins, day-night cycles, stars and clouds, radiance update modes and performance settings."
sources: ["https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/sky_shader.html", "https://docs.godotengine.org/en/stable/classes/class_sky.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sky shaders

**Goal:** a custom procedural sky with sun, stars and clouds that also lights the scene.

## Setup
WorldEnvironment > Environment > Background **Sky** > Sky resource > `sky_material` = ShaderMaterial
with a sky shader. 
## Example
```glsl
shader_type sky;
uniform vec3 day_top : source_color = vec3(0.25, 0.45, 0.9);
uniform vec3 horizon : source_color = vec3(0.8, 0.85, 0.9);
uniform sampler2D stars : filter_linear, repeat_enable;

void sky() {
    float h = clamp(EYEDIR.y, 0.0, 1.0);
    vec3 col = mix(horizon, day_top, pow(h, 0.5));
    if (LIGHT0_ENABLED) {
        float sun = smoothstep(0.9995, 0.9999, dot(EYEDIR, LIGHT0_DIRECTION));
        col += LIGHT0_COLOR * LIGHT0_ENERGY * sun;
        float night = clamp(-LIGHT0_DIRECTION.y * 4.0, 0.0, 1.0);
        col = mix(col, texture(stars, SKY_COORDS * 4.0).rgb, night * h);
    }
    COLOR = col;
}
```
Built-ins: `EYEDIR`, `SKY_COORDS` (equirect UV), `POSITION` (camera), `LIGHTn_DIRECTION/COLOR/ENERGY/ENABLED`
(DirectionalLight3D nodes, up to 4), `TIME`, `AT_HALF_RES_PASS`, `AT_QUARTER_RES_PASS`,
`AT_CUBEMAP_PASS`, `HALF_RES_COLOR`, `RADIANCE` for reflections.

## Day-night
Rotate the DirectionalLight3D; the sky reads LIGHT0_DIRECTION so it follows automatically. Ambient
and reflections come from the sky radiance.

## Performance and radiance
- Sky `process_mode`: Automatic (picks Real-Time if the shader uses `TIME` or `POSITION`, Incremental
  if it uses `LIGHTn_*` or custom uniforms), Quality (high quality importance sampling, slow, not for
  sky that changes at runtime), Incremental (same quality, updated over several frames), Real-Time
  (fast filter; `radiance_size` must be 256x256 or a warning is printed and the size is ignored).
  Use Incremental for a slowly moving time of day and Real-Time when the radiance changes every frame.
- `render_mode use_half_res_pass` / `use_quarter_res_pass`: compute expensive clouds at lower res and
  read via `HALF_RES_COLOR`.
- Branch on `AT_CUBEMAP_PASS` to render the full sky into the radiance cubemap and read it back with
  `texture(RADIANCE, EYEDIR)` in the visible pass (`RADIANCE` is only readable when `!AT_CUBEMAP_PASS`);
  this runs the complex code only when the cubemap updates.

## Gotchas
- The radiance cubemap is re-rendered whenever `TIME` is used, `POSITION` is used and the camera
  moves, a `LIGHTn_*` value is used and a DirectionalLight3D changes, or any uniform changes. The
  process mode only affects the radiance cubemap; the visible sky always runs the full shader.
- Use `source_color` hints for picked colours.

## Verify
- [ ] Day/night transition looks right and ambient lighting follows; sky cost in the Visual Profiler is acceptable.

## Checked

Checked 2026-10-25 against the Godot 4.7 documentation (godot-docs stable branch, last commit 2026-10-24; latest engine release 4.7.2) and the engine's ProceduralSkyMaterial shader source. Confirmed: `EYEDIR`, `SKY_COORDS`, `POSITION`, `LIGHTn_ENABLED/DIRECTION/COLOR/ENERGY` for four lights (`LIGHT0` to `LIGHT3`), `AT_HALF_RES_PASS`, `AT_QUARTER_RES_PASS`, `AT_CUBEMAP_PASS`, `HALF_RES_COLOR`, `RADIANCE`, render modes `use_half_res_pass` and `use_quarter_res_pass`; the list of changes that force a radiance update; Sky process mode semantics and the 256x256 radiance size limit for Real-Time (class reference for Sky); the engine's own sky code uses `dot(LIGHT0_DIRECTION, EYEDIR)` for the sun disc, matching the example. Removed the unconfirmed Convert-to-ShaderMaterial step.

Method: documentation only; no commands were run.
