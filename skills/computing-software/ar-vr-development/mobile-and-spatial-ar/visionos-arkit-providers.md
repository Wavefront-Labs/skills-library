---
id: computing-software.ar-vr-development.mobile-and-spatial-ar.visionos-arkit-providers
name: visionos-arkit-providers
category: computing-software
field: ar-vr-development
product: mobile-and-spatial-ar
tags: [mobile-and-spatial-ar, visionos-arkit-providers]
level: advanced
status: draft
description: "Run an ARKitSession with data providers."
sources: ['https://developers.google.com/ar', 'https://developer.apple.com/documentation/arkit']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Use ARKit providers on visionOS
**Goal:** Run an ARKitSession with data providers.

- Create `ARKitSession`, run providers such as `WorldTrackingProvider`, `HandTrackingProvider`, `PlaneDetectionProvider` (check the current provider list in docs).
- Request authorisation for each data type through `requestAuthorization`.
- Providers only work while an immersive space is open.

## Gotchas
- Authorisation denial must be handled.

## Self-check
Hand anchor updates stream while the space is open.
