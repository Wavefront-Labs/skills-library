---
id: creative-arts.animation.blender.material-slots
name: material-slots
category: creative-arts
field: animation
product: blender
tags: [blender, shader, material-slots, material-assignment, material-index]
level: practitioner
status: docs-checked
description: "Manage Blender material slots: add slots, assign per face in Edit Mode, Link Data vs Object, copy materials, select by slot, Remove Unused Slots and reuse existing materials."
sources:
  - https://docs.blender.org/manual/en/latest/render/materials/assignment.html
  - https://docs.blender.org/api/current/bpy.types.IDMaterials.html
  - https://docs.blender.org/api/current/bpy.types.MeshPolygon.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# material-slots

## Slots

- Material Properties > Material Slots list: **Add Material Slot** and **Remove Material Slot** buttons; the Material data-block menu creates a new material or picks an existing one for the active slot. Objects have one slot by default.
- Edit Mode: extra buttons appear. Select faces, pick the slot, **Assign**. **Select** and **Deselect** act on the faces assigned to the active slot.
- **Link**: **Data** links the material to the mesh data-block (shared by every object sharing that mesh); **Object** links it to the object, so objects sharing one mesh can have different materials.

## Utilities

- Material Specials menu (down arrow beside the list): Copy Material, Paste Material, **Copy Material to Selected** (copies the assignment from the active to the other selected objects), **Remove Unused Slots**, **Remove All Materials** (clears slots on the active object; material data-blocks remain in the file).
- **Ctrl L** in the 3D Viewport links the selected objects to the active object's material (and other aspects).
- Reusing existing materials: click the sphere beside the material name to pick from the file's materials; the list has a search field.
- Deleting a material: it is only permanently deleted when it has no real users and no Fake User; it disappears after the file is saved and reloaded.

## Python

```python
ob.data.materials.append(mat)               # add a material (new slot)
for p in ob.data.polygons: p.material_index = 0 if p.center.z < 0 else 1
```
`IDMaterials.append(material)` adds a material to the data-block; `MeshPolygon.material_index` is the slot index of a face and `MeshPolygon.center` its centre.

## Gotchas

- Joining objects merges their slot lists; check for duplicated materials afterwards and use Remove Unused Slots (practice).
- Use a smooth Mix Shader inside one material for gradual transitions; slots give hard per-face boundaries.

## Verify

In Edit Mode, Select on a slot highlights the intended faces.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (blender-v5.2-release) render/materials/assignment.rst (slots, Link Data/Object, Edit Mode Assign/Select/Deselect, Material Specials, Ctrl L, reuse, deletion behaviour) and the current Python API (IDMaterials.append, MeshPolygon.material_index and center). Removed: Asset Browser drag-onto-face claim, Geometry Nodes node names, export draw-call claim, and empty-slot rendering colour claims. Method: documentation only; no commands were run.
