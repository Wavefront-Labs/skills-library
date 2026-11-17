---
id: computing-software.ar-vr-development.mobile-and-spatial-ar.arkit-plane-lidar
name: arkit-plane-lidar
category: computing-software
field: ar-vr-development
product: mobile-and-spatial-ar
tags: [mobile-and-spatial-ar, arkit-world-tracking, arkit-plane-lidar]
level: advanced
status: draft
description: "Configure ARWorldTrackingConfiguration for planes and LiDAR meshes."
sources: ['https://developers.google.com/ar', 'https://developer.apple.com/documentation/arkit']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Plane detection and scene reconstruction
**Goal:** Configure ARWorldTrackingConfiguration for planes and LiDAR meshes.

- `config.planeDetection = [.horizontal, .vertical]`; `config.sceneReconstruction = .mesh` on LiDAR devices (check `supportsSceneReconstruction`).
- Receive anchors in `session(_:didAdd:)`; use `ARMeshAnchor` for geometry.
- `config.frameSemantics` adds people occlusion or scene depth where supported.

## Gotchas
- Check device support before enabling features.

## Self-check
Mesh anchors arrive on a LiDAR device.
