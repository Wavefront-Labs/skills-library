---
id: computing-software.computer-graphics-engineering.opengl.vulkan-fullscreen-exclusive-and-display-control
name: vulkan-fullscreen-exclusive-and-display-control
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, vulkan-swapchain, fullscreen-exclusive, vk-khr-display, direct-to-display]
level: advanced
status: docs-checked
description: "Control Vulkan fullscreen behaviour: VK_EXT_full_screen_exclusive on Windows, borderless vs exclusive trade-offs, and direct-to-display with VK_KHR_display."
sources: ["https://docs.vulkan.org/spec/latest/appendices/VK_EXT_full_screen_exclusive.html", "https://docs.vulkan.org/spec/latest/appendices/VK_KHR_display.html", "https://docs.vulkan.org/spec/latest/appendices/VK_EXT_acquire_drm_display.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fullscreen exclusive and display control

## Windows: VK_EXT_full_screen_exclusive
The extension lets the application set the policy for swapchain creation and presentation relating to full-screen access: the implementation
may acquire exclusive access to a display for a window covering the whole screen, which can bypass composition but can also cause disruptive
transitions. Make the policy explicit:
```c
VkSurfaceFullScreenExclusiveInfoEXT fse = { VK_STRUCTURE_TYPE_SURFACE_FULL_SCREEN_EXCLUSIVE_INFO_EXT };
fse.fullScreenExclusive = VK_FULL_SCREEN_EXCLUSIVE_APPLICATION_CONTROLLED_EXT;
VkSurfaceFullScreenExclusiveWin32InfoEXT w32 = { VK_STRUCTURE_TYPE_SURFACE_FULL_SCREEN_EXCLUSIVE_WIN32_INFO_EXT };
w32.hmonitor = MonitorFromWindow(hwnd, MONITOR_DEFAULTTOPRIMARY);
fse.pNext = &w32;
swapchainCI.pNext = &fse;
// both structs extend VkSwapchainCreateInfoKHR; after creation, when the window is fullscreen and focused:
vkAcquireFullScreenExclusiveModeEXT(device, swapchain);
// on alt-tab / focus loss:
vkReleaseFullScreenExclusiveModeEXT(device, swapchain);
```
| Mode | Meaning |
|---|---|
| `DEFAULT` | implementation decides |
| `ALLOWED` | implementation may use exclusive access, never required to |
| `DISALLOWED` | exclusive access is not used |
| `APPLICATION_CONTROLLED` | you manage it with `vkAcquireFullScreenExclusiveModeEXT` / `vkReleaseFullScreenExclusiveModeEXT` |

Acquire and release are valid only for swapchains created with `APPLICATION_CONTROLLED` (`VUID-vkAcquireFullScreenExclusiveModeEXT-swapchain-02675`).

For `APPLICATION_CONTROLLED` swapchains, present returns `VK_ERROR_FULL_SCREEN_EXCLUSIVE_MODE_LOST_EXT` when the swapchain does not have exclusive access,
possibly for reasons outside the application's control. The spec says the application can attempt to acquire again for the same swapchain,
so handle it by re-acquiring when appropriate.

## Borderless vs exclusive
The spec only says exclusive access can bypass composition but may bring disruptive transitions. Choose the policy by measuring on your target
systems (latency, alt-tab behaviour, capture tools); `DISALLOWED` keeps behaviour predictable for tools and overlays.

## Direct-to-display (VK_KHR_display)
Render without a window system (kiosks, embedded, VR compositors):
```c
vkGetPhysicalDeviceDisplayPropertiesKHR(gpu, &n, displays);
vkGetDisplayModePropertiesKHR(gpu, displays[0].display, &m, modes);
VkDisplaySurfaceCreateInfoKHR ds = { VK_STRUCTURE_TYPE_DISPLAY_SURFACE_CREATE_INFO_KHR };
ds.displayMode = modes[0].displayMode; ds.imageExtent = modes[0].parameters.visibleRegion;
// also set planeIndex, planeStackIndex, transform, globalAlpha and alphaMode from the plane properties
vkCreateDisplayPlaneSurfaceKHR(instance, &ds, NULL, &surface);
```
`VK_EXT_acquire_drm_display` (DRM) and `VK_EXT_acquire_xlib_display` let an application take control of a display it does not already own;
per the extension text, once acquired the display is under the application's full control until released or the connector is unplugged.

## Gotchas
- If you change the display mode or window size, recreate the swapchain and render targets.
- Capture tools and overlays may behave differently with exclusive access; test them.

## Verify
- [ ] Alt-tab and focus changes in fullscreen produce no device loss; `FULL_SCREEN_EXCLUSIVE_MODE_LOST` is handled by re-acquiring.

## Checked
Checked 2026-10-26 against Vulkan 1.4.366 (appendices/VK_EXT_full_screen_exclusive.adoc, VK_EXT_acquire_drm_display.adoc, chapters/VK_KHR_surface/wsi.adoc, validusage.json, xml/vk.xml).
Confirmed: VkSurfaceFullScreenExclusiveInfoEXT and Win32 info (hmonitor) extend VkSwapchainCreateInfoKHR; the four mode enums; acquire/release validity rules; MODE_LOST return and re-acquire statement; VkDisplaySurfaceCreateInfoKHR members; VK_EXT_acquire_drm_display and VK_EXT_acquire_xlib_display exist. Removed the Windows flip-model, PresentMon, SteamVR and Linux-compositor claims.
Method: documentation only; no commands were run.
