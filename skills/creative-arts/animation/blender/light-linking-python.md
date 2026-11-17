---
id: creative-arts.animation.blender.light-linking-python
name: light-linking-python
category: creative-arts
field: animation
product: blender
tags: [blender, lighting, light-linking, light-linking-python, light-linking-api, bpy]
level: practitioner
status: docs-checked
description: "Script Cycles light and shadow linking with bpy: create receiver and blocker collections, set include or exclude states and batch-link lights."
sources:
  - https://docs.blender.org/api/current/bpy.types.ObjectLightLinking.html
  - https://docs.blender.org/api/current/bpy.types.CollectionLightLinking.html
  - https://docs.blender.org/api/current/bpy.ops.object.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# light-linking-python

## API

- `obj.light_linking.receiver_collection` / `obj.light_linking.blocker_collection` - Collection or None on the emitter (light or emissive object).
- Membership state: `collection.collection_objects[name].light_linking.link_state` ('INCLUDE' or 'EXCLUDE', default 'INCLUDE'); for child collections `collection.collection_children[name].light_linking.link_state`.

## Example

```python
import bpy
key = bpy.data.objects["KEY"]
col = bpy.data.collections.new("LL_key_char")
key.light_linking.receiver_collection = col
for ob in bpy.data.collections["CHAR"].all_objects:
    col.objects.link(ob)
    col.collection_objects[ob.name].light_linking.link_state = 'INCLUDE'
# shadow linking: hair does not block the key
blk = bpy.data.collections.new("SL_key")
key.light_linking.blocker_collection = blk
hair = bpy.data.objects["hair"]; blk.objects.link(hair)
blk.collection_objects[hair.name].light_linking.link_state = 'EXCLUDE'
```

Operators also exist: `bpy.ops.object.light_linking_receiver_collection_new()`, `light_linking_receivers_link(link_state='INCLUDE')`, `light_linking_blocker_collection_new()`, `light_linking_blockers_link(link_state=...)`, `light_linking_unlink_from_collection()`. They act on the selected objects and the active emitter in context.

## Gotchas

- Name-keyed lookups fail with duplicate-name suffixes (.001) - use objects, not strings, where possible.

## Verify

Run script, then check the Light Linking panel on KEY shows the collection with correct states; render confirms.

## Checked

2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch) and the 5.2 source UI scripts. Confirmed: Property names receiver_collection, blocker_collection, link_state (values and default), collection_objects/collection_children and the five light_linking operators with link_state arguments, from the current Python API docs (5.2-era pages). Removed the unsupported claim about collections surviving a save without a scene link.

Method: documentation only; no commands were run.
