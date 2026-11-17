---
id: computing-software.computer-graphics-engineering.opengl.opengl-default-framebuffer-and-pixel-format
name: opengl-default-framebuffer-and-pixel-format
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, framebuffer, default-framebuffer, pixel-format, framebuffer-srgb, hidpi]
level: practitioner
status: docs-checked
description: "Configure the OpenGL default framebuffer: pixel format hints (depth, stencil, MSAA, sRGB), HiDPI framebuffer size, and querying what you actually got."
sources: ["https://www.glfw.org/docs/latest/window_guide.html", "https://www.glfw.org/docs/latest/context_guide.html", "https://registry.khronos.org/OpenGL/specs/gl/glspec46.core.pdf", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glGetFramebufferAttachmentParameter.xhtml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Default framebuffer and pixel format

The default framebuffer (FBO 0) belongs to the window system. Its format is fixed at
window/context creation; you can only request it, then check.

## Request
```c
glfwWindowHint(GLFW_RED_BITS, 8); glfwWindowHint(GLFW_GREEN_BITS, 8); glfwWindowHint(GLFW_BLUE_BITS, 8);
glfwWindowHint(GLFW_ALPHA_BITS, 0);         // 8 if you need destination alpha / transparent windows
glfwWindowHint(GLFW_DEPTH_BITS, 24);
glfwWindowHint(GLFW_STENCIL_BITS, 8);
glfwWindowHint(GLFW_SAMPLES, 0);            // keep 0: do MSAA in your own FBO and resolve
glfwWindowHint(GLFW_SRGB_CAPABLE, GLFW_TRUE);
glfwWindowHint(GLFW_DOUBLEBUFFER, GLFW_TRUE);
```

## Check what you got
```c
GLint enc, depthBits, samples;
glGetNamedFramebufferAttachmentParameteriv(0, GL_BACK_LEFT, GL_FRAMEBUFFER_ATTACHMENT_COLOR_ENCODING, &enc); // GL_SRGB or GL_LINEAR
glGetNamedFramebufferAttachmentParameteriv(0, GL_DEPTH, GL_FRAMEBUFFER_ATTACHMENT_DEPTH_SIZE, &depthBits);
glGetIntegerv(GL_SAMPLES, &samples);
```
Note the attachment names differ for FBO 0: `GL_BACK_LEFT`, `GL_DEPTH`, `GL_STENCIL`, not
`GL_COLOR_ATTACHMENT0`. With framebuffer 0 the DSA query addresses the default draw framebuffer.

## sRGB output
If the back buffer is sRGB-capable, `glEnable(GL_FRAMEBUFFER_SRGB)` makes the hardware encode
linear shader output to sRGB on write (and blend in linear). Without it, do the conversion in
the final shader (`pow(c, 1/2.2)` or exact sRGB curve) — never both. Many engines render to
their own `RGBA16F` FBO and do tone mapping + encoding in a final pass, so the default
framebuffer's sRGB flag only matters for that last blit.

## HiDPI / Retina
Window size (screen coordinates) and framebuffer size (pixels) differ on macOS Retina and
Windows with DPI scaling.
```c
int fbw, fbh; glfwGetFramebufferSize(win, &fbw, &fbh);
glViewport(0, 0, fbw, fbh);                 // NOT glfwGetWindowSize
glfwSetFramebufferSizeCallback(win, onResize);
```
Mouse coordinates come in window coordinates; scale by `fbw / winw` for picking.

## Gotchas
- Asking for `GLFW_SAMPLES` > 0 and also rendering to MSAA FBOs wastes memory; the default
  FB samples only matter when drawing directly into it.
- `GLFW_SRGB_CAPABLE` is a request: check the encoding query and fall back to shader encoding if it reports
  `GL_LINEAR`.
- Transparent windows need `GLFW_TRANSPARENT_FRAMEBUFFER` and framebuffer alpha bits: GLFW composites the
  window with the background using the framebuffer alpha channel.

## Verify
- [ ] Query results logged at startup match the requested format; viewport equals framebuffer size on a HiDPI display.

## Checked

Date: 2026-10-26. Documentation: GLFW 3.4 window guide (main branch), OpenGL 4.6 core spec (5 May 2022) and the gl4 reference page for glGetFramebufferAttachmentParameter. Confirmed: GLFW hints `GLFW_RED_BITS` to `GLFW_STENCIL_BITS`, `GLFW_SAMPLES`, `GLFW_SRGB_CAPABLE` (the `GL_FRAMEBUFFER_SRGB` enable controls sRGB rendering), `GLFW_DOUBLEBUFFER`, `GLFW_TRANSPARENT_FRAMEBUFFER` (uses framebuffer alpha); `glfwGetFramebufferSize` for pixel sizes and the window-size warning; default framebuffer attachment names `GL_BACK_LEFT`, `GL_DEPTH`, `GL_STENCIL`; framebuffer 0 in the DSA query means the default draw framebuffer; `GL_FRAMEBUFFER_ATTACHMENT_COLOR_ENCODING` and sRGB blending in linear space. Removed: Wayland/EGL sRGB config claim and the premultiplied-output claim (no documentation read).

Method: documentation only; no commands were run.
