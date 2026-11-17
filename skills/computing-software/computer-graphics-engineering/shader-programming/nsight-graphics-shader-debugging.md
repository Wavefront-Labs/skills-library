---
id: computing-software.computer-graphics-engineering.shader-programming.nsight-graphics-shader-debugging
name: nsight-graphics-shader-debugging
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, shader-debugging, nsight-shader-debugger, nsight-graphics, shader-profiler, frame-debugger, nvidia]
level: practitioner
status: gated
description: "Debug shaders in NVIDIA Nsight Graphics: frame capture, pixel history, the shader debugger with breakpoints and locals, Shader Profiler hotspots and required build flags."
sources: ["https://docs.nvidia.com/nsight-graphics/UserGuide/index.html", "https://developer.nvidia.com/nsight-graphics", "https://docs.nvidia.com/nsight-graphics/AdvancedLearning/index.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shader debugging in Nsight Graphics

## 1. Capture
- Launch the app from Nsight Graphics (Connect > Application Executable), choose the **Frame
  Debugger** activity, press the capture hotkey (default F11).
- Supports D3D11/12, Vulkan, OpenGL (and OpenXR apps). The app must run on an NVIDIA GPU.

## 2. Find the pixel and draw
- **Event list** lists API calls; **Range Profiler / GPU Trace** for timings.
- In the render target viewer, right-click a pixel > **Pixel History** to see every draw that
  touched it, with depth/stencil test results and shader output per fragment.

## 3. Shader debugger
- Requires a recent driver and debug info: DXC `-Zi -Od`, glslang `-gVS`, Slang `-g` (flags from the DXC, RenderDoc and slangc docs; the Nsight requirement itself is gated: unconfirmed, source is paywalled or blocked).
- From Pixel History or the API Inspector, choose "Debug Shader" for a pixel/thread; set
  breakpoints in source, step, inspect locals and registers, and switch warps/threads.
- For compute, pick the thread/group ID to debug.
- Shader Edit & Continue: edit HLSL/GLSL in the capture and see the result immediately (great for
  experimenting with fixes).

## 4. Shader Profiler
Within GPU Trace or the Frame Debugger's Shader Profiler: per-line sampled stall reasons (texture
wait, long scoreboard, math pipe throttle), hottest instructions, register count and occupancy.
Map hot SASS back to source lines with debug info (`-Zi` without `-Od` keeps line tables while
preserving optimisation).

## 5. Tips
- Use object names (D3D12 `SetName`, Vulkan `vkSetDebugUtilsObjectNameEXT`) and debug markers; Nsight shows
  them in the event list (gated: unconfirmed, source is paywalled or blocked).
- If the shader debugger is greyed out, check: debug info present, driver supports the API, and
  the GPU architecture is supported.

## Gotchas
- `-Od` changes timing and code; reproduce perf issues with optimised builds plus line info.
- Nsight's own overhead can mask race conditions; if a bug disappears under capture, suspect
  synchronisation.

## Verify
- [ ] Able to set a breakpoint and inspect a local in a fragment shader of your app.
- [ ] Shader Profiler shows source-level hotspots.

## Checked
- 2026-10-28. Confirmed: DXC `-Zi`/`-Od` (DXC usage page), glslang `-gVS` (RenderDoc page), Slang `-g` (slangc reference). Removed `-Qembed_debug` (not in DXC page).
- Gated: all Nsight UI, hotkey, profiler and API-support claims; the Nsight user guide fetched as an empty stub.
Method: documentation only; no commands were run.
