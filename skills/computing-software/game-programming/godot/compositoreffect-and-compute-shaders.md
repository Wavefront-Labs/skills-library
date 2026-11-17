---
id: computing-software.game-programming.godot.compositoreffect-and-compute-shaders
name: compositoreffect-and-compute-shaders
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, compositoreffect, compute-shaders, renderingdevice, post-processing, game-programming]
level: practitioner
status: docs-checked
description: "Add custom post-processing in Godot 4.3+ with CompositorEffect and RenderingDevice compute shaders: callback stages, scene buffers, uniform sets and dispatch."
sources: ["https://docs.godotengine.org/en/stable/tutorials/rendering/compositor.html", "https://docs.godotengine.org/en/stable/tutorials/shaders/compute_shaders.html", "https://docs.godotengine.org/en/stable/classes/class_compositoreffect.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CompositorEffect and compute shaders

**Goal:** custom full-screen effects inside the render pipeline (outline, custom fog, colour grading)
rather than a screen-space quad hack.

## Setup
`WorldEnvironment` or `Camera3D` > **Compositor** resource > add a `CompositorEffect` subclass.
Forward+ and Mobile renderers only (needs RenderingDevice).

```gdscript
@tool
class_name GrayscaleEffect
extends CompositorEffect
var rd: RenderingDevice
var shader: RID; var pipeline: RID

func _init() -> void:
    effect_callback_type = EFFECT_CALLBACK_TYPE_POST_TRANSPARENT
    rd = RenderingServer.get_rendering_device()
    RenderingServer.call_on_render_thread(_init_compute)

func _init_compute() -> void:
    var src: RDShaderFile = load("res://fx/grayscale.glsl")
    shader = rd.shader_create_from_spirv(src.get_spirv())
    pipeline = rd.compute_pipeline_create(shader)

func _render_callback(type: int, data: RenderData) -> void:
    var buffers := data.get_render_scene_buffers() as RenderSceneBuffersRD
    var size := buffers.get_internal_size()
    for view in buffers.get_view_count():
        var img := buffers.get_color_layer(view)
        var u := RDUniform.new(); u.uniform_type = RenderingDevice.UNIFORM_TYPE_IMAGE; u.binding = 0; u.add_id(img)
        var uniform_set := UniformSetCacheRD.get_cache(shader, 0, [u])
        var cl := rd.compute_list_begin()
        rd.compute_list_bind_compute_pipeline(cl, pipeline)
        rd.compute_list_bind_uniform_set(cl, uniform_set, 0)
        rd.compute_list_dispatch(cl, (size.x - 1) / 8 + 1, (size.y - 1) / 8 + 1, 1)
        rd.compute_list_end()

func _notification(what: int) -> void:
    if what == NOTIFICATION_PREDELETE and shader.is_valid(): rd.free_rid(shader)
```
```glsl
#[compute]
#version 450
layout(local_size_x = 8, local_size_y = 8) in;
layout(rgba16f, set = 0, binding = 0) uniform image2D color;
void main() { ivec2 p = ivec2(gl_GlobalInvocationID.xy); vec4 c = imageLoad(color, p);
  float g = dot(c.rgb, vec3(0.299, 0.587, 0.114)); imageStore(color, p, vec4(vec3(g), c.a)); }
```
Pass parameters with push constants (`compute_list_set_push_constant`, 16-byte aligned).

## Callback stages
PRE_OPAQUE, POST_OPAQUE, POST_SKY, PRE_TRANSPARENT, POST_TRANSPARENT. Request depth/normal-roughness
buffers with `needs_normal_roughness`, `access_resolved_depth` flags; motion vectors with
`needs_motion_vectors`.

## Gotchas
- RenderingDevice calls must happen on the render thread; `_render_callback` already is.
- Free the RIDs you create (free the shader in `NOTIFICATION_PREDELETE`; freeing it also frees the pipeline).
- Bounds-check `p` against size in the shader for non-multiple-of-8 resolutions.

## Verify
- [ ] Effect works in the editor viewport (the script is a `@tool`) and in an exported build.

## Checked

Checked 2026-10-25 against the Godot 4.7 documentation (godot-docs stable branch, last commit 2026-10-24; latest engine release 4.7.2). Confirmed: the Compositor resource on WorldEnvironment or Camera3D; Forward+ and Mobile renderers only; `effect_callback_type` values PRE_OPAQUE, POST_OPAQUE, POST_SKY, PRE_TRANSPARENT, POST_TRANSPARENT; `needs_normal_roughness`, `access_resolved_depth`, `needs_motion_vectors`; `RenderSceneBuffersRD.get_internal_size/get_view_count/get_color_layer`, `UniformSetCacheRD.get_cache`, `rd.shader_create_from_spirv`, `compute_pipeline_create`, `compute_list_*`, `free_rid`; push constants padded to 16 bytes; `_render_callback` runs on the render thread; `RenderingServer.call_on_render_thread` exists. The dispatch group count now uses the tutorial's `(size - 1) / 8 + 1`, and the `set` variable name (a GDScript keyword) was renamed. Removed the unconfirmed leak and RenderDoc claims.

Method: documentation only; no commands were run.
