---
id: creative-arts.animation.blender.gpu-custom-shader
name: gpu-custom-shader
category: creative-arts
field: animation
product: blender
tags: [blender, gpu-custom-shader, glsl, shader-create-info, gpu-module, gpu-batch, viewport-overlay]
level: advanced
status: docs-checked
description: "Write custom GLSL viewport shaders for Blender's gpu module with GPUShaderCreateInfo: vertex inputs, interfaces, push constants, batches and Metal and Vulkan compatibility."
sources:
  - https://docs.blender.org/api/current/gpu.html
  - https://docs.blender.org/api/current/gpu.types.html#gpu.types.GPUShaderCreateInfo
  - https://docs.blender.org/api/current/gpu.shader.html
  - https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html
  - https://developer.blender.org/docs/release_notes/5.0/python_api/
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# gpu-custom-shader

Goal: draw something the built-in shaders (`UNIFORM_COLOR`, `SMOOTH_COLOR`, `IMAGE`, `IMAGE_SCENE_LINEAR_TO_REC709_SRGB`, `POLYLINE_*`) cannot, in a way that works on OpenGL, Metal and Vulkan backends.

## Create the shader

```python
import bpy, gpu
from gpu_extras.batch import batch_for_shader

iface = gpu.types.GPUStageInterfaceInfo("my_iface")
iface.smooth('VEC3', "vPos")

info = gpu.types.GPUShaderCreateInfo()
info.push_constant('MAT4', "ModelViewProjectionMatrix")
info.push_constant('FLOAT', "time")
info.vertex_in(0, 'VEC3', "pos")
info.vertex_out(iface)
info.fragment_out(0, 'VEC4', "FragColor")
info.vertex_source("""
void main() {
  vPos = pos;
  gl_Position = ModelViewProjectionMatrix * vec4(pos, 1.0);
}""")
info.fragment_source("""
void main() {
  float s = 0.5 + 0.5 * sin(vPos.z * 10.0 + time);
  FragColor = vec4(s, 0.2, 1.0 - s, 1.0);
}""")
shader = gpu.shader.create_from_info(info)
del info, iface
```

Declarations (inputs, outputs, uniforms) go in the create-info, not in the GLSL text: Blender generates them per backend. Textures: `info.sampler(0, 'FLOAT_2D', "image")` and `shader.uniform_sampler("image", gpu.texture.from_image(img))`.

## Draw

```python
coords = [(0, 0, 0), (1, 0, 0), (0, 1, 1)]
batch = batch_for_shader(shader, 'TRIS', {"pos": coords})

def draw():
    shader.bind()
    shader.uniform_float("ModelViewProjectionMatrix",
                         gpu.matrix.get_projection_matrix() @ gpu.matrix.get_model_view_matrix())
    shader.uniform_float("time", bpy.context.scene.frame_current * 0.1)
    gpu.state.depth_test_set('LESS_EQUAL')
    batch.draw(shader)
    gpu.state.depth_test_set('NONE')
```
Register `draw` with a `POST_VIEW` draw handler (see `creative-arts.animation.blender.draw-handler-cleanup`). Build the shader and batch once, outside the callback.

## Gotchas

- Build shaders with `GPUShaderCreateInfo`: the 5.2 API docs list no `GPUShader` constructor, and the 5.0 release notes say creating shaders directly from GLSL source files was removed.
- The GLSL is cross-compiled for each backend; the API docs link a GLSL Cross Compilation page for the rules, so read it before using legacy GLSL built-ins.
- Restore every `gpu.state` you change, or other overlays draw wrong (practice).
- Textures from `gpu.texture.from_image` drawn inside a Python draw handler need `draw_texture_2d(is_scene_linear_with_rec709_srgb_target=True)` or the `IMAGE_SCENE_LINEAR_TO_REC709_SRGB` built-in shader (5.0 release notes); a custom sampler shader has to handle the colour conversion itself.

## Verify

The triangle draws in the viewport with the animated colour on scrubbing; start Blender with `--gpu-backend vulkan` (valid values: `vulkan`, `metal`, `opengl`) and confirm it still compiles.

## Checked

Blender Python API 5.2 (docs.blender.org/api/current) and manual command-line page, read 2026-10-27.
- `GPUStageInterfaceInfo(name).smooth(type, name)`, `GPUShaderCreateInfo.push_constant/vertex_in/vertex_out/fragment_out/vertex_source/fragment_source/sampler`, `gpu.shader.create_from_info`, `GPUShader.uniform_sampler`, `gpu.texture.from_image`, `gpu.matrix.get_projection_matrix/get_model_view_matrix`, `gpu.state.depth_test_set` modes, built-in shader names (UNIFORM_COLOR, SMOOTH_COLOR, IMAGE, IMAGE_SCENE_LINEAR_TO_REC709_SRGB, POLYLINE_*): API 5.2.
- `--gpu-backend` accepts vulkan, metal, opengl: manual command-line arguments. GLSL-source shader removal and the from_image drawing rule: developer-docs Python API notes for 5.0.
- Removed as unconfirmed: the `GPUShader(vertexcode, fragcode)` constructor advice, the list of forbidden GLSL constructs, the compile-error line-number claim, the background-mode guard, the 4.2 Vulkan tag.

Method: documentation only; no commands were run.
