---
id: computing-software.ar-vr-development.unity-xr.ar-anchor-manager
name: ar-anchor-manager
category: computing-software
field: ar-vr-development
product: unity-xr
tags: [unity-xr, unity-ar-anchors-and-images, ar-anchor-manager]
level: advanced
status: draft
description: "Pin content to world positions with ARAnchorManager."
sources: ['https://docs.unity3d.com/Manual/XR.html', 'https://docs.unity3d.com/Packages/com.unity.xr.interaction.toolkit@latest', 'https://docs.unity3d.com/Packages/com.unity.xr.arfoundation@latest']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Create and persist AR anchors
**Goal:** Pin content to world positions with ARAnchorManager.

- `anchorManager.TryAddAnchorAsync(pose)` (AR Foundation 6) or attach an ARAnchor component.
- Cloud/persistent anchors depend on the provider (ARCore Cloud Anchors, ARKit world maps); check subsystem descriptor support.
- Remove anchors you no longer use.

## Gotchas
- Anchors drift less than free poses but still reset when tracking is lost.

## Self-check
Content stays fixed when walking around it.
