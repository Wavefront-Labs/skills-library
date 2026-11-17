---
id: computing-software.ar-vr-development.webxr.webxr-reference-spaces-features
name: webxr-reference-spaces-features
category: computing-software
field: ar-vr-development
product: webxr
tags: [webxr, webxr-reference-spaces-features]
level: practitioner
status: draft
description: "Request spaces and optional features in the session."
sources: ['https://www.w3.org/TR/webxr/', 'https://immersiveweb.dev/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Request reference spaces and features
**Goal:** Request spaces and optional features in the session.

- `session.requestReferenceSpace('local-floor')`, fall back to `'local'`; `'bounded-floor'` for room scale.
- List feature descriptors in `requiredFeatures` (fail if missing) and `optionalFeatures` (best effort), for example 'hit-test', 'hand-tracking', 'anchors'.
- Check granted features through `session.enabledFeatures` where available.

## Gotchas
- Required features that are missing reject the session request.

## Self-check
Floor-level pose reports a head height of about a metre or more when standing.
