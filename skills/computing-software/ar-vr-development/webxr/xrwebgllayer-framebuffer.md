---
id: computing-software.ar-vr-development.webxr.xrwebgllayer-framebuffer
name: xrwebgllayer-framebuffer
category: computing-software
field: ar-vr-development
product: webxr
tags: [webxr, webxr-render-loop, xrwebgllayer-framebuffer]
level: practitioner
status: draft
description: "Create a layer and render per view into its framebuffer."
sources: ['https://www.w3.org/TR/webxr/', 'https://immersiveweb.dev/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Render into the XRWebGLLayer
**Goal:** Create a layer and render per view into its framebuffer.

- `new XRWebGLLayer(session, gl)`, `session.updateRenderState({baseLayer})`; make the GL context `xrCompatible: true`.
- In the frame callback bind `layer.framebuffer`, and for each view set the viewport from `layer.getViewport(view)`.
- Drive animation with `session.requestAnimationFrame`, not window.rAF.

## Gotchas
- Contexts not created xrCompatible need `gl.makeXRCompatible()`.

## Self-check
Both eyes draw in the correct viewports.
