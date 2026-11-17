---
id: computing-software.ar-vr-development.mobile-and-spatial-ar.visionos-immersive-space
name: visionos-immersive-space
category: computing-software
field: ar-vr-development
product: mobile-and-spatial-ar
tags: [mobile-and-spatial-ar, visionos-spatial, visionos-immersive-space]
level: advanced
status: draft
description: "Present full or mixed immersion with SwiftUI and RealityKit."
sources: ['https://developers.google.com/ar', 'https://developer.apple.com/documentation/arkit']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Open an ImmersiveSpace
**Goal:** Present full or mixed immersion with SwiftUI and RealityKit.

- Declare `ImmersiveSpace(id:)` in the App scene and open it with the `openImmersiveSpace` environment action.
- Choose an `immersionStyle` (mixed, progressive, full) and RealityView content.
- Users can leave via the Digital Crown.

## Gotchas
- Only one ImmersiveSpace is open at a time.

## Self-check
Space opens with content around the user.
