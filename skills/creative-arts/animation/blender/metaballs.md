---
id: creative-arts.animation.blender.metaballs
name: metaballs
category: creative-arts
field: animation
product: blender
tags: [blender, metaballs, metaball, implicit-surface, blobby, liquid-blobs, mercury, organic-blockout, convert-to-mesh, resolution, threshold]
level: practitioner
status: docs-checked
description: "Metaballs in Blender: blobby implicit surfaces for drops and organic blockouts: element types, families, Threshold and Resolution, Stiffness, Negative elements, convert to mesh."
sources:
  - https://docs.blender.org/manual/en/5.2/modeling/metas/index.html
  - https://docs.blender.org/manual/en/5.2/modeling/metas/properties.html
  - https://docs.blender.org/manual/en/5.2/modeling/metas/editing.html
  - https://docs.blender.org/manual/en/5.2/modeling/metas/primitives.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# metaballs

Goal: use metaballs for what they do uniquely well (surfaces that merge and split automatically) and know their limits.

## How they work

A metaball object holds **elements** (Ball, Capsule, Plane, Ellipsoid, Cube). Each element is the source of a field that can be positive or negative; the surface is where the combined field reaches the **Influence Threshold**. The structure is a form of constructive solid geometry: cheap in memory but costly to compute.

Metaball objects of one **family** (the object name before the first dot: `Mball`, `Mball.001`) interact. The **base** object (name without a dot) determines the polygonisation, resolution, threshold and transformations, and owns the material and texture area.

## Settings

- Properties > Data > Metaball (whole family): **Resolution Viewport**, **Render**, **Influence Threshold**, **Update on Edit** (Always, Half, Fast, Never).
- Active Element panel (Edit mode, selected element): **Type**, **Stiffness** (green ring), **Radius** (white ring), **Negative**, **Hide**.
- Add > Metaball (`Shift A`) offers the five primitives; more elements can be added to one object in Edit mode.
- See the skills metaball-types, metaball-stiffness, metaball-resolution, metaball-families and metaball-to-mesh for each area in detail.

## Workflows

**Liquid blobs, mercury, lava lamp:** one family, each drop a Ball (own objects are easiest to animate); drops merge when their fields overlap. Preview at the Render resolution once, since it differs from the viewport.

**Organic blockout:** rough a form from Capsule and Ellipsoid elements, then Object > Convert > Mesh and continue with mesh tools. Conversion takes the object's defined resolution into account.

**Merging meshes:** metaballs only blend other metaball elements; they do not blend ordinary meshes.

## Converting

Object Mode > Object > Convert > Mesh on the base object. Afterwards use mesh tools: Limited Dissolve or a Remesh modifier are the manual's suggestions for messy topology (documented for text conversion, equally applicable to other converted geometry).

## Gotchas

- Two families never interact; check object names in the Outliner when blobs refuse to blend.
- Transforming the base changes the polygonisation of the whole family; transforming children does not.
- A negative element is not shown in the viewport (only rings); Stiffness must be slightly above the Threshold to be visible.
- Hiding an element also removes it from the computation.
- With several scenes, keep the base in the same scene as its family.

## Verify

- Two balls dragged together form a smooth neck before touching; changing Threshold changes how strongly they influence each other.
- Converted mesh vertex count reflects the chosen resolution.

## Checked

Date: 2026-10-27. Documentation: Blender 5.2 manual (Metaball introduction, structure, primitives, properties, editing). Confirmed: element types, family and base-object rules, panel settings and Update on Edit modes, ring colours, Negative and Hide behaviour, Convert > Mesh and the resolution rule, CSG description. Corrected: ring colours (Stiffness is the green ring, Radius the white ring); removed as unconfirmed: numeric defaults and element-count limits, particle and Geometry Nodes workflows, UV/volume-shader and modifier-stack claims, Alembic and export statements.
Method: documentation only; no commands were run.
