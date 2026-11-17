---
id: computing-software.computer-graphics-engineering.opengl.opengl-swap-interval-and-vsync
name: opengl-swap-interval-and-vsync
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, opengl-context, swap-interval, wgl-swap-control, adaptive-vsync, frame-pacing]
level: practitioner
status: docs-checked
description: "Control OpenGL vsync with swap intervals (WGL/GLX/EGL, GLFW), adaptive vsync, and avoid the latency and stutter traps of SwapBuffers."
sources: ["https://registry.khronos.org/OpenGL/extensions/EXT/WGL_EXT_swap_control.txt", "https://www.glfw.org/docs/latest/group__context.html#ga6d4e0cdf151b5e579bd67f13202994ed"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Swap interval and vsync in OpenGL

## 1. Setting it
```c
glfwMakeContextCurrent(win);
glfwSwapInterval(1);   // 1 = vsync, 0 = off, -1 = adaptive (needs *_swap_control_tear)
```
Under the hood GLFW uses the platform swap-control extensions (`wglSwapIntervalEXT` on Windows). A context must be current on the calling thread, and the WGL extension applies to the window of the current context; the default WGL interval is 1. Negative intervals need `WGL_EXT_swap_control_tear` or `GLX_EXT_swap_control_tear`; check with `glfwExtensionSupported` before passing -1.

| Interval | Behaviour |
|---|---|
| 1 | Wait for vblank; no tearing; frame rate quantised to refresh/N when you miss |
| 0 | Present immediately; tearing; lowest latency |
| -1 | Vsync when on time, tear when late (avoids 60->30 halving) |
| 2 | Every second vblank (30 Hz on 60 Hz), cinematic pacing |

## 2. Things that override you
- Some GPU drivers do not honour the requested swap interval, either because of a user setting that overrides the application's request or because of driver bugs (GLFW docs).

## 3. Latency traps
- Measuring frame time with CPU timers around `SwapBuffers` measures the vsync wait, not your
  work. Use GPU timer queries for GPU cost.

## Gotchas
- Calling `glfwSwapInterval` without a current context raises a `GLFW_NO_CURRENT_CONTEXT` error.
- GLFW does not set an interval at context creation, so the API default applies until you call it; some swap-control extensions cannot reset the interval to zero once it is non-zero.

## Verify
- [ ] With interval 1, frame times sit at one refresh period with no tearing in a moving-bar test.
- [ ] Interval -1 is only requested when the tear extension is reported supported.

## Checked

2026-10-28. Confirmed in the GLFW `glfwSwapInterval` docs: interval is the number of screen updates to wait, a current context is required (`GLFW_NO_CURRENT_CONTEXT`), negative intervals need the WGL/GLX `swap_control_tear` extensions, drivers may not honour the request, the interval is not set at context creation. Confirmed in WGL_EXT_swap_control: applies to the window of the current context, default interval 1.
Removed (not in the fetched pages): `glXSwapIntervalEXT`/MESA and `eglSwapInterval` naming, DWM, Wayland and VRR claims, env vars, `glFinish` latency advice, multi-window claim, "silently does nothing" (the docs say it raises an error), 16.7 ms figure, PresentMon fields, dead links (the EXT_swap_control_tear page 404s; the Khronos wiki page is blocked).

Method: documentation only; no commands were run.
