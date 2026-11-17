---
id: creative-arts.animation.blender.linked-collection-instance
name: linked-collection-instance
category: creative-arts
field: animation
product: blender
tags: [blender, linking, linked-collection-instance, link-collection, collection-instance, proxies, set-dressing]
level: practitioner
status: docs-checked
description: "Dress shots with linked collection instances in Blender: link once, duplicate the instance empty, reload libraries, proxies replaced by overrides, and when to override instead."
sources:
  - https://docs.blender.org/manual/en/latest/files/linked_libraries/link_append.html
  - https://docs.blender.org/manual/en/latest/scene_layout/object/properties/instancing/collection.html
  - https://docs.blender.org/manual/en/latest/files/linked_libraries/library_overrides.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# linked-collection-instance

Goal: place many linked props cheaply, all updating from one source file.

## Workflow

1. `File > Link...`, open the asset .blend, choose the Collection and keep **Instance Collections** enabled. The collection is added as an instance: a single object (an empty) that represents the whole collection, created at the 3D cursor.
2. Move the empty. Duplicate the empty for more copies; the Instance Collections setting is preserved for each empty, so you get multiple copies of linked data easily. `Add > Collection Instance` adds more of any collection.
3. After the source file changes, update with Outliner > Blender File mode > right-click the library > **Reload**, which refreshes the linked data-blocks without reopening your file.
4. Where the instance pivots comes from the source collection's Instance Offset (see `creative-arts.animation.blender.collection-instance-offset`); set it in the file that owns the collection.

A linked collection does not appear in the scene until an object controls where its instance appears.

## Proxies are gone

The old proxy system was deprecated in Blender 3.0 and fully removed in 3.2. Proxies convert to library overrides automatically when loading a file, but results on complex characters are not guaranteed.

## Instance vs override

- Static props and background sets: instance only (no editing needed).
- Need to pose or animate a placement: run *Library Override > Make* on that instance. For a local empty instancing a linked collection, the empty is removed and the collection override is instanced in its place (see `creative-arts.animation.blender.override-hierarchy`).
- To edit the contents without overrides, use `bpy.ops.object.duplicates_make_real` on the instance; for a linked collection the object data stays linked and parent-child relationships do not carry over.

## Gotchas

- Linked data cannot be protected by a Fake User; a custom property pointing at an otherwise unused linked data-block keeps it referenced across saves.
- Exporters may need real objects; check each exporter's instancing handling.
- Circular dependencies between files tend to produce missing links.

## Verify

The Outliner shows one object per instance empty; after Reload, every instance reflects the library change.

## Checked

Date: 2026-10-27. Documentation: Blender manual 5.3 (files/linked_libraries/link_append.rst, files/linked_libraries/library_overrides.rst, scene_layout/object/properties/instancing/collection.rst).
Confirmed: Instance Collections behaviour and cursor placement, empty duplication, Reload location, proxy removal versions, override behaviour on instance empties, Make Instances Real behaviour for linked collections. Removed unconfirmed claims: `Shift-D` and `Alt-D` shortcuts, per-instance colour via Object Info Random, the empty display size note, memory and statistics claims, and duplicate-link behaviour.
Method: documentation only; no commands were run.
