---
id: computing-software.computer-graphics-engineering.opengl.vulkan-clearing-images-and-attachments
name: vulkan-clearing-images-and-attachments
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, vulkan-images, vkcmdclearcolorimage, clear-attachments, load-op-clear]
level: practitioner
status: docs-checked
description: "Clear Vulkan images the cheap way: loadOp CLEAR first, vkCmdClearAttachments inside passes, vkCmdClearColorImage outside, and fast-clear value rules."
sources: ["https://docs.vulkan.org/spec/latest/chapters/clears.html", "https://docs.vulkan.org/refpages/latest/refpages/source/vkCmdClearAttachments.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Clearing images and attachments

## Three ways, in order of preference
1. **`loadOp = VK_ATTACHMENT_LOAD_OP_CLEAR`** at the start of rendering. The clear is part of the
   render pass or rendering scope itself, so no separate clear command or pipeline stage is needed.
2. **`vkCmdClearAttachments`** inside a rendering scope: clears rectangles of bound attachments
   (e.g. a viewport region in split-screen, or clearing depth between UI layers).
   ```c
   VkClearAttachment ca = { VK_IMAGE_ASPECT_DEPTH_BIT, 0, { .depthStencil = { 0.0f, 0 } } };
   VkClearRect r = { {{0,0}, extent}, 0, 1 };
   vkCmdClearAttachments(cmd, 1, &ca, 1, &r);
   ```
   Use it for mid-pass clears, not as a substitute for loadOp. The rectangles must lie inside the render area and the command is only valid inside a render pass instance.
3. **`vkCmdClearColorImage` / `vkCmdClearDepthStencilImage`** outside rendering: transfer-stage
   operation for images not used as attachments (storage images, LUTs, history buffers).
   Image must be in `TRANSFER_DST_OPTIMAL`, `GENERAL` (or `SHARED_PRESENT_KHR` for color clears; depth/stencil clears accept only the first two), created with `TRANSFER_DST` usage.
   ```c
   VkClearColorValue zero = {{0,0,0,0}};
   VkImageSubresourceRange all = { VK_IMAGE_ASPECT_COLOR_BIT, 0, VK_REMAINING_MIP_LEVELS, 0, VK_REMAINING_ARRAY_LAYERS };
   vkCmdClearColorImage(cmd, img, VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL, &zero, 1, &all);
   ```
   Barrier: dst stage `CLEAR` (sync2 `VK_PIPELINE_STAGE_2_CLEAR_BIT`), access `TRANSFER_WRITE`.

## Don't clear at all when you can
- `loadOp = DONT_CARE` when every pixel will be overwritten (full-screen passes, sky-covered
  G-buffers): the previous contents become undefined, so the implementation need not load them.
- Depth: use `CLEAR` unless a full-screen depth write follows.
- Storage buffers: `vkCmdFillBuffer` (offset/size multiple of 4) instead of clearing via shaders.

## Clear values and performance
Which clear values are cheapest is vendor-specific and not defined by the Vulkan specification; check the vendor's performance guide for your target GPUs.

## Gotchas
- Integer formats use `.uint32`/`.int32` members of `VkClearColorValue`; floating-point and normalised formats use `.float32`.
- Float clear values are treated as linear for sRGB images: clearing with 0.5 stores the sRGB encoding of linear 0.5 (about 188 of 255).
- `vkCmdClearAttachments` rectangles must be within the render area and have non-zero extent and layer count.

## Verify
- [ ] GPU trace shows no separate clear commands for attachments that could use loadOp CLEAR; validation clean.

## Checked
Checked 2026-10-26 against Vulkan 1.4.366 (validusage.json, chapters/clears.adoc, chapters/synchronization.adoc).
Confirmed: vkCmdClearColorImage layout rule and TRANSFER_DST usage; vkCmdClearDepthStencilImage layouts; vkCmdClearAttachments render-area, extent and layerCount rules and render-pass-only; float clear values linear for sRGB; PIPELINE_STAGE_2_CLEAR_BIT. Removed vendor fast-clear value lists and tiler/desktop performance claims no specification covers.
Method: documentation only; no commands were run.
