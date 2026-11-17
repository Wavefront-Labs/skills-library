---
id: computing-software.ar-vr-development.mobile-and-spatial-ar.arcore-depth-instant
name: arcore-depth-instant
category: computing-software
field: ar-vr-development
product: mobile-and-spatial-ar
tags: [mobile-and-spatial-ar, arcore-session-config, arcore-depth-instant]
level: advanced
status: draft
description: "Enable depth for occlusion and fast placement on supported phones."
sources: ['https://developers.google.com/ar', 'https://developer.apple.com/documentation/arkit']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ARCore Depth API and Instant Placement
**Goal:** Enable depth for occlusion and fast placement on supported phones.

- Check `session.isDepthModeSupported(Config.DepthMode.AUTOMATIC)` then set it in the session Config.
- Instant Placement places content before plane detection finishes (`InstantPlacementMode.LOCAL_Y_UP`).
- Request camera permission before creating the session; use `ArCoreApk.requestInstall`.

## Gotchas
- Depth is unsupported on some devices; treat as optional.

## Self-check
Depth image acquires; instant placement point tracks.
