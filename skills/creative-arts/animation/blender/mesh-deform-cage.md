---
id: creative-arts.animation.blender.mesh-deform-cage
name: mesh-deform-cage
category: creative-arts
field: animation
product: blender
tags: [blender, mesh-deform, cage, modifiers, deform, rigging, binding]
level: practitioner
status: docs-checked
description: "Deform one or several Blender meshes through a closed cage with the Mesh Deform modifier: cage rules, Precision, Dynamic, Bind/Unbind, extra inner cages and known limits."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/deform/mesh_deform.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# mesh-deform-cage

Goal: deform a mesh (or several, such as a head with eyes and teeth) from one simpler cage mesh instead of weighting every object. The modifier lets an arbitrary mesh of any closed shape act as a deformation cage around another mesh. It is reasonably easy to use but binding can be very slow.

## Setup

Add *Mesh Deform* to the target, set **Object** to the cage mesh, then press **Bind**.

- **Vertex Group** (+ Invert): restricts which vertices are deformed; vertices not in the group are not deformed.
- **Precision**: accuracy of the cage mapping when cage points move. Higher values can greatly increase binding time but map more accurately. Unavailable once bound.
- **Dynamic**: takes other mesh-altering features (other modifiers, shape keys) into account when binding, improving deformation quality. Off by default to save memory and time; unavailable once bound.
- **Bind**: links current vertex positions of the modified geometry and the cage. An unbound modifier has no effect.
- **Unbind**: replaces Bind afterwards. The cage keeps its current shape (it does not reset), while the deformed object returns to its pre-bind shape. Save a copy of the cage first if you need its original shape.

## Cage hints (from the manual)

- Cage normals must point outward: they define inside and outside.
- Extra faces inside the cage, loose or as smaller cages (which may overlap the main cage), give extra control, for example two small sphere cages around eyes.
- Significant changes to the whole cage, such as rotating it upside down, can cause noticeable artefacts; a higher Precision reduces them but the limitation cannot be avoided entirely.

## Safety

Binding can freeze Blender and may run out of memory and crash: save the .blend first.

## Driving the cage

The cage is an ordinary mesh, so any way of deforming a mesh works (armature, lattice, hooks, shape keys). The manual's See Also points to the Lattice modifier as an alternative.

## Verify

Move a cage vertex: the bound targets follow smoothly. After Unbind the target returns to its original shape.

## Checked

Date: 2026-10-27. Documentation release: Blender manual, 5.2 release branch (Mesh Deform page). Confirmed all options, bind/unbind behaviour, normals hint, extra cages, artefact warning. Corrected the Dynamic description (about other modifiers and shape keys while binding, not editing the cage later). Removed unconfirmed face counts, Precision default and range, timing figures and error text.
Method: documentation only; no commands were run.
