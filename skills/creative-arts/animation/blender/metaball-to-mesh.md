---
id: creative-arts.animation.blender.metaball-to-mesh
name: metaball-to-mesh
category: creative-arts
field: animation
product: blender
tags: [blender, metaballs, metaball, metaball-to-mesh, metaball-animation, convert-to-mesh, alembic]
level: practitioner
status: docs-checked
description: "Animate Blender metaballs (element and object transforms, radius, stiffness) and convert them to meshes with Object > Convert > Mesh; Alembic caches for animated results."
sources:
  - https://docs.blender.org/manual/en/5.2/modeling/metas/editing.html
  - https://docs.blender.org/manual/en/5.2/scene_layout/object/editing/convert.html
  - https://docs.blender.org/manual/en/5.2/files/import_export/alembic.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# metaball-to-mesh

Goal: get metaball motion and shapes into a form you can sculpt, simulate on, or export.

## Animating

- Object level: animate each metaball object's transform. Several metaball objects of one family merge like several elements in one object, and each keeps its own object transform keys.
- Element level: Radius and Stiffness (Active Element panel) are properties and can be keyed with `I` over the field; managing many elements inside one object is awkward, so split them into objects of the same family.
- Remember that the base object controls the family's polygonisation: transforming the base changes the mesh structure of the whole family (see metaball-families).

## Convert to mesh

- Object Mode > Object > Convert > **Mesh** converts the selected curve, metaball, surface or text object to a mesh. The defined resolution of the object is taken into account, so set Resolution Viewport/Render deliberately before converting.
- Convert the base object of the family (the one whose name has no dot) to get the family's surface.
- Clean up afterwards with normal mesh tools (for example Merge by Distance, or a Remesh modifier).

## Exporting animation

- Alembic stores computed, baked geometric results (animated vertex positions and transforms). File > Export > Alembic has Frame Start/End and sub-frame sampling options. To export animated blobs, convert or bake them to a mesh first and check the export in a fresh file.
- On import, Alembic adds Mesh Sequence Cache modifiers to time-varying meshes.

## Gotchas

- Converting loses the metaball behaviour: the mesh no longer merges or splits.
- Topology can change every frame, so check any export on a copy before relying on it.

## Verify

Converted mesh vertex count reflects the chosen resolution; re-importing the Alembic file plays the full frame range.

## Checked

Date: 2026-10-27. Documentation: Blender 5.2 manual (Editing Meta Objects, Object > Convert, Alembic). Confirmed: Convert > Mesh scope and resolution rule, base-object polygonisation behaviour, Alembic baked-geometry description, Frame Start/End, Mesh Sequence Cache on import. Removed as unconfirmed: that Alembic export evaluates metaballs directly, FBX/glTF/USD topology statements, hooks and particle-driven animation, Geometry Nodes alternative, motion-blur claims, and the Keep Original redo option for this conversion.
Method: documentation only; no commands were run.
