---
id: creative-arts.animation.blender.face-topology
name: face-topology
category: creative-arts
field: animation
product: blender
tags: [blender, face-topology, eye-loops, mouth-loops, character-modeling, edge-flow]
level: advanced
status: docs-checked
description: "Build animation-ready facial topology: concentric eye and mouth loops, nasolabial and cheek flow, pole placement, loop counts for deformation and checking with shape keys."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/meshes/structure.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/retopology.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/tools/poly_build.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# face-topology

Goal: a face mesh that deforms cleanly for blinks, speech and expressions.

## Core loops

- **Eye loops**: concentric rings around each eye (orbicularis oculi). The inner rings form the eyelids; the outer ones let the brow and cheek move.
- **Mouth loops**: concentric rings around the lips (orbicularis oris), continuing as one region from the nose base to the chin.
- **Nasolabial flow**: a loop running from the nostril wing down beside the mouth corner, defining the smile fold.
- **Brow/forehead**: horizontal loops for brow raise wrinkles.

## Poles

Five-edge poles appear where loop systems meet: typically on the cheek between eye and mouth loops, at the nose bridge, and at the jaw corner. Keep them off the lip line and eyelid edges.

## Density

- Give the eyelids enough edges along the lid edge to close cleanly, and a couple of face rows per lid.
- Give the mouth opening enough edges around the lip edge, plus inner lip rows rolling into the mouth bag.
- Stylised low-poly: fewer rings, same pattern.

## Building

Block from a box head or retopologise a sculpt with the Poly Build tool (`creative-arts.animation.blender.poly-build-tool`): lay the eye and mouth rings first, connect them through the cheek with the nasolabial loop, then fill forehead, nose and jaw. Mirror modifier with Clipping throughout.

## Test deformation

Create shape keys (blink, jaw open, smile, oo) with proportional editing or quick sculpt; problems show as pinches and stretched faces. Fix by moving loops, not by adding random edges.

## Gotchas

- Grid-like faces (from subdivided boxes) do not open mouths or close eyes well; loops must be concentric.
- Triangles inside the deforming areas create creases; push them to the back of the head or under the jaw.
- Too many loops early make shape keys tedious; add density only where deformation needs it.

## Verify

Wireframe overlay: rings around eyes and mouth are continuous; shape keys for blink and jaw open look clean with Subdivision on.

## Checked

2026-10-27, Blender manual 5.2 (blender-v5.2-release RST). Confirmed: the Retopology page recommends manual retopology for deformation and lists the Poly Build tool, snapping and the Retopology overlay; Mirror modifier has Clipping. Removed: numeric ring and edge counts. The loop-flow guidance is modelling practice from experience and is not stated in the manual; the numeric counts, ratios and angles that no documentation covers were removed.

Method: documentation only; no commands were run.
