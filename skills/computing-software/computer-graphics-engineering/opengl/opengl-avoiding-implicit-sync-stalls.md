---
id: computing-software.computer-graphics-engineering.opengl.opengl-avoiding-implicit-sync-stalls
name: opengl-avoiding-implicit-sync-stalls
category: computing-software
field: computer-graphics-engineering
product: opengl
tags: [computer-graphics-engineering, opengl, gl-sync, implicit-sync, glfinish, cpu-gpu-stall, gl-performance]
level: advanced
status: draft
description: "Find and remove hidden CPU-GPU synchronisation in OpenGL: glGet* queries, readbacks, buffer/texture updates in use, glFinish and query results."
sources: ["https://www.khronos.org/opengl/wiki/Synchronization", "https://www.khronos.org/opengl/wiki/Buffer_Object_Streaming", "https://developer.nvidia.com/content/how-modern-opengl-can-radically-reduce-driver-overhead-0"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Avoiding implicit sync stalls in OpenGL

GL is asynchronous: commands queue up and the GPU runs one to three frames behind. Any call
that needs a GPU result *now* forces the CPU to wait for the queue to drain (a "pipeline stall"),
often costing several milliseconds.

## Calls that stall
| Call | Why | Replacement |
|---|---|---|
| `glReadPixels` to client memory | needs finished rendering | PBO + fence, read N frames later |
| `glGetBufferSubData`, map without UNSYNCHRONIZED of a buffer in flight | waits for GPU use | persistent mapping + fences, ring buffers |
| `glBufferSubData` / `glTexSubImage` on a resource the GPU is still reading | driver must wait or copy | orphaning, multi-buffering |
| `glGetQueryObject*(GL_QUERY_RESULT)` | waits for the query | check `GL_QUERY_RESULT_AVAILABLE`, read later, query buffers |
| `glClientWaitSync` with a long timeout on a recent fence | by design | wait on fences 2-3 frames old |
| `glFinish` | drains everything | remove (debug only), or use fences |
| `glGetError` (on some drivers, in multithreaded driver mode) | forces sync with driver thread | KHR_debug callback; strip from release |
| `glGetIntegerv`/`glGet*` state queries (NVIDIA threaded optimisation) | round-trip to driver thread | shadow state on the CPU |
| `glGetTexImage`, occlusion results for CPU decisions | GPU data to CPU | conditional rendering, GPU-driven culling |

## Finding them
1. Enable KHR_debug with `GL_DEBUG_TYPE_PERFORMANCE` messages: NVIDIA reports
   "Buffer performance warning: ... being copied/moved" and "Pixel-path performance warning".
2. CPU profiler (Tracy, Superluminal, VTune): look for time inside the driver
   (`nvoglv64.dll`, `atio6axx.dll`, `iris_dri.so`) on calls that should be cheap.
3. Nsight Systems / GPUView: GPU idle gaps aligned with CPU waits on the render thread.

## Fixing the frame structure
- Keep 2-3 frames of per-frame resources (uniform ring segments, staging buffers) and a fence
  per frame; wait only on the fence for frame N-2 before reusing its slot.
- Move every GPU->CPU dependency to "read last-but-one frame's result" (auto exposure,
  occlusion feedback, picking).
- Disable vendor threaded optimisation only for testing; design for it instead (no glGet in hot paths).

## Gotchas
- `glFlush` does not stall; it only submits. A missing `glFlush` after a fence on another
  context causes a deadlock, not a stall.
- Swap with vsync blocks in `SwapBuffers`; that's intentional waiting, don't confuse it with a stall.

## Verify
- [ ] CPU frame time has no spikes inside driver calls; KHR_debug performance warnings are gone.
