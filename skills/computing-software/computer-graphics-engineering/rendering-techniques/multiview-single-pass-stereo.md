---
id: computing-software.computer-graphics-engineering.rendering-techniques.multiview-single-pass-stereo
name: multiview-single-pass-stereo
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, vr-rendering, xr-rendering, multiview, single-pass-stereo, vk-khr-multiview, ovr-multiview2, gl-viewindex, stereo-instancing, view-instancing]
level: advanced
status: docs-checked
description: "Render both VR eyes in one pass with multiview (Vulkan VK_KHR_multiview, GL OVR_multiview2, D3D12 view instancing): per-view matrices via gl_ViewIndex, array targets."
sources: ["https://docs.vulkan.org/spec/latest/chapters/renderpass.html", "https://registry.khronos.org/OpenGL/extensions/OVR/OVR_multiview2.txt", "https://registry.khronos.org/OpenGL/extensions/OVR/OVR_multiview.txt", "https://microsoft.github.io/DirectX-Specs/d3d/ViewInstancing.html", "https://github.com/KhronosGroup/GLSL/blob/main/extensions/ext/GL_EXT_multiview.txt"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multiview single-pass stereo

**Goal:** halve CPU draw submission and share vertex work between eyes by broadcasting
each draw to both layers of an array render target.

## 1. Vulkan
```cpp
// dynamic rendering (1.3): layered attachments + view mask
VkRenderingInfo ri{VK_STRUCTURE_TYPE_RENDERING_INFO};
ri.viewMask = 0b11;                                  // views 0 and 1
// layerCount is only used when viewMask == 0; with a mask, attachment views need layerCount > highest set bit of viewMask
// attachments: image views of type 2D_ARRAY with at least 2 layers
// pipeline: VkPipelineRenderingCreateInfo::viewMask = 0b11
```
Enable the `multiview` feature (`VkPhysicalDeviceMultiviewFeatures`, Vulkan 1.1); `VkRenderingInfo` needs Vulkan 1.3 or dynamic rendering. With render passes: `VkRenderPassMultiviewCreateInfo`.
```glsl
#extension GL_EXT_multiview : require
layout(set = 0, binding = 0) uniform Views { mat4 viewProj[2]; vec4 eyePos[2]; };
void main() { gl_Position = viewProj[gl_ViewIndex] * model * vec4(pos, 1.0); }
```

## 2. OpenGL ES / WebGL (OVR_multiview2)
```glsl
#extension GL_OVR_multiview2 : require
layout(num_views = 2) in;
gl_Position = uViewProj[gl_ViewID_OVR] * worldPos;
```
Framebuffer: `glFramebufferTextureMultiviewOVR(GL_DRAW_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, tex, 0, 0, 2)`
on a 2-layer `GL_TEXTURE_2D_ARRAY` (signature: target, attachment, texture, level, baseViewIndex, numViews). Enabling `GL_OVR_multiview2` implicitly enables `GL_OVR_multiview`.

## 3. D3D12 view instancing
`D3D12_VIEW_INSTANCING_DESC` in the PSO with view locations (render target array index per
view); shaders read `SV_ViewID`. Hardware tier affects behaviour, so check the view instancing tier.

## 4. What changes in the engine
- **Culling**: cull against the union frustum of both eyes (one cull, both views).
- **LOD**: select per object once for both eyes (centre eye) to avoid eye-mismatched LODs.
- **Post-processing / compute**: operate on array textures (dispatch z = view) or per layer.
- Shadow maps are shared between eyes — never render them per eye.
- Per-view data must index by view ID everywhere: camera position for specular/fog, previous
  view-projection for motion vectors (TAA in VR).

## Gotchas
- With `OVR_multiview` only `gl_Position` may depend on `gl_ViewID_OVR`; `OVR_multiview2` removes that restriction. In Vulkan
  `multiviewGeometryShader` and `multiviewTessellationShader` are optional features.
- Screen-space effects that read neighbouring pixels must stay within one layer.

## Verify
- [ ] CPU draw calls halved vs two-pass stereo; GPU vertex work reduced.
- [ ] Stereo image pair correct (no swapped eyes; specular highlights differ correctly per eye).
- [ ] Motion vectors per eye validated (no TAA smearing in VR).

## Checked

2026-10-26: Vulkan-Docs chapters (renderpass.adoc, features.adoc, vk.xml, main as of 2026-10-23), OVR_multiview and OVR_multiview2 extension text from the OpenGL registry, GL_EXT_multiview (GLSL repository) and the DirectX-Specs ViewInstancing.md. Confirmed: VkRenderingInfo.layerCount applies only when viewMask is 0 (so the earlier must-be-0 claim was wrong and was replaced by the attachment layerCount rule), VkPipelineRenderingCreateInfo.viewMask, multiviewGeometryShader and multiviewTessellationShader feature fields, gl_ViewIndex in GL_EXT_multiview, FramebufferTextureMultiviewOVR parameters, the OVR_multiview2 relaxation of the gl_Position-only rule, D3D12_VIEW_INSTANCING_DESC and SV_ViewID. Removed the Three.js/WebXR auto-enable and RenderDoc claims.

Method: documentation only; no commands were run.
