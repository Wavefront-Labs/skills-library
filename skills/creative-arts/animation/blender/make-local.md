---
id: creative-arts.animation.blender.make-local
name: make-local
category: creative-arts
field: animation
product: blender
tags: [blender, linking, make-local, localize, linked-libraries, library-overrides, make-single-user]
level: practitioner
status: docs-checked
description: "Cut linked Blender data loose with Make Local: Selected Objects vs Data vs Materials vs All, Outliner Make Local, ID.make_local in Python, and when localising is the wrong fix."
sources:
  - https://docs.blender.org/manual/en/latest/files/linked_libraries/link_append.html
  - https://docs.blender.org/manual/en/latest/editors/outliner/editing.html
  - https://docs.blender.org/api/current/bpy.types.ID.html
  - https://docs.blender.org/api/current/bpy.ops.object.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# make-local

Goal: turn linked data into file-owned data deliberately, once you accept losing future updates from the library.

## What it does

Make Local makes the selected or all external objects local to the current blend-file. Links to the original library file are lost, and the data-blocks become fully editable like ones created in this file.

## Where

- 3D Viewport (Object Mode): `Object > Relations > Make Local...` (`object.make_local`). It affects the selected objects and can also localise their dependencies via **Type**:
  - **Selected Objects** (`SELECT_OBJECT`): only the objects.
  - **Selected Objects and Data** (`SELECT_OBDATA`).
  - **Selected Objects, Data and Materials** (`SELECT_OBDATA_MATERIAL`).
  - **All** (`ALL`): all external objects. The operator can report that orphan library objects were added to the current scene to avoid loss.
- Outliner: context menu > `Data-block > Make Local` turns an externally linked data-block into a local one. It has no options and only affects the selected data-blocks.

## Keeping part of the link

You can link an object, then make just the object local (`Selected Objects`) while its mesh and materials stay linked to the library files and keep updating. This is the pattern the Asset Browser page describes for editable-but-synced assets.

## Python

```python
ob.make_local()                 # ID.make_local(clear_proxy=True, clear_liboverride=False, clear_asset_data=True)
ob.data.make_local()
bpy.ops.object.make_local(type='SELECT_OBDATA_MATERIAL')
```

`ID.make_local` also has `clear_liboverride` (remove library override data from the newly local data) and `clear_asset_data` (so the result is not treated as an asset).

## Follow-ups

- Shared data keeps multiple users after localising; use the user-count button in the data-block selector, or `bpy.ops.object.make_single_user`, before editing one copy.
- Indirectly linked data (for example images, node groups) may remain linked; inspect the Outliner Blender File mode. Appending with **Localize All** copies indirectly linked data as well.

## When not to

- Animators who only need extra controls: use a library override instead (see `creative-arts.animation.blender.override-hierarchy`).
- Shot files: a localised character no longer receives rig fixes from the asset file.

## Verify

`ob.library is None and ob.data.library is None`; the library disappears from the Blender File mode if nothing else uses it.

## Checked

Date: 2026-10-27. Documentation: Blender manual 5.3 (files/linked_libraries/link_append.rst, editors/outliner/editing.rst, editors/asset_browser.rst), the current Python API (ID.make_local, bpy.ops.object.make_local) and the 5.3 release source (object_relations.cc enum labels).
Confirmed: menu paths, Type labels and identifiers, Outliner option behaviour, ID.make_local signature, Localize All meaning. Removed unconfirmed claims: an Outliner "Library Override > Make Local" entry, "All is essentially an append of all libraries", `L` menu history, the collection-membership gotcha, and file-size remarks.
Method: documentation only; no commands were run.
