---
id: creative-arts.animation.blender.instance-on-faces
name: instance-on-faces
category: creative-arts
field: animation
product: blender
tags: [blender, instancing, instance-on-faces, faces-instancing, duplifaces, scale-by-face, object-instancing, tiles]
level: practitioner
status: docs-checked
description: "Instance objects on mesh faces in Blender (Instancing > Faces) with Scale by Face and Inherit Scale: tiles, scales, armour plates, and converting to Geometry Nodes for randomness."
sources:
  - https://docs.blender.org/manual/en/latest/scene_layout/object/properties/instancing/faces.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# instance-on-faces

Goal: one object placed, oriented and sized per face — roof tiles, dragon scales, floor tiles following a curved surface.

## Setup

1. Select the tile, then the emitter (order matters, emitter active), and parent with `Ctrl-P` > Object.
2. Emitter: Properties > Object Properties > **Instancing** > *Faces*.
3. **Scale** scales each instance according to the size of its face; *Inherit Scale* additionally scales the instanced children.
4. The location, orientation and scale of the instances match the faces of the parent. Several children parented to the emitter are all instanced once per face, and subdividing the emitter adds instances.
5. The parent and the original child still show as editable templates in the 3D Viewport but neither is rendered.

The *Make Instance Face* tool converts linked objects (sharing mesh data) into an instancer with a face per object.

## Controlling layout

- The faces define placement: editing the emitter mesh changes where instances go.
- The position of an instance relative to its face depends on the child's position relative to the instancer's origin; this can cause overlap artifacts in the viewport, and moving the instancer origin off the plane of the faces is a documented workaround.
- If the child is not symmetrical, face orientation (vertex order) matters. The manual's workflow: make one square with Instancing Faces on, rotate the face until the orientation is right, then duplicate and move it, finally *Merge by Distance*.

## Geometry Nodes equivalent

`Mesh to Points` (Faces mode) → `Instance on Points` with *Rotation* from `Align Rotation to Vector` (normal) and *Scale* from the Face Area node — adds randomness, selection and collection picking (see `gn-scatter`).

## Gotchas

- Back to separate linked objects with *Make Instances Real* (`duplicates_make_real`).

## Verify

Toggle *Scale*, then scale one emitter face in Edit Mode: its instance resizes with it.

## Checked

2026-10-27, against the Blender 5.3 manual (branch blender-v5.3-release). Confirmed on the Instancing Faces page: Scale and Inherit Scale, parenting order, templates not rendered, Make Instance Face, Make Instances Real, origin-offset workaround and face orientation workflow. Removed unconfirmed claims: option named Scale by Face with a Factor, Sort Elements, Show Instancer toggles, tilt and performance remarks.

Method: documentation only; no commands were run.
