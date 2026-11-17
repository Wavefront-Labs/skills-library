---
id: computing-software.computer-graphics-engineering.opengl.opengl-khr-debug-output-and-object-labels
name: opengl-khr-debug-output-and-object-labels
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, gl-debug-output, khr-debug, gl-debug-callback, gldebugmessagecallback, object-labels, debug-groups, renderdoc, gl-errors]
level: practitioner
status: docs-checked
description: "Wire up KHR_debug in OpenGL: synchronous debug callback with breakpoints, message filtering, object labels and push/pop debug groups that show up in RenderDoc."
sources: ["https://registry.khronos.org/OpenGL/extensions/KHR/KHR_debug.txt", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glDebugMessageCallback.xhtml", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glDebugMessageControl.xhtml", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glPushDebugGroup.xhtml", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/glObjectLabel.xhtml", "https://github.com/KhronosGroup/OpenGL-Registry/blob/main/xml/gl.xml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenGL KHR_debug output and object labels

**Goal:** every GL error, performance warning and undefined-behaviour report arrives at a
callback with a stack you can break on, and captures are readable because every object
and pass has a name. Core since GL 4.3 (KHR_debug).

## 1. Install the callback
Request a debug context (`GLFW_OPENGL_DEBUG_CONTEXT`); `GL_DEBUG_OUTPUT` is initially enabled only in one — and elsewhere the amount of output is implementation-defined.
```c
static void APIENTRY onGlDebug(GLenum src, GLenum type, GLuint id, GLenum sev,
                               GLsizei len, const GLchar* msg, const void* user) {
    if (sev == GL_DEBUG_SEVERITY_NOTIFICATION) return;
    fprintf(stderr, "[GL %s] %s\n", sevName(sev), msg);
    if (type == GL_DEBUG_TYPE_ERROR) DEBUG_BREAK();          // __debugbreak / raise(SIGTRAP)
}
glEnable(GL_DEBUG_OUTPUT);
glEnable(GL_DEBUG_OUTPUT_SYNCHRONOUS);   // callback runs inside the offending call -> useful stack
glDebugMessageCallback(onGlDebug, NULL);
// silence message ids you have identified as noise (ids are implementation-defined)
GLuint quiet[] = { 0 /* replace with ids seen in your own logs */ };
glDebugMessageControl(GL_DEBUG_SOURCE_API, GL_DEBUG_TYPE_OTHER, GL_DONT_CARE, 1, quiet, GL_FALSE);
```
- `SYNCHRONOUS` costs performance; keep it for debug builds only.
- The callback may be called from a driver thread when not synchronous; keep it thread-safe.

## 2. Name objects
```c
glObjectLabel(GL_BUFFER, vbo, -1, "terrain.vbo");
glObjectLabel(GL_TEXTURE, albedo, -1, "rock_albedo.ktx2");
glObjectLabel(GL_FRAMEBUFFER, gbuf, -1, "gbuffer");
glObjectLabel(GL_PROGRAM, prog, -1, "pbr_opaque");
```
Names can appear in driver messages and in tools that read object labels. Wrap in a macro
that compiles out in release.

## 3. Debug groups (pass markers)
```c
glPushDebugGroup(GL_DEBUG_SOURCE_APPLICATION, 0, -1, "Shadow pass");
  ... draws ...
glPopDebugGroup();
```
Each group inherits and scopes the debug-message volume controls. Keep push/pop balanced
(RAII scope object in C++): popping the default group raises `GL_STACK_UNDERFLOW`.

## 4. Inject your own messages
`glDebugMessageInsert(GL_DEBUG_SOURCE_APPLICATION, GL_DEBUG_TYPE_MARKER, 0,
GL_DEBUG_SEVERITY_NOTIFICATION, -1, "level loaded")` puts app events in the same stream.

## Gotchas
- Message text, ids and volume are implementation-defined; test on more than one driver.
- KHR_debug is core from GL 4.3; on older contexts fall back to `glGetError` polling.
- Outside a debug context the level of output is implementation-defined, so do not conclude
  "no errors" from a release context.

## Verify
- [ ] Deliberately bind an invalid texture name: the callback fires and breaks with a stack
      pointing at the bad call.
- [ ] A capture in your graphics debugger shows labelled resources and nested pass groups.
- [ ] Release builds have debug output disabled and labels compiled out.

## Checked

Date: 2026-10-25. Documentation: Khronos OpenGL-Refpages gl4 and OpenGL-Registry (extension texts, xml/gl.xml; both last updated 2026-10-06) and the GLSL 4.60 specification (HTML). Confirmed in KHR_debug and the refpages: initial DEBUG_OUTPUT is TRUE only for a context created with CONTEXT_FLAG_DEBUG_BIT and implementation-defined otherwise; the implementation may call the callback asynchronously and the application must ensure thread safety, DEBUG_OUTPUT_SYNCHRONOUS guarantees in-call delivery; glDebugMessageControl parameters (source, type, severity, count, ids, enabled); glObjectLabel identifier list and negative length meaning null-terminated; glPushDebugGroup groups inherit volume control, GL_STACK_UNDERFLOW on popping the default group; GL 4.3 core (gl.xml). Removed unconfirmed vendor-specific message ids, RenderDoc and macOS claims.
Method: documentation only; no commands were run.
