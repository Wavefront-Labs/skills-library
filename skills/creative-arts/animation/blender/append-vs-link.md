---
id: creative-arts.animation.blender.append-vs-link
name: append-vs-link
category: creative-arts
field: animation
product: blender
tags: [blender, linking, append, append-vs-link, link-vs-append, append-reuse-data, instance-collections, pipeline]
level: practitioner
status: docs-checked
description: "Decide between Append and Link in Blender: what each copies or references, the Link/Append dialog options (instance collections, localize all) and pipeline rules of thumb."
sources:
  - https://docs.blender.org/manual/en/latest/files/linked_libraries/link_append.html
  - https://docs.blender.org/manual/en/latest/files/asset_libraries/introduction.html
  - https://docs.blender.org/api/current/bpy.types.BlendDataLibraries.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# append-vs-link

Goal: bring data from another .blend in the way that matches who owns it.

## The difference

- **Append** (`File > Append...`): copies the data-blocks into your file with no reference to the originals. You own the copy; source changes never arrive. Appending data you already have linked adds the objects or collections but keeps them linked (uneditable), so existing relationships stay intact.
- **Link** (`File > Link...`): references data in the source file; changes made there arrive the next time the file is reloaded. Linked data-blocks are marked with a chain icon in the Outliner and are initially not editable, including the transform of linked objects. Both are available in all modes except Edit Mode.
- Link and Append can also be done by dragging a .blend onto the Blender window.
- Data from much newer .blend files cannot be linked or appended.

In the File Browser, navigate into the .blend, pick data-blocks by type (Collection, Object, Material, and so on) and use the right-hand panel for options.

## Making linked data editable

- Link a collection with **Instance Collections** on, or object data with **Instance Object Data** on: the content is referenced through an object created in your file (placed at the 3D cursor), and that object can be transformed.
- Use **Library Overrides** for limited editing and animating of the linked data itself (see `creative-arts.animation.blender.override-hierarchy`).
- **Make Local** cuts the link permanently (see `creative-arts.animation.blender.make-local`).

## Dialog options (right-hand panel of the File Browser)

- **Link:** Relative Path, Select, Active Collection (on: add to the active collection of the active view layer; off: a new "Linked Data" collection), Instance Collections, Instance Object Data.
- **Append:** Select, Active Collection (off creates an "Appended Data" collection), Instance Collections, Instance Object Data, **Fake User** (marks appended data-blocks as protected), **Localize All** (also copies all indirectly linked data instead of keeping the links).
- With Instance Collections off, the collection is added as-is, so its content is visible in the Outliner and ready for library overrides.

## Asset Browser import methods

Assets use an Import Method rather than this dialog: the Python enum has `LINK`, `APPEND`, `APPEND_REUSE` (Append (Reuse Data)) and `PACK` (link, then pack into the file). The manual page for Preferences lists Link, Append and Pack; see `creative-arts.animation.blender.asset-library-preferences`.

## Rules of thumb

- Characters, sets, props maintained by another artist: **Link** (collection) plus an override where posing is needed.
- One-off kitbash parts, materials to modify, node groups you will fork: **Append**.
- Linked data cannot take a Fake User; a custom property pointing at an otherwise unused linked data-block keeps it referenced across saves.

## Python

```python
with bpy.data.libraries.load(path, link=True, relative=True) as (src, dst):
    dst.collections = ["CH_hero"]
```

`bpy.data.libraries.load(filepath, link=False, pack=False, relative=False, set_fake=False, recursive=False, reuse_local_id=False, assets_only=False, ...)` also exposes `create_liboverrides` and related keywords (the 5.x signature; Blender 4.5.14 has `load(filepath, link=False, relative=False, assets_only=False, create_liboverrides=False, reuse_liboverrides=False, create_liboverrides_runtime=False)`, without `pack`, `set_fake`, `recursive` and `reuse_local_id`).

## Gotchas

- Circular dependencies (linked data that links back to the current file) tend to produce missing links.
- Scene-level settings such as the rigid body world are not copied when linking objects; link the whole scene and use it as a background set instead.
- Referencing a compressed .blend loads it entirely into memory even if you take a small part.

## Verify

`File > External Data > Report Missing Files` is clean; the Outliner Blender File mode shows the library with the expected data-blocks.

## Checked

Date: 2026-10-27. Documentation: Blender manual 5.3 (blender-v5.3-release branch, files/linked_libraries/link_append.rst and editors/asset_browser.rst) and the current Python API (docs.blender.org/api/current, BlendDataLibraries.load and the Asset Import Method enum).
Confirmed: Link/Append menu names and options, "Linked Data"/"Appended Data" collections, Fake User and Localize All, the load() signature, the four import-method enum values. Removed unconfirmed claims: a Re-Use Data checkbox in the Link/Append dialog and Instance Collections being on by default for Link.
Run note, 2026-11-01, Blender 4.5.14 LTS headless: `libraries.load(link=True)` returned `None` for a name that is not in the file and set `library.filepath` on the others; linked objects were not in the scene until linked to a collection; `make_local()` returned the local object with `library` None; a linked collection instanced through an Empty (`instance_collection`) and `override_hierarchy_create` produced an override with `override_library` set; `assets_only=True` listed only marked assets; `wm.append` and `wm.link` have `link`, `do_reuse_local_id`, `clear_asset_data`, `autoselect` and `active_collection`.
Method: documentation checked against the manual and API pages; part of the claims were run headless in Blender 4.5.14 (see the run note), but other claims describe Blender 5.x features that 4.5.14 does not have, so the status stays docs-checked.
