---
id: computing-software.ar-vr-development.webxr.xr-frame-pose-views
name: xr-frame-pose-views
category: computing-software
field: ar-vr-development
product: webxr
tags: [webxr, xr-frame-pose-views]
level: practitioner
status: draft
description: "Get the pose and per-eye matrices each frame."
sources: ['https://www.w3.org/TR/webxr/', 'https://immersiveweb.dev/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Read viewer pose and views
**Goal:** Get the pose and per-eye matrices each frame.

- `frame.getViewerPose(refSpace)`; iterate `pose.views` using `view.projectionMatrix` and `view.transform`.
- Handle a null pose (tracking lost).
- Use `view.transform.inverse.matrix` for the view matrix.

## Gotchas
- Ignoring null pose throws at tracking loss.

## Self-check
Scene stays world-fixed when the head moves.
