---
id: computing-software.computer-graphics-engineering.opengl.opengl-readpixels-and-screenshots
name: opengl-readpixels-and-screenshots
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, framebuffer, glreadpixels, screenshot-capture, readback]
level: practitioner
status: docs-checked
description: "Read pixels back from OpenGL framebuffers correctly: read buffer selection, MSAA resolve first, alignment, row flip, sRGB, and float/depth reads."
sources: ["https://registry.khronos.org/OpenGL-Refpages/gl4/html/glReadPixels.xhtml", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glPixelStore.xhtml", "https://registry.khronos.org/OpenGL/specs/gl/glspec46.core.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# glReadPixels and screenshots

## Minimal correct screenshot
```c
glBindFramebuffer(GL_READ_FRAMEBUFFER, 0);           // default FB (or your resolved FBO)
glReadBuffer(GL_BACK);                               // read before SwapBuffers
glPixelStorei(GL_PACK_ALIGNMENT, 1);                 // tight rows for RGB data
std::vector<uint8_t> px(w * h * 3);
glReadPixels(0, 0, w, h, GL_RGB, GL_UNSIGNED_BYTE, px.data());
// GL's origin is bottom-left: reverse the row order, then write px with your image encoder
```

## Checklist of things that go wrong
| Symptom | Cause / fix |
|---|---|
| Sheared diagonal image | `GL_PACK_ALIGNMENT` 4 with RGB rows not multiple of 4: set 1 |
| Upside down | GL bottom-left origin: flip rows |
| Black image | reading after SwapBuffers, wrong read buffer, or FBO not bound to `GL_READ_FRAMEBUFFER` |
| `GL_INVALID_OPERATION` | reading a multisampled FBO: blit-resolve to a single-sample FBO first |
| Too dark / washed out | sRGB mismatch: linear float target read as UNORM, or sRGB FB read and encoded again |
| Size wrong on HiDPI | used window size not framebuffer size (`glfwGetFramebufferSize`) |
| Huge hitch | synchronous read: use PBO + fence for anything per-frame |

## MSAA resolve before read
```c
glBlitNamedFramebuffer(msaaFbo, resolveFbo, 0,0,w,h, 0,0,w,h, GL_COLOR_BUFFER_BIT, GL_NEAREST);
glBindFramebuffer(GL_READ_FRAMEBUFFER, resolveFbo);
```

## Other reads
- HDR: `glReadPixels(..., GL_RGBA, GL_FLOAT, ...)` from an `RGBA16F` target.
- Depth: `GL_DEPTH_COMPONENT, GL_FLOAT` (non-linear; linearise with near/far for viewing).
- Integer IDs (picking): `GL_RED_INTEGER, GL_UNSIGNED_INT` from an `R32UI` attachment, read a
  1x1 region at the cursor; use a PBO to avoid stalls.
- Which attachment: `glNamedFramebufferReadBuffer(fbo, GL_COLOR_ATTACHMENT2)`.

## Gotchas
- Values for pixels outside the window connected to the current context are undefined (reference page);
  render to an FBO for reliable captures.
- `GL_IMPLEMENTATION_COLOR_READ_FORMAT/TYPE` give the preferred format and type for the current read
  framebuffer; `glGetInternalformativ(..., GL_READ_PIXELS_FORMAT, ...)` does the same per internal format.

## Verify
- [ ] Saved PNG matches the on-screen frame pixel-for-pixel (compare with OS screenshot) at odd window widths.

## Checked

Date: 2026-10-26. Documentation: gl4 reference pages for glReadPixels and glPixelStore, OpenGL 4.6 core spec (5 May 2022). Confirmed: `GL_INVALID_OPERATION` when the read framebuffer is multisampled; pixels outside the window are undefined; `GL_PACK_ALIGNMENT` semantics (initial value 4); `GL_IMPLEMENTATION_COLOR_READ_FORMAT/TYPE` follow the read framebuffer; `GL_READ_PIXELS_FORMAT` query; `glBlitNamedFramebuffer` resolve rules. Removed: stb function names, the front-buffer-undefined claim, EXR suggestion, the slow-CPU-conversion claim (no documentation read).

Method: documentation only; no commands were run.
