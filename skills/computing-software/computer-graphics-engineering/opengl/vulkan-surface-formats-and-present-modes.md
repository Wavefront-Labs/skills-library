---
id: computing-software.computer-graphics-engineering.opengl.vulkan-surface-formats-and-present-modes
name: vulkan-surface-formats-and-present-modes
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, vulkan, vulkan-swapchain, wsi, present-modes, surface-format, mailbox, fifo, immediate, vsync, minimagecount, srgb-swapchain]
level: practitioner
status: docs-checked
description: "Choose a Vulkan swapchain surface format, colour space, present mode and image count for vsync, low latency or uncapped benchmarking, with sRGB handled correctly."
sources: ["https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/VK_KHR_surface/wsi.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/appendices/VK_KHR_swapchain.adoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vulkan surface formats and present modes

**Goal:** a swapchain configuration chosen on purpose: correct colour, the latency/tearing
behaviour the user selected, and no wasted memory.

## 1. Surface format
```cpp
vkGetPhysicalDeviceSurfaceFormatsKHR(gpu, surface, &n, fmts);
// prefer an sRGB format so the hardware encodes on write
for (auto& f : fmts)
  if ((f.format == VK_FORMAT_B8G8R8A8_SRGB || f.format == VK_FORMAT_R8G8B8A8_SRGB) &&
      f.colorSpace == VK_COLOR_SPACE_SRGB_NONLINEAR_KHR) return f;
return fmts[0];
```
- `_SRGB` swapchain: shaders output **linear** values; hardware applies the sRGB curve.
- `_UNORM` swapchain: you must apply the sRGB OETF yourself in the final pass (common when
  the last pass is a compute shader — sRGB formats have no mandatory storage-image support).
  Doing both = washed-out image; neither = too dark.

## 2. Present mode
| mode | behaviour | use |
|---|---|---|
| `FIFO` | vsync, queue of images; **always supported** | default, mobile (power) |
| `FIFO_RELAXED` | vsync but tears if late | variable-load games |
| `MAILBOX` | vsync, newest image replaces queued one; no tearing | desktop "fast vsync" |
| `IMMEDIATE` | no vsync, tears | benchmarks, competitive low-latency |
Query with `vkGetPhysicalDeviceSurfacePresentModesKHR` and fall back to FIFO. Expose as a
user setting rather than hard-coding MAILBOX (it renders frames that are never shown →
power/heat on laptops).

## 3. Image count and extent
```cpp
VkSurfaceCapabilitiesKHR caps; vkGetPhysicalDeviceSurfaceCapabilitiesKHR(gpu, surface, &caps);
uint32_t count = caps.minImageCount + 1;
if (caps.maxImageCount && count > caps.maxImageCount) count = caps.maxImageCount;  // 0 = no max
VkExtent2D ext = caps.currentExtent.width != UINT32_MAX ? caps.currentExtent
               : clamp(framebufferSize, caps.minImageExtent, caps.maxImageExtent);
```
`minImageCount + 1` is a common choice: the spec says `vkAcquireNextImageKHR` is only guaranteed to return in finite time while the application holds at
most `imageCount - minImageCount` acquired images, so `imageCount == minImageCount` leaves no spare image.
`currentExtent` of (`0xFFFFFFFF`, `0xFFFFFFFF`) means "you choose" (the spec names Wayland and Fuchsia as examples).

## 4. Other create-info fields
- `imageUsage`: add `TRANSFER_DST` (blit to swapchain) or `STORAGE` (compute writes) only
  if supported in `caps.supportedUsageFlags`.
- `preTransform = caps.currentTransform`; if it differs, the presentation engine transforms the image as part of presentation.
- `compositeAlpha`: OPAQUE unless you need a transparent window.
- `oldSwapchain` when recreating, to allow resource reuse.

## Gotchas
- Number of swapchain images ≠ frames in flight; size per-frame resources by frames in
  flight, per-image resources (renderFinished semaphores) by image count.
- Only `FIFO` is guaranteed to be supported; query the other modes and fall back.

## Verify
- [ ] Colour of a known sRGB test image matches an image viewer exactly.
- [ ] Each present-mode setting shows the expected tearing/latency behaviour.
- [ ] Startup log prints chosen format, colour space, present mode and image count.

## Checked

2026-10-26: Vulkan-Docs main (latest commit 2026-10-23), `chapters/VK_KHR_surface/wsi.adoc`. Confirmed: FIFO is the only required present mode; MAILBOX uses a single-entry queue where a new request replaces the queued one, with no tearing; FIFO_RELAXED may tear if a vertical blank was missed; IMMEDIATE may tear; `currentExtent` is (0xFFFFFFFF, 0xFFFFFFFF) on Wayland and Fuchsia and means the swapchain extent decides; the acquire forward-progress rule uses `imageCount - minImageCount`; `preTransform` differing from `currentTransform` makes the presentation engine transform the image; `VK_COLOR_SPACE_SRGB_NONLINEAR_KHR` exists. Removed the unsourced MAILBOX 'lower latency' and 'needs at least 3 images' claims and the Android and Wayland availability claims.

Method: documentation only; no commands were run.
