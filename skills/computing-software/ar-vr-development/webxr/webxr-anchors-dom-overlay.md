---
id: computing-software.ar-vr-development.webxr.webxr-anchors-dom-overlay
name: webxr-anchors-dom-overlay
category: computing-software
field: ar-vr-development
product: webxr
tags: [webxr, webxr-anchors-dom-overlay]
level: advanced
status: draft
description: "Keep content fixed with anchors and show HTML UI in AR."
sources: ['https://www.w3.org/TR/webxr/', 'https://immersiveweb.dev/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Anchors and DOM overlay
**Goal:** Keep content fixed with anchors and show HTML UI in AR.

- `frame.createAnchor(pose, refSpace)` returns an XRAnchor; read `frame.trackedAnchors`.
- DOM Overlay: request 'dom-overlay' with `domOverlay: {root: element}` for HTML controls over the camera view.
- Delete anchors when no longer needed.

## Gotchas
- Anchors can be dropped by the system; re-create gracefully.

## Self-check
Object remains fixed in the room after walking away and back.
