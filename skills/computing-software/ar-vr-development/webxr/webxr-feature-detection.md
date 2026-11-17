---
id: computing-software.ar-vr-development.webxr.webxr-feature-detection
name: webxr-feature-detection
category: computing-software
field: ar-vr-development
product: webxr
tags: [webxr, webxr-session-request, webxr-feature-detection]
level: practitioner
status: draft
description: "Check support and start an immersive session from a user gesture."
sources: ['https://www.w3.org/TR/webxr/', 'https://immersiveweb.dev/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Detect and request a WebXR session
**Goal:** Check support and start an immersive session from a user gesture.

- `await navigator.xr.isSessionSupported('immersive-vr')`; request with `navigator.xr.requestSession('immersive-vr', {optionalFeatures: [...]})` inside a click handler.
- Requires a secure context (HTTPS or localhost).
- Offer an "Enter VR" button only when supported.

## Gotchas
- requestSession outside a user gesture is rejected.

## Self-check
Button visible only on supporting browsers; session starts on click.
