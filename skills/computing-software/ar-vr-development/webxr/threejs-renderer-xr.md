---
id: computing-software.ar-vr-development.webxr.threejs-renderer-xr
name: threejs-renderer-xr
category: computing-software
field: ar-vr-development
product: webxr
tags: [webxr, webxr-three-js-integration, threejs-renderer-xr]
level: practitioner
status: draft
description: "Turn on XR in the WebGLRenderer."
sources: ['https://www.w3.org/TR/webxr/', 'https://immersiveweb.dev/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Enable WebXR in three.js
**Goal:** Turn on XR in the WebGLRenderer.

- `renderer.xr.enabled = true`; `document.body.appendChild(VRButton.createButton(renderer))` (or ARButton).
- Use `renderer.setAnimationLoop(render)`; controllers via `renderer.xr.getController(i)` and `getControllerGrip(i)`.
- Use `XRControllerModelFactory` for models.

## Gotchas
- Do not use requestAnimationFrame directly with XR.

## Self-check
Entering VR from the button shows the scene in stereo.
