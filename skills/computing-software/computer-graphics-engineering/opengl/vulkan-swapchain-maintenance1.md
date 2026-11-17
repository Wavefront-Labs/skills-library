---
id: computing-software.computer-graphics-engineering.opengl.vulkan-swapchain-maintenance1
name: vulkan-swapchain-maintenance1
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, vulkan-swapchain, swapchain-maintenance1, present-fence, present-mode-switching]
level: advanced
status: docs-checked
description: "Use VK_EXT_swapchain_maintenance1 to know when present semaphores are free (present fences), switch present modes without recreation, and release images."
sources: ["https://github.com/KhronosGroup/Vulkan-Docs/blob/main/appendices/VK_KHR_swapchain_maintenance1.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/appendices/VK_EXT_swapchain_maintenance1.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/VK_KHR_surface/wsi.adoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VK_EXT_swapchain_maintenance1

Adds window-system features left out of the original swapchain extension. It is promoted to
`VK_KHR_swapchain_maintenance1` (which needs `VK_KHR_surface_maintenance1`); the EXT version requires
`VK_EXT_surface_maintenance1` at instance level.

## 1. Present fences: know when present resources are free
Core Vulkan has no way to know when the semaphore waited on by `vkQueuePresentKHR` can be
reused or when an old swapchain can be destroyed. Attach a fence to each present:
```c
VkSwapchainPresentFenceInfoEXT pf = { VK_STRUCTURE_TYPE_SWAPCHAIN_PRESENT_FENCE_INFO_EXT };
pf.swapchainCount = 1; pf.pFences = &presentFence[imageIndex];
VkPresentInfoKHR pi = { VK_STRUCTURE_TYPE_PRESENT_INFO_KHR, &pf };
pi.waitSemaphoreCount = 1; pi.pWaitSemaphores = &renderDone[imageIndex];
pi.swapchainCount = 1; pi.pSwapchains = &swapchain; pi.pImageIndices = &imageIndex;
vkQueuePresentKHR(queue, &pi);
```
When at least one of a present's fences signals, the wait semaphores of that present can be destroyed
(they are no longer in use); a swapchain can be destroyed once the fences of all its past presents
have signalled. Use this to retire swapchains after recreation instead of `vkDeviceWaitIdle`.

## 2. Switch present modes without recreating
At creation, list compatible modes:
```c
VkPresentModeKHR modes[] = { VK_PRESENT_MODE_FIFO_KHR, VK_PRESENT_MODE_MAILBOX_KHR, VK_PRESENT_MODE_IMMEDIATE_KHR };
VkSwapchainPresentModesCreateInfoEXT pm = { VK_STRUCTURE_TYPE_SWAPCHAIN_PRESENT_MODES_CREATE_INFO_EXT };
pm.presentModeCount = 3; pm.pPresentModes = modes;            // query compatibility via VkSurfacePresentModeCompatibilityEXT
```
Then chain `VkSwapchainPresentModeInfoEXT` into `VkPresentInfoKHR` with one mode per swapchain, each
one of the modes listed at creation. Switching between modes the surface reports as compatible
needs no swapchain recreation; behaviour for transitions between other modes is implementation-defined.

## 3. Scaling behaviour on resize
`VkSwapchainPresentScalingCreateInfoEXT` (`VK_PRESENT_SCALING_STRETCH_BIT_EXT`,
`ASPECT_RATIO_STRETCH`, `ONE_TO_ONE`) lets you define what happens when an image is presented to a surface of different
size; this may allow implementations to avoid returning `VK_ERROR_OUT_OF_DATE_KHR`.

## 4. Release acquired images
`vkReleaseSwapchainImagesEXT` returns images acquired but never presented (e.g. when you
decide to recreate mid-frame), avoiding a leak of acquired images in the old swapchain.

## Gotchas
- Enable the `swapchainMaintenance1` feature in `vkCreateDevice`; query compatible present modes by
  chaining `VkSurfacePresentModeEXT` (input) and `VkSurfacePresentModeCompatibilityEXT` (output) into
  `vkGetPhysicalDeviceSurfaceCapabilities2KHR`, since not all modes are mutually compatible.
- Fences for presents to the same swapchain on the same queue signal in present order.

## Verify
- [ ] Toggling between compatible present modes needs no swapchain recreation; validation reports no semaphore-reuse errors after resizing.

## Checked

- Date: 2026-10-25. Documentation release: Vulkan specification 1.4.366 (Vulkan-Docs main, commit a8b088a, 2026-10-23), including the generated vk.xml registry.
- Confirmed: VK_KHR_swapchain_maintenance1 (promoted from the EXT) adds present fences, per-present present-mode switching, present scaling (may avoid `VK_ERROR_OUT_OF_DATE_KHR`), deferred allocation and releasing acquired images (appendix); vk.xml dependencies: EXT needs `VK_EXT_surface_maintenance1`.
- Confirmed: WSI chapter: wait semaphores can be destroyed when a present fence signals, a swapchain once all its presents' fences signal; fences on one queue signal in order; present modes in `VkSwapchainPresentModeInfoKHR` must be those given at creation; compatibility is queried via `VkSurfacePresentModeKHR`/`VkSurfacePresentModeCompatibilityKHR` in the surface-capabilities2 chain; transitions between other modes are implementation-defined.
- Fixed: the draft pointed at `vkGetPhysicalDeviceSurfacePresentModes2EXT` (a full-screen-exclusive command) for compatibility queries. Removed the 'present fences signal later than the frame fence' remark (no source).

Method: documentation only; no commands were run.
