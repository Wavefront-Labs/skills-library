---
id: computing-software.computer-graphics-engineering.opengl.opengl-glgeterror-and-state-leak-debugging
name: opengl-glgeterror-and-state-leak-debugging
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, gl-context-debug, glgeterror, gl-state-leaks, gl-error-checking, debugging, renderdoc]
level: practitioner
status: docs-checked
description: "Find OpenGL errors and leaked state: glGetError drain loops, GL_CHECK macros, bracketing failures, state save/restore and RenderDoc state diffs."
sources: ["https://registry.khronos.org/OpenGL-Refpages/gl4/html/glGetError.xhtml", "https://registry.khronos.org/OpenGL/specs/gl/glspec46.core.pdf", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glPixelStore.xhtml", "https://www.glfw.org/docs/latest/compat_guide.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# glGetError discipline and state-leak debugging

**Goal:** pin a GL error or a "wrong state" bug to the exact call that caused it, on contexts
where `KHR_debug` is missing (the GLFW compat guide says macOS has no debug contexts) or as a second check.

## 1. How glGetError really works
- Errors are **flags**, not a per-call result: `glGetError()` returns the value of one error flag and resets
  it. Implementations may keep several flag-code pairs and return them in unspecified order, so call it in a loop
  until `GL_NO_ERROR` or you will attribute old errors to new calls.
- A call that generates `GL_INVALID_ENUM`, `GL_INVALID_VALUE` or `GL_INVALID_OPERATION` is ignored apart from
  setting the flag; after `GL_OUT_OF_MEMORY` the GL state is undefined (except the error flags).
- Treat `glGetError` as a debug aid and keep it out of per-draw release paths.

```c
#ifndef NDEBUG
static void glCheck(const char* what, const char* file, int line) {
    for (GLenum e; (e = glGetError()) != GL_NO_ERROR; )
        fprintf(stderr, "%s:%d %s -> 0x%04X\n", file, line, what, e);
}
#define GL(x) do { x; glCheck(#x, __FILE__, __LINE__); } while (0)
#else
#define GL(x) x
#endif
```
Drain once at start-up (`glCheck("init")`) so errors from the loader or toolkit do not
land on your first call.

## 2. Bisecting a stray error
Insert `glCheck` at frame start, after each pass, then halve the interval that contains the
error. Common culprits by code: `0x0500 INVALID_ENUM` (core profile rejects a compat enum such as
`GL_QUADS`/`GL_LUMINANCE`), `0x0502 INVALID_OPERATION` (no VAO bound in core for vertex-array commands, program not linked,
format/type mismatch in `glTexImage`), `0x0506 INVALID_FRAMEBUFFER_OPERATION` (draw to an
incomplete FBO, check `glCheckFramebufferStatus`).

## 3. State leaks
GL is a global state machine; a helper that changes blend, depth, scissor, viewport, bound
textures or `GL_UNPACK_ALIGNMENT` and does not restore it breaks the next pass.
- Prefer **set what you need** at the start of each pass over restore-on-exit; an explicit
  per-pass state block (blend, depth test/write, cull, scissor, viewport, program, VAO) is
  cheaper than debugging leaks. DSA (`glBindTextureUnit`, `glNamed*`) removes bind-to-edit leaks.
- Third-party code (UI and text renderers) should save and restore the state it touches.
- Debug-only assert: query `glGetIntegerv(GL_CURRENT_PROGRAM / GL_VERTEX_ARRAY_BINDING /
  GL_DRAW_FRAMEBUFFER_BINDING)` and `glIsEnabled(GL_BLEND/GL_DEPTH_TEST/GL_SCISSOR_TEST)` at pass
  boundaries and compare with the expected block.
- With a frame debugger, capture a bad draw and a good draw and diff their pipeline state (blend, depth,
  raster, bound resources); the difference is the leak.

## Gotchas
- `GL_UNPACK_ALIGNMENT` defaults to 4: RGB8 textures with odd widths upload skewed. Set to 1
  for tightly packed data and leave it set deliberately.

## Verify
- [ ] Debug build runs a frame with zero `glCheck` output after draining start-up errors.
- [ ] Shuffling pass order does not change the image (no leaked state between passes).

## Checked

Date: 2026-10-26. Documentation: gl4 reference page for glGetError and glPixelStore, OpenGL 4.6 core spec (5 May 2022), GLFW compat guide. Confirmed: error flags (several flag-code pairs, one returned and cleared per call, loop until `GL_NO_ERROR`); erroring calls are ignored except `GL_OUT_OF_MEMORY`; error names `GL_INVALID_ENUM`, `GL_INVALID_OPERATION`, `GL_INVALID_FRAMEBUFFER_OPERATION`; legacy `GL_LUMINANCE` formats are removed from core and `GL_QUADS` is not a core draw mode; vertex-array commands raise `GL_INVALID_OPERATION` with no VAO bound; `GL_UNPACK_ALIGNMENT` initial value 4. Removed: the claim that glGetError stalls multithreaded drivers, ImGui backend and RenderDoc UI references, wrong-thread and WebGL notes (no documentation read).

Method: documentation only; no commands were run.
