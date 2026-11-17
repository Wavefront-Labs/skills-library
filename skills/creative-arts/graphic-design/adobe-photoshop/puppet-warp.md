---
id: creative-arts.graphic-design.adobe-photoshop.puppet-warp
name: puppet-warp
category: creative-arts
field: graphic-design
product: adobe-photoshop
tags: [graphic-design, adobe-photoshop, photoshop, photoshop-transform, puppet-warp, smart-objects, pins, mesh-density]
level: practitioner
status: draft
description: "Reposition limbs, hair or ribbons with Puppet Warp: pin placement, mesh density and expansion, pin depth, rotation and keeping it non-destructive on smart objects."
sources:
  - https://helpx.adobe.com/photoshop/using/warp-images-shapes-paths.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Puppet Warp

**Goal:** bend part of an image (arm, tail, ribbon, type) naturally while anchoring the rest.

## Setup
1. Isolate the element on its own layer (transparent surroundings give a cleaner mesh).
2. Convert to **Smart Object** - Puppet Warp becomes a re-editable smart filter.
3. Edit > **Puppet Warp**.

## Options bar
- **Mode**: Normal; Rigid for limbs (less stretch); Distort for perspective-like stretch.
- **Density**: Fewer Points (smooth, fast), Normal, More Points (precise, can kink).
- **Expansion**: grow/shrink mesh beyond edges (2-3 px avoids clipped edges).
- **Show Mesh** off to judge the result.

## Pins
- Click to add pins at joints: anchor pins where nothing should move (shoulder, torso), move pins
  at the extremity (hand). Three pins for a bending limb: base, joint, end.
- Alt/Opt-click a pin to delete; Alt/Opt-drag near a pin to rotate around it; set Rotate to Fixed with an angle.
- **Pin Depth** (+/-) controls which part overlaps when the mesh folds over itself.

## Gotchas
- Stretching more than ~20% distorts texture visibly; retouch or use a different source.
- Background behind the moved limb is revealed - fill it first (Content-Aware Fill) on the background layer.
- Puppet Warp is unavailable on text layers directly - convert the type layer to a smart object.

## Verify
- [ ] Anchored areas did not move (toggle smart filter visibility).
- [ ] No pinched or smeared texture at joints at 100%.
