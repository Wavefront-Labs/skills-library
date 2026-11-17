---
id: computing-software.computer-graphics-engineering.opengl.vulkan-multiview-rendering
name: vulkan-multiview-rendering
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, vulkan-pipelines, vk-multiview, gl-viewindex, stereo-rendering-vulkan]
level: advanced
status: docs-checked
description: "Render stereo or cube faces in one pass with Vulkan multiview: viewMask in dynamic rendering or render passes, gl_ViewIndex, layered targets and limits."
sources: ["https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/renderpass.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/queries.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/limits.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/VK_KHR_surface/wsi.adoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multiview rendering (core 1.1)

Multiview broadcasts each draw to several layers of the attachments; the shader receives
`gl_ViewIndex` to choose per-view matrices. Implementations may share work between
views, which can be cheaper than drawing once per view.

## Dynamic rendering
```c
VkRenderingInfo ri = { VK_STRUCTURE_TYPE_RENDERING_INFO };
ri.viewMask = 0b11;              // views 0 and 1 -> layers 0 and 1 of each attachment
```
`layerCount` must be non-zero only when `viewMask` is 0. With a non-zero `viewMask`, each attachment
image view must have a layer count greater than the index of the most significant bit of `viewMask`. The pipeline must declare the same mask:
```c
VkPipelineRenderingCreateInfo prci = { VK_STRUCTURE_TYPE_PIPELINE_RENDERING_CREATE_INFO };
prci.viewMask = 0b11; prci.colorAttachmentCount = 1; prci.pColorAttachmentFormats = &fmt;
```
With render pass objects use `VkRenderPassMultiviewCreateInfo` (per-subpass view masks and
correlation masks) or `VkSubpassDescription2::viewMask`.

## Shader
```glsl
#version 460
#extension GL_EXT_multiview : require
layout(set = 0, binding = 0) uniform Views { mat4 viewProj[2]; };
void main() { gl_Position = viewProj[gl_ViewIndex] * uModel * vec4(aPos, 1); }
```

## Correlation mask
`VkRenderPassMultiviewCreateInfo::pCorrelationMasks` hints that views are spatially close
(stereo eyes), which can make rendering them concurrently more efficient; correlation masks must
not change the results. `VkRenderingInfo` has no correlation mask field.

## Uses beyond VR
- Cube map shadow/probe rendering (6 views; `maxMultiviewViewCount` is guaranteed to be at least 6).
- Cascaded shadow maps into an array.

## Gotchas
- Features: `multiview`, plus `multiviewGeometryShader` / `multiviewTessellationShader` if
  those stages are used.
- Queries inside a multiview pass consume N consecutive queries (one per view).
- `VkSwapchainCreateInfoKHR::imageArrayLayers` is 1 for non-stereoscopic applications, so render
  multiview output to your own array image and copy or compose it afterwards.
- Per-view frustum culling must use the union frustum when sharing one draw list.

## Verify
- [ ] A capture tool shows both layers filled from one draw; compare GPU time with drawing each view separately.

## Checked

- Date: 2026-10-25. Documentation release: Vulkan specification 1.4.366 (Vulkan-Docs main, commit a8b088a, 2026-10-23), including the generated vk.xml registry.
- Confirmed: VkRenderingInfo valid usage: `layerCount` must not be 0 only if `viewMask` is 0; with a non-zero `viewMask` attachment views need a layer count above the most significant mask bit; correlation masks must not have a functional effect (render pass chapter).
- Confirmed: Queries in a multiview subpass use N consecutive indices and must not span subpasses; `maxMultiviewViewCount` minimum is 6 (limits table); `imageArrayLayers` is 1 for non-stereoscopic applications; multiview is promoted to 1.1.
- Removed HLSL, mobile and OpenXR remarks (no source found).

Method: documentation only; no commands were run.
