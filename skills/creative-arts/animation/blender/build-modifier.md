---
id: creative-arts.animation.blender.build-modifier
name: build-modifier
category: creative-arts
field: animation
product: blender
tags: [blender, build-modifier, sort-elements, modifiers, animation, face-order, reveal]
level: practitioner
status: verified
description: "Animate a mesh assembling or disintegrating face by face with Blender's Build modifier: start frame, length, reversed, randomize/seed, and controlling order with Sort Elements."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/build.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/mesh/sort_elements.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# build-modifier

Goal: a mesh that appears (or vanishes) face by face over a frame range with no keyframes, for logo builds or a progressive reveal. For Grease Pencil strokes use the GP Build modifier instead (see `grease-pencil-modifiers-fx`).

## Settings

- **Start Frame** (default 1): frame where building starts.
- **Length** (default 100): number of frames over which the object is rebuilt.
- **Reversed**: runs the effect backwards, a "deconstruction" effect.
- **Randomize** + **Seed**: random build order; the order is always the same for a given seed and mesh.

## Controlling order

By default faces appear in the order they are stored in memory (normally creation order). Change the stored order in Edit Mode with **Mesh > Sort Elements...**:

- *View Z Axis*: along the active view's Z axis, farthest to nearest.
- *View X Axis*: along the view's X axis, left to right.
- *Cursor Distance*: nearest to farthest from the 3D cursor.
- *Material* (by material slot index), *Selected* (selected elements first), *Randomize*, *Reverse*.
- The redo panel has **Elements** (vertices, edges or faces), **Reverse** and **Seed**. Choose *Faces* for Build.

Sort first, then leave Randomize off on the modifier.

## Instancing use

A vertices-only mesh with a Build modifier can be an Instancing Vertices emitter, so a collection of objects appears progressively. The manual presents this as an art-directable alternative to particles.

## Verify

Scrub the timeline: at Start Frame nothing is visible (or everything if Reversed); after Length frames everything is present, in the intended order.

## Checked

Date: 2026-10-27. Documentation release: Blender manual, 5.2 release branch (modifier and Sort Elements pages). Confirmed: Start Frame, Length, Reversed, Randomize, Seed; the menu path Mesh > Sort Elements and its sort types and their directions; default order is storage order. Removed unconfirmed recipes, and the non-existent "View Y Axis" option.
Run check, 2026-11-01, Blender 4.5.14 LTS headless: a cube with Start 10 and Length 6 showed 0 faces at frames 1 and 10, 3 at frame 13 and 6 from frame 16; Reversed ran it backwards (6, 6, 3, 0); the same seed gave the same vertices twice and another seed a different set; a vertices-only mesh built 0, 5 and 10 vertices at frames 1, 6 and 11 and can be set to Instancing Vertices; the Sort Elements operator has the types View Z Axis, View X Axis, Cursor Distance, Material, Selected, Randomize, Reverse and an Elements option (vertex, edge, face).

Method: manual text confirmed from documentation; Build behaviour run headless in Blender 4.5.14.
