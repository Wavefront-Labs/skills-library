---
id: creative-arts.animation.blender.bake-udim-multiple
name: bake-udim-multiple
category: creative-arts
field: animation
product: blender
tags: [blender, bake-udim, bake-multiple-objects, udim, texture-baking, cycles-bake, atlas]
level: advanced
status: docs-checked
description: "Bake into UDIM tiled images and bake many objects at once in Cycles: tiled image setup, filling tiles, shared atlases, per-object images and batching with Python."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/meshes/uv/workflows/udims.html
  - https://docs.blender.org/manual/en/latest/render/cycles/baking.html
  - https://docs.blender.org/api/current/bpy.ops.object.html#bpy.ops.object.bake
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# bake-udim-multiple

Goal: bake hero assets that span several UV tiles, or a whole set of props, in one pass.

## UDIM

1. UVs laid out across tiles (1001, 1002, ...; tile 1001 is the main tile and 1002 sits to its right).
2. Image Editor → *New* with *Tiled* enabled. Manage tiles in Sidebar → Image → UDIM Tiles: *Add Tile* (Number, Count, Label, Fill) and *Fill Tile* to occupy a tile with a generated image. A tile that is not filled is not saved with the image.
3. Use that tiled image in the active, selected Image Texture node.
4. Bake: each texel goes to the tile its UV falls in.
5. Save with the `<UDIM>` token in the filename (`asset_bc.<UDIM>.png`): `<UDIM>` is `1001 + u-tile + v-tile * 10`, giving files such as `asset_bc.1021.png`.

## Many objects

- **Shared atlas**: all objects use materials whose active Image Texture node points to the same image, UVs do not overlap across objects. Select all, bake once with *Clear Image* on.
- **Per-object images**: each material's active node points to its own image; one bake call bakes all selected objects to their own images.
- *Selected to Active* is one active target per bake; for many high/low pairs, loop in Python:

```python
import bpy
pairs = [("crate_high", "crate_low"), ("barrel_high", "barrel_low")]
for hi, lo in pairs:
    for o in bpy.context.view_layer.objects: o.select_set(False)
    bpy.data.objects[hi].select_set(True); low = bpy.data.objects[lo]
    low.select_set(True); bpy.context.view_layer.objects.active = low
    bpy.ops.object.bake(type='NORMAL', use_selected_to_active=True, cage_extrusion=0.02, margin=16)
    img = low.active_material.node_tree.nodes.active.image
    img.filepath_raw = f"//bake/{lo}_n.png"; img.file_format = 'PNG'; img.save()
```

## Gotchas

- Shared materials across objects with different target images are impossible; make materials single-user first.
- *Clear Image* clears the image before baking; turn it off after the first call when accumulating.

## Verify

Each tile file exists and contains content where the UVs are; re-import the asset with the UDIM image and see no missing tile areas; every baked prop image saved with the expected name.

## Checked

2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch) and the 5.2 source UI scripts. Confirmed: Tile numbering, UDIM Tiles panel (Add Tile, Fill Tile, unfilled tiles not saved) and the <UDIM> token formula (UDIMs page); Tiled option on image.new and bpy.ops.object.bake option names type, use_selected_to_active, cage_extrusion, margin (image_ops.cc, object_bake_api.cc). Removed unsupported "silently skipped" and GPU memory claims.

Method: documentation only; no commands were run.
