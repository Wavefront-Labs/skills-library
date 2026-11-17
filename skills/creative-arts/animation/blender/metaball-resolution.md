---
id: creative-arts.animation.blender.metaball-resolution
name: metaball-resolution
category: creative-arts
field: animation
product: blender
tags: [blender, metaballs, metaball, metaball-resolution, metaball-threshold, update-on-edit, performance]
level: practitioner
status: docs-checked
description: "Balance metaball quality and speed in Blender: Resolution Viewport vs Render, Influence Threshold, Update on Edit modes, and how the base object's scale affects polygonisation."
sources:
  - https://docs.blender.org/manual/en/5.2/modeling/metas/properties.html
  - https://docs.blender.org/manual/en/5.2/modeling/metas/editing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# metaball-resolution

Goal: smooth metaball surfaces at render time without a frozen viewport.

## Properties > Data > Metaball (applies to the whole family)

- **Resolution Viewport**: resolution of the mesh generated in the 3D Viewport; smaller values are finer. **Render**: resolution used when rendering.
- **Influence Threshold**: the field level at which the surface is computed; global to the group of metaball objects. As it increases, so does the influence each meta has on the others.
- **Update on Edit** (while transforming metas):
  - *Always*: fully display the meta during transformation.
  - *Half*: display at half the viewport resolution during transformation.
  - *Fast*: do not display the meta during transformation.
  - *Never*: never show the meta mesh (it is only visible at render time, so not recommended).
- Use Half or Fast with many elements or very high resolutions.

## Scale relation

The base object controls the polygonisation of the family. Scaling the base changes the mesh structure of its children (the manual's example: scaling the base down raises the children's mesh resolution while the base's drops), so scale elements or apply scale rather than relying on object scale.

## Polishing

- Convert to mesh and add modifiers for smoothing (conversion uses the defined resolution; see metaball-to-mesh).
- Preview at the Render resolution once before final output, since viewport and render meshes differ.

## Gotchas

- Only the base object's (no dot in its name) settings apply to the family.

## Verify

Render a test frame at the target Render resolution; check the viewport stays interactive with Update set to Half or Fast.

## Checked

Date: 2026-10-27. Documentation: Blender 5.2 manual (Metaball Properties, Editing Meta Objects). Confirmed: Resolution Viewport/Render, Influence Threshold description, the four Update on Edit modes, base-object polygonisation and scale behaviour. Corrected: Fast means the meta is not displayed during the transform (not "updates when the transform ends"); the numeric defaults (0.4, 0.2, 0.6), sample resolutions and render-time/motion-blur claims are not in the manual and were removed.
Method: documentation only; no commands were run.
