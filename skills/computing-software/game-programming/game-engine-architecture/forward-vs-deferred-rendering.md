---
id: computing-software.game-programming.game-engine-architecture.forward-vs-deferred-rendering
name: forward-vs-deferred-rendering
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, deferred-rendering, forward-plus, rendering, game-programming]
level: practitioner
status: draft
description: "Choose between forward, deferred and Forward+ rendering: G-buffer layouts, light culling, MSAA and transparency trade-offs, and bandwidth on mobile."
sources: ["https://learnopengl.com/Advanced-Lighting/Deferred-Shading", "https://www.3dgep.com/forward-plus/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Forward vs deferred rendering

**Goal:** pick the lighting architecture that fits the game's lights, materials, platform and AA.

## Forward
Each object's shader loops over the lights affecting it. Cheap for few lights, supports MSAA and
transparency naturally, arbitrary materials per object. Cost grows with objects x lights.

## Deferred
1. Geometry pass writes a **G-buffer**: e.g. RT0 albedo+AO (RGBA8), RT1 normal (RGB10A2 octahedral
   encoded), RT2 roughness/metallic/material id (RGBA8), depth.
2. Lighting pass: for each light, shade only pixels it covers (light volumes or tiled/clustered).
Cost scales with pixels x lights covering them, independent of scene complexity. Problems:
- High bandwidth (G-buffer write and read): costly on mobile tile-based GPUs unless kept on chip
  (Vulkan subpasses / Metal tile memory).
- MSAA expensive; usually TAA instead.
- Transparency needs a separate forward pass.
- Material variety limited by G-buffer contents.

## Forward+ / clustered forward
Depth pre-pass, then a compute pass bins lights into screen tiles (2D) or clusters (3D froxels);
forward shading reads only its tile's light list. Many lights, MSAA, transparency and material
freedom. Used by Unity URP (Forward+), many modern engines (Doom 2016 clustered forward).
Clustered deferred also exists (light lists for the deferred lighting pass).

## Decision guide
| Need | Lean towards |
|---|---|
| Mobile, few lights | Forward |
| Many dynamic lights, desktop | Clustered deferred or Forward+ |
| MSAA / VR | Forward or Forward+ |
| Many transparent/complex materials | Forward+ |

## Verify
- GPU capture (RenderDoc, PIX): pass timings and G-buffer bandwidth; light count stress test
  (100, 500, 1000 lights) on each target.
