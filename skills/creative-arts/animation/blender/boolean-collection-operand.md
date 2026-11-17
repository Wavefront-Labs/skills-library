---
id: creative-arts.animation.blender.boolean-collection-operand
name: boolean-collection-operand
category: creative-arts
field: animation
product: blender
tags: [blender, boolean, collection-operand, exact, modifiers, hard-surface, cutters]
level: practitioner
status: verified
description: "Use a collection as the Boolean modifier operand in Blender so many mesh cutters act through one modifier, and the solver limits that apply to collections."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/booleans.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# boolean-collection-operand

Goal: many cutters handled by one modifier.

## Setup

Boolean modifier > **Operand Type: Collection** > choose the collection. The source is a collection of any number of mesh objects.

- **Operation**: *Difference* cuts the sources out of the modified mesh, *Union* adds them while removing interior faces, *Intersect* keeps only the volume inside the modified mesh and all sources.
- With the **Float** solver, *Intersect* is not allowed for collections (4.5.14 reports: intersect only available using exact solver).
- With the **Exact** solver the collection may be empty, in which case the modifier simply removes the modified mesh's interior (self-intersecting) geometry.
- The Manifold solver works only on manifold meshes.

## Why use it

One modifier replaces several, and adding a cutter is a matter of putting it in the collection (hard-surface workflow: `creative-arts.animation.blender.hard-surface-booleans`).

## Several cut groups

Use more than one Boolean modifier, each with its own collection, when you need different operations (for example one Union and one Difference); the modifier stack order decides which is applied first.

## Tip

Showing the cutters with Wireframe in Properties > Object > Viewport Display (and X-Ray) lets you see the intersection edges while you move them.

## Verify

Move a new mesh object into the collection: the cut appears without touching the modifier.

## Checked

Date: 2026-10-27. Documentation release: Blender manual, 5.2 release branch (Boolean modifier page). Confirmed: Operand Type Collection, operations, Float-solver Intersect restriction, empty collection with Exact. Removed unconfirmed claims about nested collections, non-mesh objects, render visibility and Fast-solver union reliability.

Run check, 2026-11-01, Blender 4.5.14 LTS headless: Boolean with Python: Operand Type has Object and Collection; Operations Intersect, Union, Difference; a two-cutter collection gave Difference 14 faces and Union 18 faces on both Exact and Manifold, and Float with Intersect reported the modifier error above; an empty collection with Exact and Difference left the 6-face cube. Not run: Wireframe and X-Ray viewport display tip and moving objects between collections (UI).

Method: manual text confirmed from documentation; behaviour run headless in Blender 4.5.14.
