---
id: computing-software.ar-vr-development.webxr.webxr-emulation-testing
name: webxr-emulation-testing
category: computing-software
field: ar-vr-development
product: webxr
tags: [webxr, webxr-emulation-testing]
level: practitioner
status: draft
description: "Use emulators to develop without a headset."
sources: ['https://www.w3.org/TR/webxr/', 'https://immersiveweb.dev/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Test WebXR without hardware
**Goal:** Use emulators to develop without a headset.

- Browser DevTools has a WebXR emulator in some browsers; the Immersive Web Emulation Runtime and Meta's Immersive Web Emulator extension are options (confirm current names).
- Serve over HTTPS (local certificates) for device testing; use port forwarding for Android Chrome.
- Test on real device before release.

## Gotchas
- Emulators skip performance realism.

## Self-check
App enters a session and responds to emulated controllers.
