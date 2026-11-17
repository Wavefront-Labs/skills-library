---
id: creative-arts.animation.blender.line-art-source
name: line-art-source
category: creative-arts
field: animation
product: blender
tags: [blender, line-art, line-art-source, line-art-collection, line-art-usage, object-line-art]
level: practitioner
status: docs-checked
description: "Set what Line Art reads: scene, collection or object source, per-object/collection usage (include, exclude, occlusion only, intersection only) and multiple modifiers."
sources:
  - https://docs.blender.org/manual/en/latest/grease_pencil/modifiers/generate/line_art.html
  - https://docs.blender.org/manual/en/latest/scene_layout/object/properties/line_art.html
  - https://docs.blender.org/manual/en/latest/scene_layout/collections/collections.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# line-art-source

Goal: draw lines for exactly the right geometry while everything else still occludes correctly.

## Source Type (modifier)

Needs an active camera; lines are generated only on portions visible from it (or from a *Custom Camera* in Geometry Processing).
- **Scene**: all visible objects. Add → Grease Pencil → *Scene Line Art* creates an empty Grease Pencil object with a Line Art modifier referencing each scene object.
- **Collection**: only the chosen collection (*Collection Line Art*); *Invert Collection Filtering* selects everything except that collection.
- **Object**: one object (*Object Line Art*); supported types are Mesh, Text, Curve, Surface and Curves.
*Layer* and *Material* choose where the strokes go. The manual notes Line Art still loads and calculates the entire visible scene for correct occlusion unless a Usage property says otherwise.

## Usage overrides

Object Properties → Line Art → Usage (overrides the parent collection), and Collection Properties → Line Art → Usage:

| Usage | Effect |
|---|---|
| Inherit (object only) | follows the parent collection |
| Include | generates feature lines |
| Occlusion Only | only occludes existing lines; its geometry stays invisible |
| Exclude | not loaded at all |
| Intersection Only | only intersection lines; geometry stays invisible |
| No Intersection | no intersection lines on itself or with other objects |
| Force Intersection | intersection lines even with objects that disabled them |

## Patterns

- Characters: one Collection source per character with its own layer and material; environment set to Occlusion Only so it hides lines behind it without drawing any.
- *Instanced Objects* (Geometry Processing) loads particles and other instanced objects, with a performance impact when there are many.

## Gotchas

- Several Line Art modifiers each run the full occlusion calculation, so many collection sources slow evaluation (see `line-art-baking-performance`).
- Without an active camera nothing is generated.

## Verify

Switch an object's Usage between Include and Occlusion Only: its own lines vanish but it still hides lines behind it.

## Checked

2026-10-27 against the Blender 5.2 manual (Line Art Modifier, Grease Pencil Primitives, Object Properties Line Art and Collections pages). Confirmed source types, supported object types, Add menu entries and all Usage values. Removed unconfirmed claims about render-hidden versus viewport-hidden objects, linked rigs and scene source speed.
Method: documentation only; no commands were run.
