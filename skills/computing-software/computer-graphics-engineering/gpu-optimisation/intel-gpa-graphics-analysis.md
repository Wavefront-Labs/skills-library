---
id: computing-software.computer-graphics-engineering.gpu-optimisation.intel-gpa-graphics-analysis
name: intel-gpa-graphics-analysis
category: computing-software
field: computer-graphics-engineering
product: gpu-optimisation
tags: [computer-graphics-engineering, gpu-optimisation, gpu-profiling, intel-gpa, intel-gpu, frame-analyzer, graphics-performance-analyzers, integrated-graphics]
level: practitioner
status: draft
description: "Profile on Intel GPUs with Intel GPA: Graphics Monitor launch, Frame Analyzer per-draw metrics, replay experiments (2x2 textures, simple PS) and System Analyzer."
sources: ["https://www.intel.com/content/www/us/en/developer/tools/graphics-performance-analyzers/overview.html", "https://www.intel.com/content/www/us/en/docs/gpa/user-guide/current/overview.html", "https://www.intel.com/content/www/us/en/developer/articles/guide/developer-and-optimization-guide-for-intel-processor-graphics-gen11-api.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Intel GPA

Intel Graphics Performance Analyzers: free suite for D3D11/12, Vulkan and OpenGL on Intel GPUs
(integrated and Arc), with partial support for other vendors in some tools.

## 1. Components
- **Graphics Monitor**: launcher; choose the app, configure capture hotkeys and metrics.
- **System Analyzer**: live metrics overlay/HUD (CPU, GPU, frame time) and real-time experiments.
- **Frame Analyzer**: open a captured frame (stream or single frame) and analyse per draw.
- **Graphics Trace Analyzer**: timeline of CPU threads, GPU queues and present.

## 2. Frame Analyzer workflow
1. Capture a frame (Ctrl+Shift+C default) via Graphics Monitor.
2. Open in Frame Analyzer: bar chart of draws by GPU duration; select ranges by marker.
3. Metrics per draw/range: EU (execution unit) active/stall/idle, thread occupancy, sampler busy,
   L3/memory bandwidth, pixel/vertex counts.
4. **Experiments** (per selected draws): replace textures with 2x2, simple pixel shader, disable
   draws, scissor 1x1 - measure the time difference to isolate texture-bound, shader-bound or
   fill-bound draws without editing code.
5. Shader view with per-instruction statistics; edit shaders and replay.

## 3. Intel-specific considerations
- Integrated GPUs share memory bandwidth with the CPU: bandwidth (render target formats, overdraw)
  often dominates; CPU load affects GPU clocks (shared power budget).
- SIMD8/16/32 dispatch per shader: register pressure changes the SIMD width; GPA shows it.
- Arc discrete: XeSS integration, different cache sizes; check Intel's optimisation guides per
  generation.

## Gotchas
- Metrics availability depends on GPU generation and driver; update both.
- Experiments are approximations (a 2x2 texture also changes cache behaviour); use them to rank
  suspects, then confirm with real changes.

## Verify
- [ ] Bottleneck draws ranked with experiment deltas.
- [ ] Fix confirmed on the Intel target (not only on discrete GPUs).
