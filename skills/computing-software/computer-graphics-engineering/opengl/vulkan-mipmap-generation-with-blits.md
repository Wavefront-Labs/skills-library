---
id: computing-software.computer-graphics-engineering.opengl.vulkan-mipmap-generation-with-blits
name: vulkan-mipmap-generation-with-blits
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, vulkan, vulkan-images, vulkan-textures, mipmap-generation, vkcmdblitimage, format-properties, format-support, linear-filter-blit, compute-downsample]
level: practitioner
status: docs-checked
description: "Generate Vulkan mip chains at runtime with vkCmdBlitImage: format feature checks, per-level barriers, and when to use a compute downsampler or offline mips instead."
sources: ["https://docs.vulkan.org/spec/latest/chapters/copies.html#copies-imagescaling", "https://docs.vulkan.org/spec/latest/chapters/formats.html#formats-properties", "https://docs.vulkan.org/refpages/latest/refpages/source/vkCmdBlitImage2.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vulkan mipmap generation with blits

**Goal:** a full, correctly filtered mip chain for runtime-created textures (render
targets, procedurally generated, uncompressed loads).

## 1. Check the format can be blitted with filtering
```cpp
VkFormatProperties fp; vkGetPhysicalDeviceFormatProperties(gpu, fmt, &fp);
bool ok = (fp.optimalTilingFeatures & VK_FORMAT_FEATURE_BLIT_SRC_BIT) &&
          (fp.optimalTilingFeatures & VK_FORMAT_FEATURE_BLIT_DST_BIT) &&
          (fp.optimalTilingFeatures & VK_FORMAT_FEATURE_SAMPLED_IMAGE_FILTER_LINEAR_BIT);
```
Block-compressed formats (BC/ASTC/ETC) are not normally blit destinations (check `BLIT_DST_BIT`) → mips must come offline.
The spec requires `SAMPLED_IMAGE_FILTER_LINEAR_BIT` on the source format for `VK_FILTER_LINEAR`, and a signed or unsigned integer format
can only be blitted to the same integer kind, so integer formats use `VK_FILTER_NEAREST`. Use `vkGetPhysicalDeviceFormatProperties2`
with `VkFormatProperties3` for the 64-bit feature flags on 1.3.

## 2. Create with all levels and both usages
`mipLevels = floor(log2(max(w,h))) + 1`, `usage = SAMPLED | TRANSFER_SRC | TRANSFER_DST`.

## 3. The loop
```cpp
// level 0 is in TRANSFER_DST_OPTIMAL after the upload
int32_t mw = w, mh = h;
for (uint32_t i = 1; i < levels; ++i) {
    barrierMip(cmd, img, i - 1, TRANSFER_DST_OPTIMAL, TRANSFER_SRC_OPTIMAL,
               /*src*/ COPY, TRANSFER_WRITE, /*dst*/ BLIT, TRANSFER_READ);
    VkImageBlit2 b{VK_STRUCTURE_TYPE_IMAGE_BLIT_2};
    b.srcSubresource = {VK_IMAGE_ASPECT_COLOR_BIT, i - 1, 0, 1};
    b.srcOffsets[1]  = {mw, mh, 1};
    b.dstSubresource = {VK_IMAGE_ASPECT_COLOR_BIT, i, 0, 1};
    b.dstOffsets[1]  = {std::max(mw / 2, 1), std::max(mh / 2, 1), 1};
    VkBlitImageInfo2 bi{VK_STRUCTURE_TYPE_BLIT_IMAGE_INFO_2};
    bi.srcImage = img; bi.srcImageLayout = VK_IMAGE_LAYOUT_TRANSFER_SRC_OPTIMAL;
    bi.dstImage = img; bi.dstImageLayout = VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL;
    bi.regionCount = 1; bi.pRegions = &b; bi.filter = VK_FILTER_LINEAR;
    vkCmdBlitImage2(cmd, &bi);
    barrierMip(cmd, img, i - 1, TRANSFER_SRC_OPTIMAL, SHADER_READ_ONLY_OPTIMAL, BLIT, TRANSFER_READ,
               FRAGMENT_SHADER, SHADER_SAMPLED_READ);
    mw = std::max(mw / 2, 1); mh = std::max(mh / 2, 1);
}
barrierMip(cmd, img, levels - 1, TRANSFER_DST_OPTIMAL, SHADER_READ_ONLY_OPTIMAL, ...);
```
Each level needs its own barrier because levels are in different layouts mid-loop.

## 4. Better options
- **Offline mips** (KTX2 via toktx/Basis) for asset textures: higher quality filters
  (Kaiser/Lanczos), gamma-correct, and compressed.
- **Compute downsampler** for per-frame chains (Hi-Z depth pyramids, bloom): supports min/max
  reductions that blits cannot do (blits on depth/stencil must use `VK_FILTER_NEAREST`).
- `vkCmdBlitImage2` requires a command pool that supports `VK_QUEUE_GRAPHICS_BIT` (not transfer-only queues).

## Gotchas
- Non-power-of-two sizes: the `max(...,1)` clamps matter; each level is `max(size / 2, 1)`.
- sRGB formats: the spec converts sRGB source values to linear for filtering and re-encodes on write to an sRGB destination.

## Verify
- [ ] RenderDoc shows every mip level populated (no black/garbage tail levels).
- [ ] Format without linear blit support takes the compute or offline path.
- [ ] Validation clean through the loop.

## Checked
Checked 2026-10-26 against Vulkan 1.4.366 (validusage.json for vkCmdBlitImage/vkCmdBlitImage2, chapters/formats.adoc, chapters/copies.adoc).
Confirmed: BLIT_SRC/BLIT_DST format features; LINEAR filter requires SAMPLED_IMAGE_FILTER_LINEAR_BIT; integer-format blit rule; depth/stencil blits need NEAREST; blit requires a graphics-capable pool; sRGB conversion in blits; VkFormatProperties3 exists. Removed the unverified FidelityFX SPD and odd-size filter claims; the blit loop itself was not re-derived beyond these rules.
Method: documentation only; no commands were run.
