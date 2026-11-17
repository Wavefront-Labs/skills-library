---
id: computing-software.computer-graphics-engineering.rendering-techniques.xr-frame-timing-and-performance-targets
name: xr-frame-timing-and-performance-targets
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, xr-rendering, xr-frame-timing, frame-budget, ovr-metrics, dynamic-resolution]
level: advanced
status: docs-checked
description: "Hit XR frame budgets (72/90/120 Hz): per-frame ms targets, CPU and GPU timing tools, reading compositor stats, dynamic resolution and the cheap wins that matter in stereo."
sources: ["https://registry.khronos.org/OpenXR/specs/1.1/html/xrspec.html", "https://github.com/KhronosGroup/OpenXR-Docs/tree/main/specification/sources/chapters/extensions/fb/fb_display_refresh_rate.adoc", "https://github.com/KhronosGroup/OpenXR-Docs/tree/main/specification/sources/chapters/extensions/fb/fb_foveation.adoc", "https://github.com/KhronosGroup/OpenXR-Docs/tree/main/specification/sources/chapters/extensions/meta/meta_foveation_eye_tracked.adoc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# XR frame timing and performance targets

## 1. Budgets
| Refresh | Frame period |
|---|---|
| 72 Hz | 13.9 ms |
| 90 Hz | 11.1 ms |
| 120 Hz | 8.3 ms |
These are 1000 / Hz. Read the real refresh from the runtime: `XrFrameState.predictedDisplayPeriod` in core
OpenXR, and `XR_FB_display_refresh_rate` where supported. The compositor needs part of the period, so keep
headroom and measure on the headset. Consistency beats average fps.

## 2. Measure on device
- **OpenXR**: `XrFrameState.predictedDisplayPeriod` gives the real budget; time between
  xrWaitFrame and xrEndFrame shows whether you are CPU-late.
- Use the vendor's on-device performance tooling for GPU and CPU time; desktop previews tell you little about a
  mobile headset.

## 3. CPU vs GPU bound
GPU-bound: frame time drops when you halve the eye-buffer scale. CPU-bound: draw-call count and
script time dominate; the GPU waits. Stereo doubles vertex work and (without multiview) draw calls.

## 4. Wins that matter most in XR
1. Multiview / single-pass stereo (one draw per object for both views, see the multiview skill).
2. Foveation: `XR_FB_foveation` (fixed) and `XR_META_foveation_eye_tracked` (eye-tracked) where the runtime offers them.
3. Prefer hardware MSAA over heavy post-process AA; avoid full-screen post passes on mobile XR.
4. Baked lighting, few real-time shadow casters, simple shaders on large surfaces.
5. Dynamic resolution: scale the eye buffer from measured GPU time with hysteresis; start from the
   runtime's `recommendedImageRectWidth`/`Height` (`XrViewConfigurationView`).
6. Compositor layers for text/video/UI instead of rendering them into the eye buffer.
7. Keep CPU/GPU headroom so the app does not throttle thermally over a long session.

## Gotchas
- Profiling the desktop preview tells you little about a mobile headset.
- Frame extrapolation such as `XR_FB_space_warp` needs motion vectors and its own depth image submitted per view.

## Verify
- [ ] No missed frames over a long session on target hardware.
- [ ] GPU time leaves headroom at the hottest scene.

## Checked

2026-10-26: OpenXR specification source (KhronosGroup/OpenXR-Docs, main as of 2026-10-16). Confirmed: XrFrameState.predictedDisplayPeriod semantics, XR_FB_display_refresh_rate, XR_FB_foveation and XR_META_foveation_eye_tracked exist in the extension chapters, recommendedImageRectWidth in XrViewConfigurationView, XR_FB_space_warp motion-vector and depth inputs; frame periods are 1000 divided by the refresh rate. Removed the Quest default refresh claim, the practical millisecond budgets, named profiling tools and log tags, the 0.7-1.0 resolution scale, the 1% stale-frame target and the half-rate figure because no readable documentation backs them.

Method: documentation only; no commands were run.
