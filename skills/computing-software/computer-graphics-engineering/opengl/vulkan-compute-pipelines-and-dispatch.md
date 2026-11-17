---
id: computing-software.computer-graphics-engineering.opengl.vulkan-compute-pipelines-and-dispatch
name: vulkan-compute-pipelines-and-dispatch
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, vulkan-pipelines, vulkan-compute-pipeline, vkcmddispatch, compute-shader-vulkan]
level: practitioner
status: docs-checked
description: "Build and run Vulkan compute pipelines: shader stage, layout with storage images/buffers and push constants, dispatch sizing, and barriers around it."
sources: ["https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/dispatch.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/descriptorsets.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/limits.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/appendices/VK_KHR_maintenance5.adoc", "https://github.com/google/shaderc/blob/main/glslc/README.asciidoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compute pipelines and dispatch

## Shader
```glsl
#version 460
layout(local_size_x = 16, local_size_y = 16) in;
layout(set = 0, binding = 0, rgba16f) uniform image2D img;
layout(push_constant) uniform PC { vec4 tint; ivec2 size; } pc;
void main() {
    ivec2 p = ivec2(gl_GlobalInvocationID.xy);
    if (any(greaterThanEqual(p, pc.size))) return;           // partial edge groups
    imageStore(img, p, imageLoad(img, p) * pc.tint);
}
```
Compile: `glslc --target-env=vulkan1.3 tint.comp -o tint.spv` (the `.comp` extension selects the compute stage; `-fshader-stage=compute` overrides the extension).

## Pipeline
```c
VkPushConstantRange pcr = { VK_SHADER_STAGE_COMPUTE_BIT, 0, sizeof(PC) };
VkPipelineLayoutCreateInfo pl = { VK_STRUCTURE_TYPE_PIPELINE_LAYOUT_CREATE_INFO };
pl.setLayoutCount = 1; pl.pSetLayouts = &setLayout; pl.pushConstantRangeCount = 1; pl.pPushConstantRanges = &pcr;
vkCreatePipelineLayout(dev, &pl, NULL, &layout);

VkComputePipelineCreateInfo ci = { VK_STRUCTURE_TYPE_COMPUTE_PIPELINE_CREATE_INFO };
ci.stage = (VkPipelineShaderStageCreateInfo){ VK_STRUCTURE_TYPE_PIPELINE_SHADER_STAGE_CREATE_INFO,
            .stage = VK_SHADER_STAGE_COMPUTE_BIT, .module = module, .pName = "main" };
ci.layout = layout;
vkCreateComputePipelines(dev, pipelineCache, 1, &ci, NULL, &pipe);
```
With `VK_KHR_maintenance5` (core in Vulkan 1.4), pass `VkShaderModuleCreateInfo` in `stage.pNext` and skip the module object.

## Dispatch
```c
vkCmdBindPipeline(cmd, VK_PIPELINE_BIND_POINT_COMPUTE, pipe);
vkCmdBindDescriptorSets(cmd, VK_PIPELINE_BIND_POINT_COMPUTE, layout, 0, 1, &set, 0, NULL);
vkCmdPushConstants(cmd, layout, VK_SHADER_STAGE_COMPUTE_BIT, 0, sizeof(pc), &pc);
vkCmdDispatch(cmd, (w + 15) / 16, (h + 15) / 16, 1);
```
Compute and graphics have separate bind points: binding a compute pipeline does not disturb
graphics state and vice versa, but descriptor sets must be bound per bind point.

## Image layout and barriers
- Storage images must be in `VK_IMAGE_LAYOUT_GENERAL` while written.
- Before: transition from previous use (e.g. `UNDEFINED` or `SHADER_READ_ONLY_OPTIMAL`) to
  `GENERAL`, dst stage `COMPUTE_SHADER`, access `SHADER_STORAGE_READ|WRITE`.
- After: barrier to the consumer (sampling, present via blit, next dispatch).
- Swapchain usage is limited to the surface's `supportedUsageFlags`, and the spec's mandatory-format table gives sRGB RGBA8 no storage-image support; a common pattern is to render into your own
  `RGBA16F` image and blit/copy to the swapchain.

## Gotchas
- `maxComputeWorkGroupCount` is guaranteed to be at least 65535 per dimension; huge 1D dispatches need 2D folding.
- Running compute on the graphics queue between render passes is fine; async compute needs a
  separate queue and semaphores.
- Image format qualifiers (`rgba16f`) must be compatible with the image view format; with the
  `shaderStorageImageReadWithoutFormat` feature enabled, reads can omit the qualifier.

## Verify
- [ ] Validation clean; RenderDoc shows the dispatch with expected group counts and output image contents.

## Checked

2026-10-26: Vulkan-Docs main (latest commit 2026-10-23) and the shaderc glslc README. Confirmed: `maxComputeWorkGroupCount` minimum (65535 per dimension); storage image descriptors need an image view with the identity swizzle and the `STORAGE` usage; VK_KHR_maintenance5 allows `VkShaderModuleCreateInfo` in the stage `pNext` and is promoted to Vulkan 1.4; glslc option names `--target-env=vulkan1.3` and `-fshader-stage=`, with `.comp` selecting the compute stage; the mandatory-format table has no storage-image entry for `R8G8B8A8_SRGB`. Removed the vendor generalisation about swapchain storage support.

Method: documentation only; no commands were run.
