---
id: computing-software.computer-graphics-engineering.opengl.opengl-shared-contexts-and-multithreaded-uploads
name: opengl-shared-contexts-and-multithreaded-uploads
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, opengl-context, gl-shared-context, gl-multithreaded-upload, glfencesync, resource-streaming]
level: advanced
status: draft
description: "Create shared OpenGL contexts for a loader thread, upload buffers/textures off the render thread, and hand them over safely with fences."
sources: ["https://registry.khronos.org/OpenGL/specs/gl/glspec46.core.pdf", "https://www.khronos.org/opengl/wiki/OpenGL_and_multithreading", "https://www.glfw.org/docs/latest/context_guide.html#context_sharing"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Shared contexts and multithreaded uploads

**Goal:** stream textures and meshes from a worker thread without stalling the render thread.
GL is single-threaded per context: one context can be current on one thread at a time. Sharing
lets a second context see the same *objects* (buffers, textures, programs, samplers, syncs) but
not *container* objects (VAOs, FBOs, program pipelines, transform feedback), which stay per-context.

## 1. Create the shared worker context
```c
glfwWindowHint(GLFW_VISIBLE, GLFW_FALSE);
GLFWwindow* worker = glfwCreateWindow(1, 1, "", NULL, mainWindow);  // last arg = share
std::thread loader([=]{
    glfwMakeContextCurrent(worker);          // current on THIS thread only
    gladLoadGLLoader((GLADloadproc)glfwGetProcAddress);  // per-context on some platforms (WGL)
    loaderLoop();
});
```
Create both contexts on the main thread (GLFW requires window creation there), then make the
worker current inside the thread. Same pixel format/profile/version on both or sharing fails
(`wglShareLists` returns FALSE, EGL returns `EGL_BAD_MATCH`).

## 2. Upload and fence
```c
// worker thread
GLuint tex; glCreateTextures(GL_TEXTURE_2D, 1, &tex);
glTextureStorage2D(tex, mips, GL_RGBA8, w, h);
glTextureSubImage2D(tex, 0, 0, 0, w, h, GL_RGBA, GL_UNSIGNED_BYTE, pixels);
glGenerateTextureMipmap(tex);
GLsync done = glFenceSync(GL_SYNC_GPU_COMMANDS_COMPLETE, 0);
glFlush();                                   // REQUIRED: else the fence may never reach the GPU
queue.push({tex, done});
// render thread
if (auto j = queue.try_pop()) {
    glWaitSync(j->done, 0, GL_TIMEOUT_IGNORED);   // GPU-side wait, no CPU stall
    glDeleteSync(j->done);
    material.albedo = j->tex;
}
```
The spec (Appendix D) says object changes made in one context are only guaranteed visible in
another after the change is complete (fence) *and* the object is re-bound in the consuming
context. Re-bind (or bind for the first time) after the wait.

## 3. What not to share
- Create VAOs and FBOs on the render thread only; a VAO built on the worker is invisible to the
  renderer.
- Avoid using one object in both contexts concurrently (e.g. writing a buffer the renderer is
  reading); double-buffer or use persistent mapping instead.

## Alternatives
- Single context + persistent-mapped PBO/staging buffer, filled by worker threads with plain
  `memcpy`; only the GL calls stay on the render thread. Often faster and far less driver-buggy.
- Program binaries compiled on a shared context are fine, but `KHR_parallel_shader_compile`
  is simpler for shader warm-up.

## Gotchas
- Some drivers (older Intel, some mobile EGL) serialize shared contexts internally, so you get
  no speedup; measure.
- macOS: shared contexts work but GL is deprecated; prefer Metal for new work.
- Forgetting `glFlush` after `glFenceSync` on the worker deadlocks `glWaitSync` / `glClientWaitSync`.

## Verify
- [ ] Render-thread frame time unchanged while streaming (check with timer queries).
- [ ] KHR_debug shows no errors in either context; textures appear only after the fence signals.
