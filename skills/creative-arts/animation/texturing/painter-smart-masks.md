---
id: creative-arts.animation.texturing.painter-smart-masks
name: painter-smart-masks
category: creative-arts
field: animation
product: texturing
tags: [smart-masks, painter-layers, substance-painter, mask-presets, shelf, reusable-masks, procedural-masks, studio-library]
level: practitioner
status: draft
description: "Create and reuse Substance 3D Painter smart masks: saving mask stacks to the shelf, parameter exposure, and keeping a studio library consistent across assets."
sources:
  - https://helpx.adobe.com/substance-3d-painter/painting/masking-and-effects.html
  - https://helpx.adobe.com/substance-3d-painter/interface/shelf.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Smart masks

**Goal:** reusable mask recipes (edge chips, cavity dust, sun-bleach top faces) that adapt to any mesh,
so the whole show's assets share a consistent wear language.

## Make one

1. Build a mask stack on a layer or folder: generator + levels + grunge fill + blur.
2. Right-click the mask - **Create smart mask**. It is saved to the shelf under Smart masks.
3. Name with the show prefix and purpose: `SHOW_edge_chips_light`, `SHOW_cavity_dust`.

## Apply

Drag a smart mask from the shelf onto a layer or folder's mask slot. Because it is driven by mesh maps
(curvature, AO, position), it recomputes for each asset.

## Studio library

- Point every artist's shelf to a shared library folder (Preferences - Libraries / shelf paths) with the
  show's smart masks and smart materials, read-only for artists, curated by the look-dev lead.
- Version names when changing a mask; existing projects keep the old instance (smart masks are copied
  into the project, not linked).

## Smart masks vs smart materials

- Smart mask: only "where" (mask stack).
- Smart material: "what and where" (fill layers with their masks): see
  `creative-arts.animation.texturing.texture-painting` for hand-painted stacks and the shelf for materials.

## Gotchas

- Smart masks depend on baked maps existing; on an asset without bakes they look empty or wrong.
- Grunge scale is in UV space unless set to tri-planar; assets with different texel density show
  different grain sizes.
- Manual paint inside a smart mask is saved with the mask; that painting is mesh-specific and should be
  removed before saving as a reusable smart mask.

## Verify

Apply the smart mask to three different assets with bakes: each shows wear in plausible places without
edits; pulling the same mask from the shared shelf on another machine gives identical results.
