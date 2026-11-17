---
id: creative-arts.animation.blender.linked-duplicates
name: linked-duplicates
category: creative-arts
field: animation
product: blender
tags: [blender, instancing, linked-duplicates, alt-d, shared-mesh-data, duplicate-linked, make-single-user, link-transfer-data]
level: practitioner
status: docs-checked
description: "Use Alt D linked duplicates in Blender: shared mesh data, Copy on Duplicate preferences, Link/Transfer Data (Ctrl L), Make Single User, and when instancing is better."
sources:
  - https://docs.blender.org/manual/en/latest/scene_layout/object/editing/duplicate_linked.html
  - https://docs.blender.org/manual/en/latest/scene_layout/object/editing/link_transfer/link_data.html
  - https://docs.blender.org/manual/en/latest/editors/preferences/editing.html
  - https://docs.blender.org/manual/en/latest/scene_layout/object/editing/relations/make_single_user.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# linked-duplicates

Goal: edit one model and have every copy update, while each copy keeps its own transform.

## Basics

- `Alt D` (*Duplicate Linked*): new object, **same mesh datablock**. The mesh shows a user count (e.g. `2`) in Object Data.
- `Shift D` (*Duplicate*) follows Preferences > Editing > **Copy on Duplicate**: checked data types are copied, unchecked ones stay linked. Uncheck *Mesh* there to make Shift D share meshes too.
- Transform properties are copied, not linked, so each copy can be moved, rotated and scaled freely. The material is linked, not copied. If the original was animated, the duplicate links to the same Action.

## Link existing objects (`Ctrl L` > Link/Transfer Data)

- *Link Object Data*: make selected objects use the active's mesh (swap a placeholder for the final asset across 200 copies).
- *Link Materials*, *Copy Modifiers* (replaces the modifiers of the selected objects), *Link Instance Collection*, *Link Fonts to Text*.

## Unlink

`Object > Relations > Make Single User`, choosing the data-blocks (Object, Object Data, Materials, ...) in the redo panel, or click the user-count number in Object Data to make it single user.

## Linked duplicates vs instances

- Linked duplicates: each is a real object that shares its data.
- Collection instances and Geometry Nodes instances are not individually editable objects; use them when you need many copies of one asset.

## Gotchas

- Modifiers cannot be applied to objects whose mesh is shared; make the mesh single user first.
- Shape keys are on mesh data → shared by all linked duplicates.
- Edit mode on one copy shows edits on all — expected, but surprises new users.

## Verify

Object Data panel shows the user count; editing one copy's mesh updates the others.

## Checked

2026-10-27, Blender manual 5.2 (blender-v5.2-release RST: Duplicate Linked, Duplicate, Link Data, Make Single User and Preferences > Editing pages). Confirmed: Alt D Duplicate Linked and its shared-data behaviour with copied transforms and linked material and Action; Shift D Duplicate; Preferences > Editing Copy on Duplicate checkboxes; Ctrl L Link/Transfer Data entries (Link Object Data, Link Materials, Link Collections, Link Instance Collection, Link Fonts to Text, Copy Modifiers); Make Single User under Object > Relations with data-block choices. Corrected: the preference is named Copy on Duplicate, and there is no Link Modifiers entry. Removed as unconfirmed: the error message quote, exporter behaviour and the instance performance claim. Shared modifiers on apply follow the Bool Tool documentation, which notes modifiers cannot be applied to shared mesh data.

Method: documentation only; no commands were run.
