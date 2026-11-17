---
id: creative-arts.animation.blender.metaball-families
name: metaball-families
category: creative-arts
field: animation
product: blender
tags: [blender, metaballs, metaball, metaball-families, metaball-family, base-object, naming]
level: practitioner
status: docs-checked
description: "Group Blender metaballs into families by object name: the base object rule, what the base owns, keeping separate blobs from merging, and listing family members with Python."
sources:
  - https://docs.blender.org/manual/en/5.2/modeling/metas/editing.html
  - https://docs.blender.org/manual/en/5.2/modeling/metas/properties.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# metaball-families

Goal: control which metaball objects merge with each other.

## Rules

- A **family** is defined by the left part of the object name, before the first dot: `Goo`, `Goo.001`, `Goo.drop` are one family; `Lava` is separate. Use the Object Name, not the Metaball data-block name.
- The family is controlled by a **base** metaball object: the one whose object name has no dot (`Goo`).
- The base object determines the basis, the resolution, the threshold and the transformations of the polygonisation, and it owns the material and texture area. The other objects behave as if included in the base.
- The Metaball panel settings (Resolution Viewport/Render, Influence Threshold, Update on Edit) apply to all objects of the active family.
- Transforming the base changes the mesh structure (polygonisation) of the whole family; transforming a child does not. Scaling the base changes the effective resolution of the children too.

## Practical

- Two liquids that must not merge (water and oil): name them as two families (`Water`, `Oil`) with different materials on their base objects.
- Rename an object to move it into another family.
- With several scenes, keep the base in the same scene as the other family members; otherwise objects can appear invisible.

## Python

```python
for ob in bpy.data.objects:
    if ob.type == 'META' and ob.name.split('.')[0] == "Goo":
        print(ob.name)
```

## Gotchas

- Duplicating `Goo` creates `Goo.001`, which is in the same family (often intended, but surprising if you wanted a separate blob).
- Metaballs of different families do not interact.

## Verify

Rename one member to a new base name: it splits off into its own surface.

## Checked

Date: 2026-10-27. Documentation: Blender 5.2 manual (Editing Meta Objects > Object Families; Metaball Properties). Confirmed: family defined by name before the first dot, base object rules, what the base owns, polygonisation behaviour when transforming base vs children, multi-scene hint. Removed as unconfirmed: particle-instance family behaviour, what happens when the base is deleted, view-layer visibility rules and the claim that non-base materials are ignored (the manual only says the base owns the material).
Method: documentation only; no commands were run.
