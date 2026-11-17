---
id: computing-software.ar-vr-development.xr-design-and-performance.xr-comfort-reprojection-framerate
name: xr-comfort-reprojection-framerate
category: computing-software
field: ar-vr-development
product: xr-design-and-performance
tags: [xr-design-and-performance, xr-comfort-reprojection-framerate]
level: practitioner
status: draft
description: "Keep render rate at the display rate to avoid judder."
sources: ['https://developers.meta.com/horizon/', 'https://www.khronos.org/openxr/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hold frame rate and latency
**Goal:** Keep render rate at the display rate to avoid judder.

- Target the headset refresh rate (for example 72, 90 or 120 Hz); the frame budget is 1000 / Hz ms, such as about 13.9 ms at 72 Hz and 11.1 ms at 90 Hz.
- Reprojection (timewarp/spacewarp variants) masks occasional drops but not sustained ones; treat any reprojection use as a defect to fix.
- Reduce motion-to-photon latency by using late pose latching and predicted display time.

## Gotchas
- Sustained half-rate rendering is more comfortable than uneven drops but still a fail.

## Self-check
Profiler shows frame time under budget with 20 percent margin during worst-case scenes.
