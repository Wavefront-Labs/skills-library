---
id: computing-software.computer-graphics-engineering.opengl.vulkan-image-layout-transitions
name: vulkan-image-layout-transitions
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, vulkan, vulkan-synchronization, image-layout-transitions, vkimagememorybarrier2, synchronization2, layout-tracking, render-graph, attachment-optimal]
level: advanced
status: docs-checked
description: "Get Vulkan image layout transitions right: the common transition table with stage/access masks, per-subresource state tracking, and when GENERAL or UNDEFINED is the answer."
sources: ["https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/synchronization.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/commonvalidity/image_layout_transition_common.adoc", "https://github.com/KhronosGroup/Vulkan-Guide/blob/main/chapters/synchronization_examples.adoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vulkan image layout transitions

**Goal:** each image is in the right layout for each use, with the narrowest correct
stage/access masks, and the engine — not each call site — tracks current state.

## 1. Transition helper (sync2)
```cpp
void transition(VkCommandBuffer cmd, VkImage img, VkImageAspectFlags aspect,
                ImgState from, ImgState to, uint32_t mip0 = 0, uint32_t mips = VK_REMAINING_MIP_LEVELS) {
    VkImageMemoryBarrier2 b{VK_STRUCTURE_TYPE_IMAGE_MEMORY_BARRIER_2};
    b.srcStageMask = from.stage; b.srcAccessMask = from.access; b.oldLayout = from.layout;
    b.dstStageMask = to.stage;   b.dstAccessMask = to.access;   b.newLayout = to.layout;
    b.image = img; b.subresourceRange = {aspect, mip0, mips, 0, VK_REMAINING_ARRAY_LAYERS};
    VkDependencyInfo d{VK_STRUCTURE_TYPE_DEPENDENCY_INFO}; d.imageMemoryBarrierCount = 1; d.pImageMemoryBarriers = &b;
    vkCmdPipelineBarrier2(cmd, &d);
}
```

## 2. The table you actually need
| use | layout | stage | access |
|---|---|---|---|
| discard / first use | `UNDEFINED` | `NONE` (`TOP_OF_PIPE`) | 0 |
| upload destination | `TRANSFER_DST_OPTIMAL` | `COPY` | `TRANSFER_WRITE` |
| sampled in FS | `SHADER_READ_ONLY_OPTIMAL` | `FRAGMENT_SHADER` | `SHADER_SAMPLED_READ` |
| colour target | `COLOR_ATTACHMENT_OPTIMAL` | `COLOR_ATTACHMENT_OUTPUT` | `COLOR_ATTACHMENT_WRITE` (+READ if blending/LOAD) |
| depth target | `DEPTH_ATTACHMENT_OPTIMAL` | `EARLY_FRAGMENT_TESTS` and `LATE_FRAGMENT_TESTS` | `DEPTH_STENCIL_ATTACHMENT_READ` and `_WRITE` |
| depth read-only + sampled | `DEPTH_READ_ONLY_OPTIMAL` | tests + FS | read |
| compute storage image | `GENERAL` | `COMPUTE_SHADER` | `SHADER_STORAGE_READ` and `_WRITE` |
| present | `PRESENT_SRC_KHR` | `NONE`/`BOTTOM` (dst) | 0 |
With sync2 / 1.3 you may use the generic `ATTACHMENT_OPTIMAL` and `READ_ONLY_OPTIMAL`.

## 3. Track state per image (per subresource when needed)
Store `{layout, stage, access}` with each image; `use(img, newState)` emits a barrier only
when needed and updates the record. Mip-chain generation and per-layer rendering (cube
shadow faces) need per-mip/per-layer tracking. A render graph computes all of this per
frame from declared pass inputs/outputs.

## 4. UNDEFINED is a feature
Transition from `UNDEFINED` when you will overwrite everything (G-buffer each frame,
swapchain image): it tells the implementation the contents may be discarded, which the spec
notes can provide performance or power benefits.

## Gotchas
- Transitioning from `UNDEFINED` an image you meant to keep (accumulation/history buffer)
  lets the implementation discard its contents.
- Prefer the specific optimal layout for attachments and sampled images; use `GENERAL`
  mainly for storage images.
- Read-after-read needs no barrier — but a layout change does, even read→read.
- Depth aspect: combined depth/stencil formats need `DEPTH|STENCIL` aspect in the range
  unless `separateDepthStencilLayouts` is used.

## Verify
- [ ] Validation (with sync validation) silent across all passes.
- [ ] A capture tool shows the expected layout at each event.
- [ ] Removing one transition triggers a validation error (the tracker isn't masking bugs).

## Checked

- Date: 2026-10-25. Documentation release: Vulkan specification 1.4.366 (Vulkan-Docs main, commit a8b088a, 2026-10-23), including the generated vk.xml registry.
- Confirmed: Old layout must be `UNDEFINED` or the current layout; `UNDEFINED` lets contents be discarded (spec note: performance or power benefit). Layout transitions are potentially read/write operations, so a layout change needs dependencies even for read-to-read.
- Confirmed: Combined depth/stencil images need both aspects in a barrier range unless `separateDepthStencilLayouts` is enabled (common validity for image layout transitions); that feature is in `VkPhysicalDeviceVulkan12Features`.
- Confirmed: `TOP_OF_PIPE` equals `NONE` in a first scope. Removed compression and GPU-specific claims; fixed table cells that contained pipe characters.

Method: documentation only; no commands were run.
