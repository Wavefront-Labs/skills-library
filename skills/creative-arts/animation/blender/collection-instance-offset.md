---
id: creative-arts.animation.blender.collection-instance-offset
name: collection-instance-offset
category: creative-arts
field: animation
product: blender
tags: [blender, collection-instance, collection-instance-offset, instance-offset, instancing, asset-pivot]
level: practitioner
status: docs-checked
description: "Set where Blender collection instances pivot: Collection Properties > Instancing > Instance Offset, Set Offset from Cursor, and instance empties."
sources:
  - https://docs.blender.org/manual/en/latest/scene_layout/collections/collections.html
  - https://docs.blender.org/manual/en/latest/scene_layout/object/properties/instancing/collection.html
  - https://docs.blender.org/api/current/bpy.types.Collection.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# collection-instance-offset

Goal: collection instances sit on their empty where you place them, positioned around the asset's base.

## The offset

- Every collection has **Instance Offset X, Y, Z** (Properties > Collection tab > Instancing). The manual describes it as a spatial offset of the instanced collection from the original object's origin; Python: `collection.instance_offset`.
- Assets modelled away from the world origin therefore appear away from the instance empty unless the offset compensates.

## Setting it

- Type values into Collection Properties > Instancing > Instance Offset, or
- Use **Set Offset from Cursor**, found in the Collection Specials menu (down arrow) of the Collections panel in Object Properties; place the 3D cursor at the asset's base first.
- Python: `coll.instance_offset = (0.0, 0.0, 0.0)`.

## Instance empties

- `Add > Collection Instance` creates an empty that instances the collection. Duplicating the empty keeps its Instance Collection setting for each copy.
- Object Properties > Instancing > Collection chooses which collection the empty shows.
- To edit the content, use `bpy.ops.object.duplicates_make_real` on the instance; if the collection was linked, the object data stays linked and parent-child relationships do not carry over.

## Linked collections

A linked collection does not appear in the scene until you create an object (the instance empty) that controls where it appears (or link it with *Instance Collections* on). The offset is a property of the collection, so set it in the file that owns the collection.

## Best practice

Model assets at the world origin and leave the offset at zero where possible, so instancing, linking and exports agree; use the offset only for assets you cannot move.

## Verify

Add a Collection Instance at the cursor: the asset sits where intended, and rotating the empty turns it around the intended pivot.

## Checked

Date: 2026-10-27. Documentation: Blender manual 5.3 (scene_layout/collections/collections.rst, scene_layout/object/properties/instancing/collection.rst, files/linked_libraries/link_append.rst) and the current Python API (Collection.instance_offset).
Confirmed: Instance Offset location and fields, Collection Specials entry, empty and Make Instances Real behaviour, linked collection behaviour. Removed unconfirmed claims: a "minus offset" formula, Object > Collection menu entries "Set Offset from Object" and "Set Cursor from Offset", an Outliner "Set Offset from Cursor" entry, Geometry Nodes Collection Info options and nested offset accumulation.
Method: documentation only; no commands were run.
