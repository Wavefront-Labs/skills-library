---
id: creative-arts.animation.blender.bpy-collections-api
name: bpy-collections-api
category: creative-arts
field: animation
product: blender
tags: [blender, bpy-collections-api, collection-api, view-layer-api, layer-collection, collections, bpy]
level: practitioner
status: verified
description: "Manage collections from Python: create and link, move objects between collections, layer_collection exclude and hide, active collection, and collection visibility flags."
sources:
  - https://docs.blender.org/api/current/bpy.types.Collection.html
  - https://docs.blender.org/api/current/bpy.types.LayerCollection.html
  - https://docs.blender.org/manual/en/latest/scene_layout/collections/collections.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# bpy-collections-api

Goal: organise scenes from code with the same result as dragging things around the Outliner.

## Create, link, move

```python
import bpy
sc = bpy.context.scene
props = bpy.data.collections.get("PROPS") or bpy.data.collections.new("PROPS")
if props.name not in sc.collection.children:
    sc.collection.children.link(props)          # top level; or parent_coll.children.link(props)

def move_to(ob, coll):
    for c in list(ob.users_collection):
        c.objects.unlink(ob)
    coll.objects.link(ob)

move_to(bpy.data.objects["Crate"], props)
```

- An object can live in several collections (`ob.users_collection`); "move" means unlink from all, then link.
- A new object from `bpy.data.objects.new` is in no collection and not in the scene until you link it.
- Removing a collection: `bpy.data.collections.remove(coll)`; its objects survive only if linked elsewhere.

## The two layers of visibility

| Property | Where | Meaning |
|---|---|---|
| `coll.hide_viewport` | Collection (monitor icon) | Disabled in all view layers |
| `coll.hide_render` | Collection (camera icon) | Not rendered |
| `coll.hide_select` | Collection (arrow icon) | Selection disabled in the viewport |
| `layer_coll.exclude` | View layer (checkbox) | Not evaluated in this view layer |
| `layer_coll.hide_viewport` | View layer (eye icon) | Hidden in this view layer only |
| `layer_coll.holdout` | View layer | Mask out the collection's objects in this view layer |
| `layer_coll.indirect_only` | View layer | Objects contribute only indirectly (shadows and reflections) |

Layer collections mirror the collection tree per view layer; find one recursively:

```python
def find_layer_collection(lc, name):
    if lc.name == name:
        return lc
    for child in lc.children:
        hit = find_layer_collection(child, name)
        if hit:
            return hit

vl = bpy.context.view_layer
lc = find_layer_collection(vl.layer_collection, "PROPS")
lc.exclude = False
vl.active_layer_collection = lc     # new objects from operators land here
```

## Gotchas

- `layer_collection.children` only has the direct children; always search recursively.
- Objects of an excluded collection are not part of that view layer: un-exclude first if you need to select or edit them. `select_set` on such an object raises RuntimeError ("can't be selected because it is not in View Layer"). `vl.objects` still lists the object right after you set `exclude`; call `vl.update()` before testing membership.
- Collection colour tags are `coll.color_tag = 'COLOR_01'`..`'COLOR_08'` or `'NONE'` (the identifiers in Collection Color Items).

## Verify

The Outliner shows the same tree your script built; `[c.name for c in ob.users_collection]` lists exactly one collection after a move; render excluded collections and confirm they are absent.

## Checked

2026-10-27 against the Blender 5.2 Python API (Collection, LayerCollection, BlendDataCollections, Collection Color Items). Confirmed: `hide_viewport`, `hide_render`, `hide_select`, `color_tag` identifiers, `exclude`, `holdout`, `indirect_only`, layer `hide_viewport`, `collections.remove`. The `select_set` error on excluded objects was restored after a run (below). Run check, 2026-11-01, Blender 4.5.14 LTS headless: object move by unlink/link gave one `users_collection`; a new object is in no collection and not in the scene; `hide_viewport`, `hide_render`, `hide_select`, `color_tag` (items NONE, COLOR_01 to COLOR_08) and layer `exclude`, `hide_viewport`, `holdout`, `indirect_only` exist; setting `active_layer_collection` made `context.collection` return PROPS; `layer_collection.children` lists only direct children (A shows B, root shows A); `collections.remove` left the object alive with no collection; `select_set` on an excluded object raised RuntimeError; `vl.objects` was stale until `vl.update()`. Unrun: holdout and indirect-only render behaviour, Outliner behaviour.

Method: documentation checked against the manual and API pages; the code was run headless in Blender 4.5.14.
