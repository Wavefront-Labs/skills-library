---
id: computing-software.ar-vr-development.xr-design-and-performance.xr-frame-budget
name: xr-frame-budget
category: computing-software
field: ar-vr-development
product: xr-design-and-performance
tags: [xr-design-and-performance, xr-frame-budget-profiling, xr-frame-budget]
level: practitioner
status: draft
description: "Split the frame budget between CPU, GPU and platform overhead."
sources: ['https://developers.meta.com/horizon/', 'https://www.khronos.org/openxr/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Set a frame budget and content limits
**Goal:** Split the frame budget between CPU, GPU and platform overhead.

- Measure on the lowest target device and record CPU and GPU frame time separately; allow headroom for thermals on mobile headsets.
- Set limits for draw calls, triangles and overdraw per scene from measured values on your device rather than generic numbers.
- Prefer baked lighting, simple shaders and LODs on standalone headsets.

## Gotchas
- Plugged-in PC numbers mean nothing for standalone targets.

## Self-check
Worst-case scene runs for 20 minutes without frame drops or thermal throttling.
