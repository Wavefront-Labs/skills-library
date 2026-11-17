---
id: computing-software.ar-vr-development.unity-xr.ar-mesh-manager-lidar
name: ar-mesh-manager-lidar
category: computing-software
field: ar-vr-development
product: unity-xr
tags: [unity-xr, ar-mesh-manager-lidar]
level: advanced
status: draft
description: "Generate a mesh of the surroundings where supported."
sources: ['https://docs.unity3d.com/Manual/XR.html', 'https://docs.unity3d.com/Packages/com.unity.xr.interaction.toolkit@latest', 'https://docs.unity3d.com/Packages/com.unity.xr.arfoundation@latest']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Scan the environment with ARMeshManager
**Goal:** Generate a mesh of the surroundings where supported.

- Add ARMeshManager with a MeshFilter prefab; set normals/colliders as needed.
- ARKit LiDAR devices and some headsets support it; check descriptor.
- Use mesh colliders for physics against the real world.

## Gotchas
- Meshes can be heavy; limit density.

## Self-check
Ball bounces on real-world mesh.
