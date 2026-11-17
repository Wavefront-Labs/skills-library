---
id: computing-software.ar-vr-development.xr-design-and-performance.xr-gpu-profiling-tools
name: xr-gpu-profiling-tools
category: computing-software
field: ar-vr-development
product: xr-design-and-performance
tags: [xr-design-and-performance, xr-gpu-profiling-tools]
level: advanced
status: draft
description: "Use frame capture and runtime metrics to find the bottleneck."
sources: ['https://developers.meta.com/horizon/', 'https://www.khronos.org/openxr/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Profile XR GPU and CPU
**Goal:** Use frame capture and runtime metrics to find the bottleneck.

- On Quest-class headsets use the vendor performance overlay/metrics tool and the vendor's frame capture (Meta provides RenderDoc-based tooling) to inspect passes.
- In engines use Unity Profiler/Frame Debugger or Unreal `stat unit`, `stat gpu`, Insights.
- Check CPU-bound versus GPU-bound first, then fix the largest cost.

## Gotchas
- Profile a development build, not the editor.

## Self-check
One measured change cuts the dominant cost and frame time improves.
