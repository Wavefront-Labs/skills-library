---
id: creative-arts.animation.blender.clear-custom-split-normals
name: clear-custom-split-normals
category: creative-arts
field: animation
product: blender
tags: [blender, normals, custom-normals, clear-custom-split-normals, custom-split-normals, geometry-data, imported-meshes]
level: practitioner
status: docs-checked
description: "Manage custom split normals data in Blender: Object Data > Geometry Data add/clear, why imported meshes shade wrong, and when to keep custom normals for game exports."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/meshes/properties/custom_data.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/structure.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/mesh/normals.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# clear-custom-split-normals

Goal: control whether a mesh uses authored (custom) normals or Blender's computed ones.

## Geometry Data panel (Object Data properties)

- **Add/Clear Custom Split Normals Data**: *Clear* deletes the custom normals, so shading falls back to smooth/flat plus sharp edges. *Add* creates custom split normals data if none exists yet (the Normals operators then edit it, and it can be transferred).
- The panel is *Geometry Data* in the mesh Object Data properties; the data is stored as the `custom_normal` attribute on the face corner domain.
- Also on the panel: *Clear Sculpt Mask Data*, *Add/Clear Skin Data*, *Clear Sculpt Face Sets*, *Reorder Mesh Spatially*. Clearing data loses it.

## Typical situations

- **Imported meshes**: the FBX importer has a *Custom Normals* option and imports them if available. Clear them to get Blender's computed shading, then use *Shade Auto Smooth* if needed.
- **Game assets** with baked normal maps: keep the custom normals that match the bake. Do not clear before export.
- **Data Transfer of normals** (e.g. foliage, body-to-head seam blending) writes custom normals; clear to undo.

## Python

```python
bpy.ops.mesh.customdata_custom_splitnormals_clear()   # active object, object mode
```

## Gotchas

- Clearing is destructive to authored shading; duplicate first if unsure.
- Modifier-generated custom normals (Weighted Normal, Normal Edit, Data Transfer) live in the stack and are not affected by Clear until applied.

## Verify

After clearing, the *Split Normals* overlay (Viewport Overlays > Normals) shows the computed normals; shading responds to Shade Smooth/Flat.

## Checked

2026-10-27, Blender manual 5.2 (blender-v5.2-release RST: Geometry Data, Custom Split Normals and FBX pages) and the 5.2 Python operator page names. Confirmed: Add/Clear Custom Split Normals Data on the Geometry Data panel (bpy.ops.mesh.customdata_custom_splitnormals_clear); other panel entries (Clear Sculpt Mask Data, Add/Clear Skin Data, Clear Sculpt Face Sets); storage as the custom_normal face-corner attribute; FBX importer Custom Normals option. Removed as unconfirmed: the Auto Smooth requirement before 4.1 and the Normal Edit and Data Transfer undo advice.

Method: documentation only; no commands were run.
