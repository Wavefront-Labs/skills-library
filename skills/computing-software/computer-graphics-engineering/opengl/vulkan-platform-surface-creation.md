---
id: computing-software.computer-graphics-engineering.opengl.vulkan-platform-surface-creation
name: vulkan-platform-surface-creation
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, vulkan, vulkan-swapchain, vk-surface, vkcreatewin32surfacekhr, wayland-vulkan]
level: practitioner
status: docs-checked
description: "Create VkSurfaceKHR on Win32, X11/XCB, Wayland, Android and Metal (or via GLFW/SDL), check present support per queue family, and handle surface loss."
sources: ["https://docs.vulkan.org/spec/latest/chapters/VK_KHR_surface/wsi.html", "https://www.glfw.org/docs/latest/vulkan_guide.html", "https://github.com/libsdl-org/SDL/blob/main/include/SDL3/SDL_vulkan.h"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Platform surface creation

## Instance extensions per platform
Each create function takes a `Vk*SurfaceCreateInfo*` structure holding the native handles listed.

| Platform | Extensions | Create function |
|---|---|---|
| Windows | `VK_KHR_surface`, `VK_KHR_win32_surface` | `vkCreateWin32SurfaceKHR(hinstance, hwnd)` |
| X11 | `VK_KHR_xcb_surface` (or `VK_KHR_xlib_surface`) | `vkCreateXcbSurfaceKHR(connection, window)` |
| Wayland | `VK_KHR_wayland_surface` | `vkCreateWaylandSurfaceKHR(wl_display, wl_surface)` |
| Android | `VK_KHR_android_surface` | `vkCreateAndroidSurfaceKHR(ANativeWindow*)` |
| macOS/iOS | `VK_EXT_metal_surface` | `vkCreateMetalSurfaceEXT(CAMetalLayer*)` |
| Headless | `VK_EXT_headless_surface` | testing without a display |

Let the windowing library do it:
```c
uint32_t n; const char** req = glfwGetRequiredInstanceExtensions(&n);    // add these to instance
glfwCreateWindowSurface(instance, window, NULL, &surface);
// SDL3: SDL_Vulkan_GetInstanceExtensions(&n); SDL_Vulkan_CreateSurface(win, instance, NULL, &surface);
```
For a Vulkan-only GLFW window call `glfwWindowHint(GLFW_CLIENT_API, GLFW_NO_API)` first so GLFW creates no OpenGL context (GLFW's Vulkan guide).
Separately, creating a second swapchain on a native window that already has one returns `VK_ERROR_NATIVE_WINDOW_IN_USE_KHR` (spec).

## Present support
```c
VkBool32 canPresent = VK_FALSE;
vkGetPhysicalDeviceSurfaceSupportKHR(gpu, qfi, surface, &canPresent);
```
Check per queue family; the graphics family usually presents, but not guaranteed (some
multi-GPU laptops). If graphics and present families differ, the swapchain needs
`VK_SHARING_MODE_CONCURRENT` over both or an ownership transfer.

## Surface lifetime
- Destroy order: all swapchains for the surface -> surface -> instance (`VUID-vkDestroySurfaceKHR-surface-01266`).
- Android: when the platform destroys the native window, destroy the swapchain and surface and recreate both when a new
  window arrives; presenting to a lost surface returns `VK_ERROR_SURFACE_LOST_KHR`.
- Wayland: `currentExtent` is the special value (0xFFFFFFFF, 0xFFFFFFFF), meaning the surface size is determined by the swapchain extent you choose.

## Gotchas
- `VK_ERROR_SURFACE_LOST_KHR`: recreate the surface, then the swapchain.
- On Linux choose xcb or wayland at runtime according to the session; enable only the extensions the instance reports.
- macOS/iOS: `vkCreateMetalSurfaceEXT` takes a `CAMetalLayer` (`pLayer`).

## Verify
- [ ] Present support queried and logged; app survives background/foreground on Android and window close without validation errors.

## Checked
Checked 2026-10-26 against Vulkan 1.4.366 (xml/vk.xml, chapters/VK_KHR_surface/wsi.adoc, appendices for the surface extensions, validusage.json), GLFW docs/vulkan.md and SDL3 include/SDL3/SDL_vulkan.h (main).
Confirmed: create-info members (hinstance/hwnd, connection/window, display/surface, window, pLayer); NATIVE_WINDOW_IN_USE rule is for swapchain creation; surface destroyed only after its swapchains; Wayland currentExtent special value; GLFW_NO_API hint and glfwGetRequiredInstanceExtensions/glfwCreateWindowSurface; SDL_Vulkan_GetInstanceExtensions(Uint32*) and SDL_Vulkan_CreateSurface(window, instance, allocator, surface). Removed the unverified Android event names, Wayland FIFO blocking, XDG_SESSION_TYPE and contentsScale claims.
Method: documentation only; no commands were run.
