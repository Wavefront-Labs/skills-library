---
id: computing-software.computer-graphics-engineering.opengl.vulkan-present-wait-and-present-id
name: vulkan-present-wait-and-present-id
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, vulkan-swapchain, present-wait, present-id, frame-pacing]
level: advanced
status: docs-checked
description: "Pace Vulkan frames and cut latency with VK_KHR_present_id/present_wait: tag presents, wait for display, and start frames just in time."
sources: ["https://github.com/KhronosGroup/Vulkan-Docs/blob/main/appendices/VK_KHR_present_wait.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/appendices/VK_KHR_present_wait2.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/appendices/VK_KHR_present_id2.adoc", "https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/VK_KHR_surface/wsi.adoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Present wait and present id

`VK_KHR_present_id` tags each present with an increasing 64-bit id. `VK_KHR_present_wait`
lets the CPU block until a given id has been *displayed* (first pixel visible), not merely
queued. Together they give frame pacing and latency control without vendor SDKs.

## Tag presents
```c
uint64_t id = ++presentCounter;
VkPresentIdKHR pid = { VK_STRUCTURE_TYPE_PRESENT_ID_KHR };
pid.swapchainCount = 1; pid.pPresentIds = &id;
VkPresentInfoKHR pi = { VK_STRUCTURE_TYPE_PRESENT_INFO_KHR, &pid, /* ... */ };
vkQueuePresentKHR(queue, &pi);
```

## Wait before starting the next frame
```c
// at frame start: don't get more than 1 present ahead of the display
if (presentCounter >= 1)
    vkWaitForPresentKHR(device, swapchain, presentCounter - 1, 100'000'000 /* 100 ms */);
sampleInput(); simulate(); record(); submit(); present();
```
Waiting for `N-1` keeps one present queued; waiting for `N` (the frame just presented) minimises
latency at the cost of GPU idle bubbles.

## Measuring
Record the CPU time when `vkWaitForPresentKHR` returns for each id: the deltas are actual
display intervals. Missed vblanks show as 33 ms gaps at 60 Hz; correlate with CPU/GPU frame
times to see which side was late.

## Handling errors and timeouts
- Returns `VK_TIMEOUT` if the id has not been presented within the timeout: don't block the loop
  forever; use a modest timeout and continue.
- When the swapchain becomes out of date the call returns `VK_SUCCESS` (image delivered to the
  presentation engine) or `VK_ERROR_OUT_OF_DATE_KHR`; `VK_SUBOPTIMAL_KHR` and surface-lost errors are
  possible too: handle as for present.
- Each non-zero id must be greater than all earlier ids for that swapchain (zero means no id), and the
  swapchain passed to `vkWaitForPresentKHR` must not be retired: track ids per swapchain.

## Support
Enable the `presentId` and `presentWait` features (`VK_KHR_present_wait` depends on
`VK_KHR_present_id`). `VK_KHR_present_id2` and `VK_KHR_present_wait2` are newer variants driven by
surface capabilities (`VkSurfaceCapabilitiesPresentId2KHR`) rather than device features;
`vkWaitForPresent2KHR` completes when the presentation has taken effect or been replaced without
presentation. Check which extensions the device exposes.

## Gotchas
- `vkWaitForPresentKHR` returns once the swapchain's present id reaches the requested id. With
  `VK_PRESENT_MODE_MAILBOX_KHR` (or other modes where queued images can be replaced), a wait on a
  replaced image must signal no later than the wait on the image that replaced it.

## Verify
- [ ] Display-interval log shows steady refresh-rate intervals; measured click-to-photon latency drops vs. the unpaced loop.

## Checked

- Date: 2026-10-25. Documentation release: Vulkan specification 1.4.366 (Vulkan-Docs main, commit a8b088a, 2026-10-23), including the generated vk.xml registry.
- Confirmed: present_wait: `vkWaitForPresentKHR` blocks until the swapchain's present id is greater than or equal to the requested id or the timeout passes; it finishes when the present is visible, as close as possible to the first pixel (appendix and WSI chapter); success codes `VK_SUCCESS`, `VK_TIMEOUT`, `VK_SUBOPTIMAL_KHR` (vk.xml).
- Confirmed: VUID-VkPresentIdKHR-presentIds-04999: each non-zero id must be greater than all previously submitted ids for that swapchain; `VK_KHR_present_wait` depends on `VK_KHR_present_id` (vk.xml `depends`); present_id2 and present_wait2 exist and are surface-capability driven.
- Fixed: the draft said a wait must target the newest id under MAILBOX, but the spec only requires waits for replaced images to signal no later than the replacing image. Removed Windows, Mesa, MoltenVK, Android and latency-frame-count remarks (no source).

Method: documentation only; no commands were run.
