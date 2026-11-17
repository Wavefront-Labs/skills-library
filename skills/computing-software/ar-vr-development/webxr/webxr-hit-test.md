---
id: computing-software.ar-vr-development.webxr.webxr-hit-test
name: webxr-hit-test
category: computing-software
field: ar-vr-development
product: webxr
tags: [webxr, webxr-hit-test-anchors, webxr-hit-test]
level: practitioner
status: draft
description: "Place objects on real surfaces in immersive-ar."
sources: ['https://www.w3.org/TR/webxr/', 'https://immersiveweb.dev/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Run an AR hit test
**Goal:** Place objects on real surfaces in immersive-ar.

- Request `'hit-test'`, create a source with `session.requestHitTestSource({space: viewerSpace})`.
- Each frame: `frame.getHitTestResults(source)`; use `results[0].getPose(refSpace)`.
- Cancel the source when done.

## Gotchas
- immersive-ar is not available on every browser.

## Self-check
A reticle slides over the floor.
