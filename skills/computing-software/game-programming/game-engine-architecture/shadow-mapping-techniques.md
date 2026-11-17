---
id: computing-software.game-programming.game-engine-architecture.shadow-mapping-techniques
name: shadow-mapping-techniques
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, shadow-mapping, cascaded-shadow-maps, rendering, game-programming]
level: practitioner
status: draft
description: "Implement shadow mapping: depth bias and acne, peter-panning, cascaded shadow maps with stable cascades, PCF filtering, and point and spot light shadows."
sources: ["https://learn.microsoft.com/en-us/windows/win32/dxtecharts/common-techniques-to-improve-shadow-depth-maps", "https://learn.microsoft.com/en-us/windows/win32/dxtecharts/cascaded-shadow-maps"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Shadow mapping

**Goal:** stable, artefact-free real-time shadows within a fixed budget.

## Basic algorithm
1. Render depth from the light (shadow map).
2. In the main pass, transform each pixel to light space; compare its depth with the map: farther =
   in shadow.

## Artefacts and fixes (Microsoft *Common Techniques to Improve Shadow Depth Maps*)
- **Shadow acne:** surfaces self-shadow due to depth precision. Use slope-scaled depth bias in the
  rasteriser (D3D `DepthBias`, `SlopeScaledDepthBias`) and/or normal offset (push sample position
  along the normal by a texel-size factor).
- **Peter-panning:** too much bias detaches shadows; minimise bias, use normal offset, render back
  faces into the map for closed meshes.
- **Aliasing / perspective aliasing:** fit the light frustum tightly to the visible scene.

## Cascaded shadow maps (directional lights)
- Split the view frustum into 3-4 cascades (logarithmic/practical split scheme with lambda ~0.5-0.9).
- Fit each cascade's orthographic projection around its slice.
- **Stabilisation:** fit a bounding sphere (rotation-invariant size) and snap the projection origin
  to shadow-map texel increments, or shadows shimmer as the camera moves.
- Blend between cascades over a band to hide seams; pick cascade by depth or by map bounds.

## Filtering
- Hardware PCF via comparison samplers (`SampleCmpLevelZero`) for 2x2 bilinear; a 3x3-5x5 Poisson or
  Gaussian kernel for softness.
- PCSS for contact-hardening soft shadows (blocker search + variable kernel); VSM/EVSM allow
  pre-filtering but leak light.

## Other light types
- Spot: one perspective shadow map.
- Point: cube map (6 renders) or dual-paraboloid; cache static geometry shadows and update dynamic
  ones only.

## Budget
Shadow atlases with per-light resolution by screen size/importance; update distant cascades every
other frame.

## Verify
- Slowly rotate the camera: no shimmer. Grazing-angle surfaces: no acne; contact points: no peter-panning.
