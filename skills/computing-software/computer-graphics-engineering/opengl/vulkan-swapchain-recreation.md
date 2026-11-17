---
id: computing-software.computer-graphics-engineering.opengl.vulkan-swapchain-recreation
name: vulkan-swapchain-recreation
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, vulkan, vulkan-swapchain, swapchain-recreation, vk-error-out-of-date, vk-suboptimal-khr, window-resize, minimize, oldswapchain]
level: practitioner
status: docs-checked
description: "Handle Vulkan window resize, minimise and display changes: detect OUT_OF_DATE/SUBOPTIMAL at acquire and present, recreate the swapchain and size-dependent targets safely."
sources: ["https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/VK_KHR_surface/wsi.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/appendices/VK_KHR_swapchain_maintenance1.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/xml/vk.xml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vulkan swapchain recreation

**Goal:** resizing, minimising, moving between monitors and fullscreen toggles never
crash, hang or show validation errors.

## 1. Detect
```cpp
VkResult r = vkAcquireNextImageKHR(dev, swapchain, UINT64_MAX, frame.acquireSem, VK_NULL_HANDLE, &img);
if (r == VK_ERROR_OUT_OF_DATE_KHR) { recreate(); return; }           // cannot render this frame
if (r != VK_SUCCESS && r != VK_SUBOPTIMAL_KHR) fatal(r);
... record, submit ...
r = vkQueuePresentKHR(queue, &present);
if (r == VK_ERROR_OUT_OF_DATE_KHR || r == VK_SUBOPTIMAL_KHR || framebufferResized) {
    framebufferResized = false; recreate();
}
```
- Also set `framebufferResized` from the window resize callback: when the swapchain extent differs from the surface, platforms may scale and
  return `VK_SUBOPTIMAL_KHR` or fail with `VK_ERROR_OUT_OF_DATE_KHR` (the spec says behaviour differs per platform), so do not rely on one result.
- On acquire OUT_OF_DATE, the acquire semaphore was **not** signalled; do not submit a
  wait on it. Reset the frame's fence only after a successful acquire, or the next
  `vkWaitForFences` deadlocks.

## 2. Recreate
```cpp
void recreate() {
    int w = 0, h = 0; glfwGetFramebufferSize(win, &w, &h);
    while (w == 0 || h == 0) { glfwWaitEvents(); glfwGetFramebufferSize(win, &w, &h); } // minimised
    vkDeviceWaitIdle(dev);                    // simple and correct; see below for smoother
    VkSwapchainKHR old = swapchain;
    createSwapchain(/*oldSwapchain=*/old);    // re-query caps: extent, transform may change
    destroyImageViews(); vkDestroySwapchainKHR(dev, old, nullptr);
    createImageViews();
    recreateSizeDependentTargets();           // depth buffer, G-buffer, post targets
    // per-image semaphores: recreate if image count changed
}
```
- Re-query surface capabilities every time; extent and transform can change.
- Projection matrices and viewport/scissor (dynamic state) must use the new extent.

## 3. Smoother resize (optional)
`vkDeviceWaitIdle` causes a hitch per resize event. Alternatives: pass `oldSwapchain`
and keep rendering, deferring destruction of the old swapchain and its views until the
frames that used it have completed (track with the frame fences), or with
`VK_KHR_swapchain_maintenance1` (promoted from `VK_EXT_swapchain_maintenance1`) use present fences to know when the resources of a present can be destroyed.

## Gotchas
- Don't destroy the old swapchain while a present on it may still be pending; waiting idle is the simple way, present fences from
  swapchain maintenance1 the precise one.
- Exclusive fullscreen (`VK_EXT_full_screen_exclusive`) loss also returns
  `VK_ERROR_FULL_SCREEN_EXCLUSIVE_MODE_LOST_EXT`.

## Verify
- [ ] Continuous drag-resize for 30 s: no validation errors, no crash, memory stable.
- [ ] Minimise and restore: no busy-loop at 100% CPU while minimised, rendering resumes.
- [ ] Moving the window to a monitor with a different DPI/refresh keeps correct size.

## Checked

2026-10-26: Vulkan-Docs main (latest commit 2026-10-23), `wsi.adoc` and `VK_KHR_swapchain_maintenance1.adoc`, plus vk.xml. Confirmed: when `vkAcquireNextImageKHR` does not acquire an image the semaphore and fence are unaffected, and a `VK_SUBOPTIMAL_KHR` result still acquires an image; presenting a swapchain whose extent differs from the surface either scales and returns `VK_SUBOPTIMAL_KHR` or fails with `VK_ERROR_OUT_OF_DATE_KHR` depending on the platform; passing `oldSwapchain` retires it and it can be destroyed to free its memory; `VK_EXT_swapchain_maintenance1` is promoted to `VK_KHR_swapchain_maintenance1`, which adds a fence signalled when present resources can be destroyed; `VK_ERROR_FULL_SCREEN_EXCLUSIVE_MODE_LOST_EXT` exists. Removed the claims that X11 and some Wayland compositors never return OUT_OF_DATE, that Windows blocks the message loop during drag-resize, and that the HDR monitor changes format support.

Method: documentation only; no commands were run.
