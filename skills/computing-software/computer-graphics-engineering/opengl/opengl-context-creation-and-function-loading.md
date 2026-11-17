---
id: computing-software.computer-graphics-engineering.opengl.opengl-context-creation-and-function-loading
name: opengl-context-creation-and-function-loading
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, opengl-context, glfw, sdl2, core-profile, glad, glew, gl-extensions, forward-compatible, debug-context, macos-opengl]
level: practitioner
status: docs-checked
description: "Create an OpenGL 4.x core-profile context with GLFW or SDL, load functions with glad, check version and extensions, and avoid the classic black-window failures."
sources: ["https://www.glfw.org/docs/latest/context_guide.html", "https://www.glfw.org/docs/latest/window_guide.html", "https://www.glfw.org/docs/latest/compat_guide.html", "https://github.com/Dav1dde/glad", "https://registry.khronos.org/OpenGL/specs/gl/glspec46.core.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenGL context creation and function loading

**Goal:** a window with a known GL version/profile, every entry point loaded, and a
startup log that tells you exactly what driver you got.

## 1. Request the context (GLFW)
```c
glfwInit();
glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 4);
glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 6);
glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);
glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GLFW_TRUE);  // macOS only offers forward-compatible core contexts
#ifndef NDEBUG
glfwWindowHint(GLFW_OPENGL_DEBUG_CONTEXT, GLFW_TRUE);   // debug context (KHR_debug); ignored on macOS
#endif
glfwWindowHint(GLFW_SRGB_CAPABLE, GLFW_TRUE);
GLFWwindow* w = glfwCreateWindow(1280, 720, "app", NULL, NULL);
if (!w) { /* the requested version is unavailable: fall back or report */ }
glfwMakeContextCurrent(w);
glfwSwapInterval(1);                                    // 1 = wait for one screen update per swap; 0 = no wait
```

## 2. Load function pointers (glad)
Generate a loader with the glad web service (see the glad README), including the extensions you intend to
use (e.g. `GL_KHR_debug`, `GL_ARB_bindless_texture`).
```c
#include <glad/gl.h>          // glad2; include BEFORE any other GL header
int ver = gladLoadGL(glfwGetProcAddress);
if (!ver) fatal("gladLoadGL failed - no current context?");
printf("GL %d.%d  %s / %s\n", GLAD_VERSION_MAJOR(ver), GLAD_VERSION_MINOR(ver),
       glGetString(GL_VENDOR), glGetString(GL_RENDERER));
if (!GLAD_GL_ARB_bindless_texture) { /* take the fallback path */ }
```
- Loading must happen **after** `glfwMakeContextCurrent`: the glad README example loads right after it.

## 3. Extension checks in core profile
`glGetString(GL_EXTENSIONS)` is **removed** in the core profile (the 4.6 core spec lists the unified extension string as removed). Use:
```c
GLint n; glGetIntegerv(GL_NUM_EXTENSIONS, &n);
for (GLint i = 0; i < n; ++i) puts((const char*)glGetStringi(GL_EXTENSIONS, i));
```
Prefer the loader's generated flags over string compares.

## Gotchas
- **Black window on core profile:** no VAO bound. The core profile has no default VAO,
  so vertex-array commands raise `GL_INVALID_OPERATION` until one is bound; bind one even for attribute-less
  fullscreen triangles.
- **macOS:** OpenGL is deprecated by Apple; GLFW's compat guide says only forward-compatible core
  contexts are available there (the forward-compat hint is ignored since GLFW 3.4) and debug contexts
  are not supported. Check `GL_VERSION` at runtime.
- **Framebuffer vs window size** differ on HiDPI: use `glfwGetFramebufferSize` for
  `glViewport`, not the window size.

## Verify
- [ ] Startup log prints the GL version, vendor and renderer you expected.
- [ ] A missing optional extension takes the fallback path instead of crashing on a NULL pointer.
- [ ] Debug builds create a debug context (`GL_CONTEXT_FLAGS & GL_CONTEXT_FLAG_DEBUG_BIT`).
- [ ] Resizing on a HiDPI display keeps the viewport filling the window.

## Checked

Date: 2026-10-26. Documentation: GLFW 3.4 docs (window, context and compat guides, main branch), glad README (2.0 branch), OpenGL 4.6 core spec (5 May 2022). Confirmed: GLFW hint names (`GLFW_CONTEXT_VERSION_MAJOR/MINOR`, `GLFW_OPENGL_PROFILE`, `GLFW_OPENGL_FORWARD_COMPAT`, `GLFW_OPENGL_DEBUG_CONTEXT`, `GLFW_SRGB_CAPABLE`); macOS limits (forward-compatible core only, no debug contexts); `glfwGetFramebufferSize` for pixel sizes; glad2 `gladLoadGL(glfwGetProcAddress)` and `GLAD_VERSION_MAJOR/MINOR`; unified extension string removed in core. Removed: macOS 4.1 cap and compute claim, SDL attributes, glad CLI flags, GLEW workaround, laptop GPU exports, remote-desktop note (no documentation read).

Method: documentation only; no commands were run.
