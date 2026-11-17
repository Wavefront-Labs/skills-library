---
id: computing-software.computer-graphics-engineering.opengl.vulkan-subpass-and-external-dependencies
name: vulkan-subpass-and-external-dependencies
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, vulkan-synchronization, subpass-dependencies, vk-subpass-external, render-pass-sync]
level: advanced
status: docs-checked
description: "Write VkSubpassDependency2 correctly for render pass objects: VK_SUBPASS_EXTERNAL in/out, swapchain acquire chains, BY_REGION, and implicit dependencies."
sources: ["https://docs.vulkan.org/spec/latest/chapters/renderpass.html#renderpass-implicit-dependencies", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/renderpass.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/appendices/versions.adoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Subpass and external dependencies

With `VkRenderPass` objects (the way to read attachments in a later subpass before
`dynamic_rendering_local_read`, core in 1.4), synchronisation into, between and out of subpasses is
declared as `VkSubpassDependency2` entries.

## Incoming: wait for swapchain acquire
```c
VkSubpassDependency2 in = { VK_STRUCTURE_TYPE_SUBPASS_DEPENDENCY_2 };
in.srcSubpass = VK_SUBPASS_EXTERNAL; in.dstSubpass = 0;
in.srcStageMask  = VK_PIPELINE_STAGE_COLOR_ATTACHMENT_OUTPUT_BIT | VK_PIPELINE_STAGE_EARLY_FRAGMENT_TESTS_BIT;
in.dstStageMask  = VK_PIPELINE_STAGE_COLOR_ATTACHMENT_OUTPUT_BIT | VK_PIPELINE_STAGE_EARLY_FRAGMENT_TESTS_BIT;
in.srcAccessMask = 0;
in.dstAccessMask = VK_ACCESS_COLOR_ATTACHMENT_WRITE_BIT | VK_ACCESS_DEPTH_STENCIL_ATTACHMENT_WRITE_BIT;
```
The acquire semaphore waits at `COLOR_ATTACHMENT_OUTPUT`; this dependency's src stage matches,
forming a chain, so the `UNDEFINED -> COLOR_ATTACHMENT_OPTIMAL` layout transition (which happens
at the start of the render pass) waits for the image. Including `EARLY_FRAGMENT_TESTS` covers
the depth buffer reuse across frames (WAW on depth).

## Between subpasses (G-buffer -> lighting with input attachments)
```c
VkSubpassDependency2 mid = { VK_STRUCTURE_TYPE_SUBPASS_DEPENDENCY_2 };
mid.srcSubpass = 0; mid.dstSubpass = 1;
mid.srcStageMask  = VK_PIPELINE_STAGE_COLOR_ATTACHMENT_OUTPUT_BIT;
mid.dstStageMask  = VK_PIPELINE_STAGE_FRAGMENT_SHADER_BIT;
mid.srcAccessMask = VK_ACCESS_COLOR_ATTACHMENT_WRITE_BIT;
mid.dstAccessMask = VK_ACCESS_INPUT_ATTACHMENT_READ_BIT;
mid.dependencyFlags = VK_DEPENDENCY_BY_REGION_BIT;         // framebuffer-local dependency
```
`BY_REGION` makes the dependency framebuffer-local instead of framebuffer-global, so implementations
can synchronise per region (this matters most on tile-based GPUs).

## Outgoing: to a later sampling pass or present
```c
VkSubpassDependency2 out = { VK_STRUCTURE_TYPE_SUBPASS_DEPENDENCY_2 };
out.srcSubpass = 0; out.dstSubpass = VK_SUBPASS_EXTERNAL;
out.srcStageMask  = VK_PIPELINE_STAGE_COLOR_ATTACHMENT_OUTPUT_BIT;
out.dstStageMask  = VK_PIPELINE_STAGE_FRAGMENT_SHADER_BIT;      // next pass samples it
out.srcAccessMask = VK_ACCESS_COLOR_ATTACHMENT_WRITE_BIT;
out.dstAccessMask = VK_ACCESS_SHADER_READ_BIT;
```
For present, `finalLayout = PRESENT_SRC_KHR` and the semaphore signal handles visibility;
dst stage `BOTTOM_OF_PIPE`/access 0 is fine.

## Implicit dependencies
If you declare no external dependency, the spec adds an implicit one only when an automatic layout
transition happens (away from `initialLayout`, or into `finalLayout`). The incoming one has
srcStageMask `NONE` (`TOP_OF_PIPE` before synchronization2), dstStageMask `ALL_COMMANDS` and
srcAccessMask 0, so it does not chain with an acquire semaphore waiting at
`COLOR_ATTACHMENT_OUTPUT`. The outgoing one is `ALL_COMMANDS` to `NONE` (`BOTTOM_OF_PIPE`) with
dstAccessMask 0. Declare both external dependencies explicitly.

## Verify
- [ ] Sync validation clean for the declared external and between-subpass dependencies.

## Checked

- Date: 2026-10-25. Documentation release: Vulkan specification 1.4.366 (Vulkan-Docs main, commit a8b088a, 2026-10-23), including the generated vk.xml registry.
- Confirmed: Implicit external dependencies (render pass chapter): they exist only with an automatic layout transition; incoming is srcStage `NONE` (`TOP_OF_PIPE` before sync2) / dstStage `ALL_COMMANDS` / srcAccess 0 / dstAccess input, colour and depth/stencil attachment read and write; outgoing is `ALL_COMMANDS` to `NONE` (`BOTTOM_OF_PIPE`) with srcAccess colour and depth/stencil write and dstAccess 0.
- Confirmed: `VkSubpassDependency2` members match vk.xml; `VK_KHR_dynamic_rendering_local_read` is promoted to 1.4 (versions appendix). `TOP_OF_PIPE` in a first scope equals `NONE`.
- Removed tile-GPU flush and profiler remarks (no source found); BY_REGION is described only as framebuffer-local.

Method: documentation only; no commands were run.
