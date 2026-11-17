---
id: computing-software.computer-graphics-engineering.opengl.vulkan-swapchain-image-count-and-latency
name: vulkan-swapchain-image-count-and-latency
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, vulkan-swapchain, swapchain-image-count, frames-in-flight-tuning, input-latency]
level: advanced
status: docs-checked
description: "Choose Vulkan swapchain minImageCount and frames in flight: the latency/throughput trade-off per present mode, and why images != frames in flight."
sources: ["https://docs.vulkan.org/spec/latest/chapters/VK_KHR_surface/wsi.html", "https://docs.vulkan.org/guide/latest/swapchain_semaphore_reuse.html", "https://docs.vulkan.org/spec/latest/appendices/VK_KHR_present_wait.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Swapchain image count and latency

## Two separate knobs
- **Swapchain images** (`minImageCount`): how many presentable images exist. The presentation
  engine holds some (on screen, queued); you can acquire the rest.
- **Frames in flight** (your per-frame command buffers, fences, uniform slots): how many frames
  the CPU may record ahead of the GPU. Usually 2.
They are independent. Index per-frame resources by frame counter (`frame % FRAMES_IN_FLIGHT`)
and per-image resources (render-finished semaphores, framebuffers) by the acquired image index.

## Choosing minImageCount
```c
VkSurfaceCapabilitiesKHR caps; vkGetPhysicalDeviceSurfaceCapabilitiesKHR(gpu, surface, &caps);
uint32_t count = caps.minImageCount + 1;                  // common default
if (caps.maxImageCount > 0 && count > caps.maxImageCount) count = caps.maxImageCount;  // 0 = no limit
```
The spec says the swapchain contains at least `minImageCount` images, possibly more; always query with `vkGetSwapchainImagesKHR`.

| Mode | Images | Behaviour |
|---|---|---|
| FIFO, 2 images | queue of pending presents, one removed per vertical blank; no tearing; fewer queued frames means less latency but less slack | |
| FIFO, 3 images | more slack for frame-time spikes; each extra queued image can add a frame of latency | common default (measure) |
| MAILBOX | single-entry queue: a new present replaces the pending one; no tearing; the app may render faster than the display refresh | when the extra rendering work is acceptable |
| IMMEDIATE | no wait for vertical blank; tearing may be visible | lowest latency, benchmarks |

The minimum number of images that guarantees forward progress can differ per present mode (the spec's example: FIFO might need 2, MAILBOX 4);
query `VkSurfacePresentModeKHR` with `VK_KHR_surface_maintenance1` / `VK_EXT_surface_maintenance1` when you need per-mode counts.

## Controlling latency
- Latency ~= frames queued between CPU input sampling and scan-out. To cut it without losing
  throughput: sample input as late as possible, keep 2 frames in flight, and use
  `VK_KHR_present_wait` to wait until the previous present was displayed before starting the
  next frame (or vendor low-latency extensions).
- Don't wait on the image-acquire fence *and* the frame fence redundantly; acquire with a
  semaphore, and wait on the frame-in-flight fence before reusing that frame's resources.

## Gotchas
- Using one "render finished" semaphore per frame-in-flight instead of per swapchain image is a
  known validation error (semaphore may still be in use by present). Index those by image.
- With MAILBOX the app is not throttled by the display; cap the frame rate yourself if you need to.
- Changing image count requires swapchain recreation.

## Verify
- [ ] Swapchain image count logged; no `VUID-vkQueueSubmit-pSignalSemaphores` reuse errors; frame time histogram smooth under load spikes.

## Checked
Checked 2026-10-26 against Vulkan 1.4.366 (chapters/VK_KHR_surface/wsi.adoc present-mode definitions and per-present-mode image count note, validusage.json for VkSwapchainCreateInfoKHR, appendices/VK_KHR_present_wait.adoc) and the Vulkan Guide swapchain_semaphore_reuse chapter.
Confirmed: minImageCount and maxImageCount rules (maxImageCount of 0 means no limit; the VUIDs require minImageCount within the reported capabilities); FIFO, MAILBOX and IMMEDIATE definitions; at-least-minImageCount statement; per-present-mode image counts; present-wait extension; present-wait semaphore reuse. Removed Arm tiler guidance, 60-to-30 vsync claim and vendor low-latency product names.
Method: documentation only; no commands were run.
