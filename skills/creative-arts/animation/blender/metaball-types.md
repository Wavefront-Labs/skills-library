---
id: creative-arts.animation.blender.metaball-types
name: metaball-types
category: creative-arts
field: animation
product: blender
tags: [blender, metaballs, metaball, metaball-types, metaball-negative, metaball-capsule, implicit-surface]
level: practitioner
status: docs-checked
description: "Choose Blender metaball element types: Ball, Capsule, Plane, Ellipsoid, Cube with Size X/Y/Z, and Negative elements, plus Add > Metaball and the Active Element panel."
sources:
  - https://docs.blender.org/manual/en/5.2/modeling/metas/primitives.html
  - https://docs.blender.org/manual/en/5.2/modeling/metas/structure.html
  - https://docs.blender.org/manual/en/5.2/modeling/metas/properties.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# metaball-types

Goal: the right element shapes so blobby forms need fewer elements.

## Element types

Add with Add > Metaball (`Shift A`, Object or Edit mode). Change in Edit mode with Properties > Data > Active Element > Type, or the Type selector in the Sidebar Transform panel.

| Type | Underlying structure | Size controls | Resulting surface |
|---|---|---|---|
| Ball | point | none (Radius) | sphere |
| Capsule | straight line | Size X (length) | cylinder with rounded closed ends |
| Plane | rectangle | Size X, Y | flat box with fixed thickness and rounded borders |
| Ellipsoid | ellipsoidal volume | Size X, Y, Z | ellipsoid |
| Cube | box volume | Size X, Y, Z | box with rounded edges |

- Several elements can live in one object (add more while in Edit mode); each has its own shape, rings and settings.
- Radius is the physical size (white ring); Stiffness is the influence range (green ring) (see metaball-stiffness).

## Negative

- *Negative* changes the element's influence from positive (attraction) to negative (repulsion). The manual notes a negative element is not visible in the 3D Viewport, only its rings.
- Hide (Edit mode) hides selected elements and also removes them from the metaball computation.
- Only the active element can be deleted (`X`, `Delete`).

## Verify

Toggle Negative on an element: the surrounding surfaces change; switch Type: position stays and the shape changes.

## Checked

Date: 2026-10-27. Documentation: Blender 5.2 manual (Metaball Primitives, Structure, Properties, Editing). Confirmed: five types and their structures, Size parameters, Add menu and shortcut, Active Element and Transform panel Type selectors, Negative and Hide behaviour, delete rule. Removed as unconfirmed: use-case column, "scaling changes Radius" in Edit mode, carving/"only affects positives" wording, `H` key for Hide, and resolution advice.
Method: documentation only; no commands were run.
