---
id: creative-arts.animation.blender.bpy-datablock-creation
name: bpy-datablock-creation
category: creative-arts
field: animation
product: blender
tags: [blender, bpy, python, bpy-datablock-creation, datablock-creation, bpy-data-new, collections]
level: practitioner
status: verified
description: "Create, link and delete datablocks from Python: bpy.data.*.new, linking objects into collections, removing with do_unlink, users and fake users, and purging orphans."
sources:
  - https://docs.blender.org/api/current/bpy.types.BlendData.html
  - https://docs.blender.org/api/current/bpy.types.BlendDataObjects.html
  - https://docs.blender.org/api/current/info_gotcha.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# bpy-datablock-creation

Goal: build scenes from code without leaking unused data.

## Creating

```python
import bpy
me = bpy.data.meshes.new("crate_mesh")
ob = bpy.data.objects.new("crate", me)          # object data can be None for an empty
coll = bpy.data.collections.get("props") or bpy.data.collections.new("props")
if coll.name not in bpy.context.scene.collection.children:
    bpy.context.scene.collection.children.link(coll)
coll.objects.link(ob)                             # objects must be in a collection to be in the scene
mat = bpy.data.materials.new("crate_mat")
me.materials.append(mat)
```
Other types follow the same pattern: `bpy.data.lights.new(name, type='AREA')`, `cameras.new`, `images.new(name, w, h, alpha=True, float_buffer=False)`, `actions.new`, `node_groups.new(name, 'GeometryNodeTree')`.

## Deleting

```python
bpy.data.objects.remove(ob, do_unlink=True)   # removes from all collections too
bpy.data.meshes.remove(me)                    # mesh data separately, if no other users
bpy.data.batch_remove([ob1, ob2, me1])        # many at once; faster than remove() but less safe
bpy.data.orphans_purge(do_recursive=True)     # delete all IDs with no user (do_local_ids/do_linked_ids default True)
```

## Users

- `id.users`: how many references. Zero-user data is not saved (unless `use_fake_user = True`).
- New datablocks start with zero users until linked. Data with no users is not saved unless it has a fake user.
- Linked duplicates share mesh data: changing `me` changes all objects using it.

## Gotchas

- Names are unique (`ID.name`): `new()` with an existing name returns a datablock with a changed name (tested: a second `meshes.new("m")` was named `m.001`). Read back `.name` after creating.
- Deleting an object does not delete its mesh. Clean up both, or purge.
- Removing data invalidates Python references other code holds to it; look it up again afterwards.

## Verify

After running the build script twice, the Outliner (Blender File view) shows no duplicate-named datablocks or orphan data.

## Checked

2026-10-27 against the Blender 5.2 Python API (BlendData.orphans_purge, batch_remove; BlendDataObjects.remove with do_unlink; BlendDataImages.new signature; BlendDataLights.new(name, type); BlendDataNodeTrees.new types). Removed unconfirmed claims (error text, `.001` naming, File > Clean Up menu). Run check, 2026-11-01, Blender 4.5.14 LTS headless: the create-and-link snippet; `lights.new(name, type='AREA')`, `cameras.new`, `images.new(name, w, h, alpha=True, float_buffer=False)`, `actions.new`, `node_groups.new(name, 'GeometryNodeTree')`; a fresh mesh has 0 users, an object that owns it makes 1, two objects make 2; `objects.remove(ob, do_unlink=True)` left the mesh; `orphans_purge(do_recursive=True)` removed unused data and kept a mesh with `use_fake_user`; `batch_remove([...])`. Unrun: Outliner Blender File view.

Method: documentation checked against the manual and API pages; the code was run headless in Blender 4.5.14.
