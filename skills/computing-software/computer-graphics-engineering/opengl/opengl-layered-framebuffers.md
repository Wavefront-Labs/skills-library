---
id: computing-software.computer-graphics-engineering.opengl.opengl-layered-framebuffers
name: opengl-layered-framebuffers
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, framebuffer, layered-framebuffer, gl-layer, layered-rendering, cubemap-rendering]
level: advanced
status: docs-checked
description: "Render to all faces of a cube map or all layers of an array in one pass with layered FBOs and gl_Layer from vertex or geometry shaders."
sources: ["https://registry.khronos.org/OpenGL/specs/gl/glspec46.core.pdf", "https://registry.khronos.org/OpenGL/specs/gl/GLSLangSpec.4.60.pdf", "https://registry.khronos.org/OpenGL/extensions/ARB/ARB_shader_viewport_layer_array.txt"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Layered framebuffers

Attaching a whole cube map, 3D texture or 2D array with `glNamedFramebufferTexture` (no layer
argument) makes the FBO **layered**. Each primitive is routed to a layer by writing `gl_Layer`.

```c
glNamedFramebufferTexture(fbo, GL_DEPTH_ATTACHMENT, shadowCubeArray, 0);   // all layers
// vs glNamedFramebufferTextureLayer(fbo, GL_DEPTH_ATTACHMENT, tex, 0, layer) = single layer, not layered
```
If any attachment is layered, all populated attachments must be layered and be textures of the same target
(3D, 1D/2D array, cube map or cube map array), otherwise `GL_FRAMEBUFFER_INCOMPLETE_LAYER_TARGETS`. If layer
counts differ, rendering is limited to the smallest count.

## Writing gl_Layer
**Vertex shader + instancing (needs the `ARB_shader_viewport_layer_array` extension: GLSL 4.60 core only
lets geometry shaders write `gl_Layer`):**
```glsl
#extension GL_ARB_shader_viewport_layer_array : require
uniform mat4 uFaceViewProj[6];
void main() {
    gl_Layer = gl_InstanceID;                         // draw with instanceCount = 6
    gl_Position = uFaceViewProj[gl_InstanceID] * uModel * vec4(aPos, 1);
}
```
**Geometry shader (core):**
```glsl
layout(triangles, invocations = 6) in;               // instanced GS: one invocation per face
layout(triangle_strip, max_vertices = 3) out;
void main() {
    for (int i = 0; i < 3; ++i) {
        gl_Layer = gl_InvocationID;
        gl_Position = uFaceViewProj[gl_InvocationID] * gl_in[i].gl_Position;
        EmitVertex();
    }
    EndPrimitive();
}
```
For cube map arrays the layer is `cubeIndex * 6 + face`.

## When it pays
- Point-light shadow cubes, environment probe capture, cascaded shadow maps into an array,
  voxelisation into 3D textures.
- Saves CPU (one draw instead of six) but every primitive is processed for every layer unless
  you cull per face in the shader; compare against six culled draws by measuring.

## Gotchas
- Clearing a layered FBO clears all layers.
- `gl_Layer` is a built-in input of GLSL 4.60 fragment shaders; it reads 0 if the geometry stage never assigns it, and is
  undefined if the assignment is not on every path.

## Verify
- [ ] Each cube face in RenderDoc shows the right view; one draw call per object instead of six.

## Checked

Date: 2026-10-26. Documentation: OpenGL 4.6 core spec (5 May 2022), GLSL 4.60 spec, ARB_shader_viewport_layer_array extension text. Confirmed: layered attachment rules and `FRAMEBUFFER_INCOMPLETE_LAYER_TARGETS`; layer count limited to the smallest attachment; clearing a layered attachment clears all layers; `gl_Layer = layer*6+face` for cube map arrays; geometry shader `gl_Layer` output and fragment shader `gl_Layer` input in GLSL 4.60; writing `gl_Layer` from the vertex shader needs ARB_shader_viewport_layer_array. Removed: AMD_vertex_shader_layer, OVR_multiview, GS performance claims, the GL 4.3 version claim.

Method: documentation only; no commands were run.
