---
id: creative-arts.animation.blender.gpu-module-drawing
name: gpu-module-drawing
category: creative-arts
field: animation
product: blender
tags: [blender, gpu-module, draw-handler, viewport-overlay, bgl, gpu-shader, blf, custom-gizmo, overlay-drawing, batch, offscreen-render, python, tool-ui, draw-handler-add, gpu-batch, gpu-builtin-shaders, gpu-state]
level: sme
status: docs-checked
description: "Draw overlays in Blender editors with the gpu module: draw handlers, built-in shaders, batches, blf text, depth/blend state, offscreen rendering, gizmos, bgl migration."
sources:
  - https://docs.blender.org/api/current/gpu.html
  - https://docs.blender.org/api/current/gpu.shader.html
  - https://docs.blender.org/api/current/blf.html
  - https://docs.blender.org/api/current/bpy.types.SpaceView3D.html#bpy.types.SpaceView3D.draw_handler_add
  - https://developer.blender.org/docs/release_notes/5.0/python_api/
  - https://docs.blender.org/api/current/bpy.types.Gizmo.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# gpu-module-drawing

Goal: draw lines, shapes, images and text over the 3D viewport (or any editor) from Python for tools, measurements, debug visualisation and HUDs — using `gpu`, which is backend-neutral (`--gpu-backend` accepts vulkan, metal, opengl); the old `bgl` module no longer appears in the current API docs.

## Draw handlers

```python
import bpy, gpu
from gpu_extras.batch import batch_for_shader

coords = [(0,0,0), (1,1,1)]
shader = gpu.shader.from_builtin('UNIFORM_COLOR')     # built-in names: 'UNIFORM_COLOR', 'SMOOTH_COLOR', 'FLAT_COLOR', 'IMAGE', 'IMAGE_COLOR', 'POINT_UNIFORM_COLOR', 'POLYLINE_UNIFORM_COLOR', 'POLYLINE_FLAT_COLOR', 'POLYLINE_SMOOTH_COLOR'
batch = batch_for_shader(shader, 'LINES', {"pos": coords})   # 'POINTS','LINES','LINE_STRIP','LINE_LOOP','TRIS','TRI_STRIP','TRI_FAN', indices=...

def draw():
    gpu.state.blend_set('ALPHA'); gpu.state.line_width_set(2.0); gpu.state.depth_test_set('LESS_EQUAL')
    shader.uniform_float("color", (1.0, 0.5, 0.0, 0.8))
    batch.draw(shader)
    gpu.state.depth_test_set('NONE'); gpu.state.blend_set('NONE')

handle = bpy.types.SpaceView3D.draw_handler_add(draw, (), 'WINDOW', 'POST_VIEW')
# remove: bpy.types.SpaceView3D.draw_handler_remove(handle, 'WINDOW')
```
- `draw_handler_add(callback, args, region_type, draw_type)`: region `'WINDOW'` (main), `'HEADER'`, `'UI'`, `'TOOLS'`; draw type **`'POST_VIEW'`** (3D space — coordinates are world units, respects the view matrix; use for lines on geometry), **`'POST_PIXEL'`** (2D screen pixels after everything — HUD text, boxes), `'PRE_VIEW'` (in some cases), `'BACKDROP'` (node editor backdrops). Other editor space classes such as `SpaceImageEditor` have the same `draw_handler_add`.
- The callback is called every time the region is drawn: build batches once and rebuild only when data changes (practice); store the handle on a module/class attribute and remove it on unregister/`finish`. Force a redraw after changing data: `area.tag_redraw()` or `context.region.tag_redraw()`.
- During development, wrap the callback body in try/except so an error does not repeat on every redraw (practice).

## Shaders and batches

- Built-ins (`gpu.shader.from_builtin(name)`): `UNIFORM_COLOR` (one `color` uniform; `pos` attribute), `SMOOTH_COLOR`/`FLAT_COLOR` (per-vertex `color` attribute), `IMAGE` (textured quad: `pos` + `texCoord`, `shader.uniform_sampler("image", tex)`), `POLYLINE_*` (wide lines — set the `lineWidth` and `viewportSize` uniforms: `shader.uniform_float("lineWidth", 3.0)`, `shader.uniform_float("viewportSize", (w, h))`). `gpu.state.line_width_set(width)` sets the width of rasterized lines; prefer POLYLINE shaders for thick lines (practice). Point size: `gpu.state.point_size_set(6)`; a `POINT_UNIFORM_COLOR` built-in exists.
- Custom shaders: `gpu.types.GPUShaderCreateInfo()` → `.vertex_in(0, 'VEC3', "pos")`, `.push_constant('MAT4', "ModelViewProjectionMatrix")`, `.fragment_out(0, 'VEC4', "FragColor")`, `.vertex_source(...)`, `.fragment_source(...)`, then `gpu.shader.create_from_info(info)`. See `creative-arts.animation.blender.gpu-custom-shader` for a full example; the matrices are available as `gpu.matrix.get_model_view_matrix()` / `get_projection_matrix()`.
- `gpu.matrix` stack: `with gpu.matrix.push_pop(): gpu.matrix.multiply_matrix(ob.matrix_world); batch.draw(shader)` draws local-space geometry under an object transform; `gpu.matrix.load_matrix`, `translate`, `scale`.
- Depth: `gpu.state.depth_test_set('LESS_EQUAL')` for occluded-by-geometry drawing; `'NONE'` for always-on-top (X-ray). `depth_mask_set(True)` to write depth. Blend modes: `'ALPHA'`, `'ADDITIVE'`, `'MULTIPLY'`, `'ALPHA_PREMULT'`. `face_culling_set('BACK')`. Scissor: `gpu.state.scissor_set(x,y,w,h)` + `scissor_test_set(True)`.
- 2D ↔ 3D: `from bpy_extras import view3d_utils`; `view3d_utils.location_3d_to_region_2d(region, rv3d, co)` for labels anchored to points; `region_2d_to_location_3d`, `region_2d_to_origin_3d` + `region_2d_to_vector_3d` for picking rays.
- Images: `tex = gpu.texture.from_image(img)` (bpy image → GPU texture), or `gpu.types.GPUTexture((w,h), format='RGBA8', data=buffer)`; draw with the `IMAGE` shader on a quad; `gpu_extras.presets.draw_texture_2d(tex, (x,y), w, h)` is the one-liner. Circles: `gpu_extras.presets.draw_circle_2d(center, color, radius, segments=32)`.

## Text (`blf`)

```python
import blf
font_id = 0                          # default UI font; blf.load("//fonts/x.ttf") for custom
def draw_text():
    blf.size(font_id, 14.0)          # 4.x: (font_id, size) ; older: (font_id, size, dpi)
    blf.color(font_id, 1, 1, 1, 1)
    blf.enable(font_id, blf.SHADOW); blf.shadow(font_id, 3, 0, 0, 0, 0.8); blf.shadow_offset(font_id, 1, -1)
    blf.position(font_id, 20, 40, 0); blf.draw(font_id, "Frame 1001")
    w, h = blf.dimensions(font_id, "Frame 1001")   # for backgrounds/right-align
    blf.disable(font_id, blf.SHADOW)
```
Use `POST_PIXEL`; scale sizes by `bpy.context.preferences.system.ui_scale` for HiDPI. `blf.clipping`, `blf.rotation` (with `blf.ROTATION` enabled), `blf.word_wrap`.

## Offscreen rendering

`off = gpu.types.GPUOffScreen(w, h)`; `with off.bind(): fb = gpu.state.active_framebuffer_get(); fb.clear(color=(0,0,0,0)); with gpu.matrix.push_pop(): gpu.matrix.load_matrix(view); gpu.matrix.load_projection_matrix(proj); draw...` then `buf = off.texture_color.read()` → `bpy.data.images.new(...).pixels.foreach_set(...)`. `off.draw_view3d(scene, view_layer, view3d, region, view_matrix, proj_matrix)` renders the viewport itself offscreen (thumbnail generators, custom playblasts, texture painting projections). Projection from a camera: `cam.calc_matrix_camera(depsgraph, x=w, y=h)`; view matrix: `cam.matrix_world.inverted()`.

## Gizmos (interactive handles)

`bpy.types.Gizmo` subclasses with `draw`/`draw_select`/`invoke`/`modal`/`exit` + a `GizmoGroup` (`bl_space_type='VIEW_3D'`, `bl_region_type='WINDOW'`, `bl_options={'3D','PERSISTENT'}`, `poll`, `setup` creating `self.gizmos.new("GIZMO_GT_arrow_3d")` etc.) — built-in gizmo types are created by identifier with `self.gizmos.new(type)` (for example `"GIZMO_GT_arrow_3d"`; the identifier list is not on the API pages). Link to properties with `gz.target_set_prop("offset", ob, "location", index=2)` or operators with `gz.target_set_operator("transform.translate")`; `gz.matrix_basis`, `color`, `alpha`, `scale_basis`, `use_draw_modal`. Custom shapes: `self.new_custom_shape('TRIS', verts)` in `setup` and `self.draw_custom_shape(shape)` in `draw`. Gizmos suit things the user drags; draw handlers suit pure display (practice).

## Migrating from bgl

| bgl | gpu |
|---|---|
| `bgl.glEnable(bgl.GL_BLEND)` | `gpu.state.blend_set('ALPHA')` |
| `glLineWidth(2)` | `gpu.state.line_width_set(2)` or POLYLINE shaders |
| `glEnable(GL_DEPTH_TEST)` | `gpu.state.depth_test_set('LESS_EQUAL')` |
| `glPointSize` | `gpu.state.point_size_set` |
| `glScissor` | `gpu.state.scissor_set` |
| `bgl.Buffer` + `glReadPixels` | `fb.read_color(...)`, `GPUTexture.read()` |
| `'2D_UNIFORM_COLOR'` / `'3D_UNIFORM_COLOR'` shader names | `'UNIFORM_COLOR'` (the 2D/3D prefixes were dropped in 4.0) |

## Gotchas

- Forgetting to remove a handler (or reloading the add-on without removing) leaves ghost drawings until restart; keep the handle in a module variable and guard `register`.
- Drawing in `POST_VIEW` without a depth test shows through geometry; with `'LESS_EQUAL'`, lines lying on a surface can z-fight, so offset them slightly along the normal (practice).
- Built-in shader attribute and uniform names must match the shader's listing in the API docs (`"pos"`, `"color"`, `"texCoord"`, `"image"`).
- Avoid calling operators from draw callbacks (practice).
- Text size API changed in 4.0 (`blf.size(font, size)` — no dpi); check `bpy.app.version`.
- Reading pixels back is a synchronisation point on the GPU; do it on demand (practice).
- Textures from `gpu.texture.from_image` drawn inside a Python draw handler need `draw_texture_2d(is_scene_linear_with_rec709_srgb_target=True)` or the `IMAGE_SCENE_LINEAR_TO_REC709_SRGB` built-in shader (5.0 release notes).

## Verify

- A `POST_VIEW` line between two objects follows them when moved (`tag_redraw` from a `depsgraph_update_post`), is occluded when depth test is on, and disappears on unregister.
- `POST_PIXEL` text stays at 20,40 px regardless of view, scales with UI scale, reads crisp (shadow on).
- Offscreen render of the active camera at 512×512 lands in a new Image data-block that matches the viewport framing.
- Gizmo arrow drags change the linked property and undo works in one step.

## Checked

Blender Python API 5.2 (docs.blender.org/api/current) and developer-docs release notes 4.0 and 5.0, read 2026-10-27.
- Built-in shader names and the POLYLINE `lineWidth`/`viewportSize` uniforms, `gpu.state` functions and blend modes, `gpu.matrix` functions, `gpu_extras.batch.batch_for_shader`, `gpu_extras.presets.draw_texture_2d/draw_circle_2d`, `blf` functions (`blf.size(fontid, size)`, shadow, clipping, rotation, word_wrap), `GPUOffScreen(width, height, *, format)` with `bind`, `draw_view3d`, `texture_color`, `GPUFrameBuffer.clear/read_color`, `GPUTexture(size, *, layers, is_cubemap, format, data)`, `Gizmos.new(type)`, `Gizmo.target_set_prop/target_set_operator/new_custom_shape/draw_custom_shape`, GizmoGroup `bl_options` incl. 3D and PERSISTENT, `bpy_extras.view3d_utils` functions, `Object.calc_matrix_camera`.
- 4.0 notes: `blf.size()` dpi argument removed; the 2D_/3D_ shader-name prefixes removed. 5.0 notes: from_image drawing rule.
- Removed as unconfirmed: bgl deprecation dates, line-width limits on Metal/Vulkan, the background-mode gpu claim, the GLSL `#version` rule, built-in gizmo identifier list, performance remarks.

Method: documentation only; no commands were run.
