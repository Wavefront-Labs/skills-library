---
id: computing-software.computer-graphics-engineering.opengl.vulkan-shader-objects
name: vulkan-shader-objects
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, vk-pipelines, shader-objects, vk-ext-shader-object, dynamic-state, pipeline-explosion]
level: advanced
status: docs-checked
description: "Replace Vulkan pipelines with VK_EXT_shader_object: create linked or unlinked shaders, set all state dynamically, layer support and performance trade-offs."
sources: ["https://github.com/KhronosGroup/Vulkan-Docs/blob/main/proposals/VK_EXT_shader_object.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/appendices/VK_EXT_shader_object.adoc", "https://github.com/KhronosGroup/Vulkan-ExtensionLayer/blob/main/docs/shader_object_layer.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shader objects (VK_EXT_shader_object)

**Goal:** bind individual shader stages and set all fixed-function state at record time,
like GL/D3D11, instead of baking thousands of `VkPipeline` permutations.

## 1. Create
```cpp
VkShaderCreateInfoEXT ci[2]{};
ci[0] = {VK_STRUCTURE_TYPE_SHADER_CREATE_INFO_EXT}; ci[0].stage = VK_SHADER_STAGE_VERTEX_BIT;
ci[0].nextStage = VK_SHADER_STAGE_FRAGMENT_BIT; ci[0].codeType = VK_SHADER_CODE_TYPE_SPIRV_EXT;
ci[0].pCode = vsSpv; ci[0].codeSize = vsSize; ci[0].pName = "main";
ci[0].setLayoutCount = 1; ci[0].pSetLayouts = &setLayout;          // same layouts as a pipeline
ci[0].flags = VK_SHADER_CREATE_LINK_STAGE_BIT_EXT;                  // linked = better codegen
ci[1] = ci[0]; ci[1].stage = VK_SHADER_STAGE_FRAGMENT_BIT; ci[1].nextStage = 0; /* fs code */
VkShaderEXT sh[2]; vkCreateShadersEXT(dev, 2, ci, nullptr, sh);
```
Shaders are linked only when created in one `vkCreateShadersEXT` call (count above one) with the LINK flag
in every create info. Unlinked shaders can be mixed freely; if any bound shader was linked, all shaders
linked with it must be bound.
`vkGetShaderBinaryDataEXT` gives a cacheable binary (codeType `BINARY_EXT`).

## 2. Record
```cpp
VkShaderStageFlagBits st[2] = {VK_SHADER_STAGE_VERTEX_BIT, VK_SHADER_STAGE_FRAGMENT_BIT};
vkCmdBindShadersEXT(cmd, 2, st, sh);
// Most fixed-function state must be set dynamically before drawing, for example:
vkCmdSetViewportWithCount, vkCmdSetScissorWithCount, vkCmdSetRasterizerDiscardEnable,
vkCmdSetPolygonModeEXT, vkCmdSetCullMode, vkCmdSetFrontFace, vkCmdSetDepthTestEnable,
vkCmdSetDepthWriteEnable, vkCmdSetDepthCompareOp, vkCmdSetPrimitiveTopology,
vkCmdSetVertexInputEXT, vkCmdSetColorBlendEnableEXT, vkCmdSetColorWriteMaskEXT,
vkCmdSetRasterizationSamplesEXT, vkCmdSetSampleMaskEXT, vkCmdSetAlphaToCoverageEnableEXT ...
```
Binding `VK_NULL_HANDLE` for a stage unbinds it. The extension depends on dynamic rendering (no
render pass objects).

## 3. When to use
Good for tools, emulators, ports from GL/D3D11 and engines with permutation explosions.
Linked shaders may perform anywhere from the same as to substantially better than unlinked ones, and
the flexibility versus compile-time-state trade-off is left to the application, so measure. Where
the driver lacks it, the Khronos extension layer `VK_LAYER_KHRONOS_shader_object` implements the
extension (it needs `VK_KHR_maintenance2` and `VK_KHR_dynamic_rendering`, and is not implemented for Android).

## Gotchas
- Every state the extension lists as dynamic must be set before drawing; omitting one is invalid usage.
- The union of descriptor set layouts and push constant ranges across all bound shaders must not
  conflict, and stage interfaces must be compatible; the implementation does no draw-time check.
- Check `shaderObject` feature in `VkPhysicalDeviceShaderObjectFeaturesEXT` and enable it.

## Verify
- [ ] Validation clean with all draws; a capture tool shows the bound shader objects per draw.
- [ ] Hitch-free first use of new state combinations (no pipeline compile spikes).

## Checked

- Date: 2026-10-25. Documentation release: Vulkan specification 1.4.366 (Vulkan-Docs main, commit a8b088a, 2026-10-23), including the generated vk.xml registry.
- Confirmed: From the VK_EXT_shader_object proposal: linking requires one `vkCreateShadersEXT` call with the LINK flag, linked shaders must be bound together, `VK_NULL_HANDLE` unbinds a stage, most state must be set with dynamic-state commands, and the application is responsible for interface and layout compatibility.
- Confirmed: vk.xml: the extension depends on `VK_KHR_dynamic_rendering` (or 1.3); `VkShaderCreateInfoEXT` members (`flags`, `stage`, `nextStage`, `codeType`, `codeSize`, `pCode`, `pName`, `setLayoutCount`, ...) match the example. Extension-layer requirements read from the LunarG layer document.
- Removed vendor parity and mobile remarks (no source found).

Method: documentation only; no commands were run.
