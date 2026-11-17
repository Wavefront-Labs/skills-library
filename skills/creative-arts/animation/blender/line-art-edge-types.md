---
id: creative-arts.animation.blender.line-art-edge-types
name: line-art-edge-types
category: creative-arts
field: animation
product: blender
tags: [blender, line-art, line-art-edge-types, line-art-contour, line-art-crease, intersection-lines]
level: practitioner
status: docs-checked
description: "Choose which edges Line Art draws in Blender: contour, silhouette, crease angle, material borders, edge marks, intersections, loose and overlapping types."
sources:
  - https://docs.blender.org/manual/en/latest/grease_pencil/modifiers/generate/line_art.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/modifiers/generate/line_art.html#edge-types
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# line-art-edge-types

Goal: the right line set for the style, not a wireframe.

## Edge Types panel (Line Art modifier)

| Type | Draws |
|---|---|
| Contour | edges separating front-facing from back-facing faces; options *Contour*, *Silhouette* (whole source as one) and *Individual Silhouette* (per source object); the silhouette can be inverted |
| Crease | edges whose angle is smaller than *Crease Threshold* |
| Intersections | where faces intersect |
| Material Borders | edges separating faces with different materials |
| Edge Marks | edges marked as Freestyle edges |
| Loose | edges that do not form a face |
| Light Contour | light/shadow separation lines from a *Light Object* (Light Reference subpanel) |
| Cast Shadow | contour lines projected using a light object |

- **Allow Overlapping Types**: an edge with several types gets a separate stroke for each type.
- **Illumination Filtering**: None, Illuminated, Shaded, Illuminated (Enclosed Shapes); it does not affect cast shadow and light contour.
- **Crease on Smooth** lets crease edges show inside smooth surfaces; **Crease on Sharp** lets creases show on sharp edges.

## Crease priority and per-object control

- Crease angle priority: object Line Art *Override Crease* beats the modifier's crease default. Object Properties → Line Art → *Override Crease* with a *Crease* value.
- Object *Usage*: Inherit, Include, Intersection Only, Occlusion Only, Exclude, No Intersection, Force Intersection; *Intersection Priority* decides which object an intersection line is attached to.
- Mark edges in Edit Mode (`Ctrl E` → *Mark Freestyle Edge*) for exact art-directed lines with *Edge Marks*.

## Per-type styling

Use several Line Art modifiers with different edge types, layers and materials. Each modifier runs its own occlusion calculation, so this slows evaluation (see `line-art-baking-performance`).

## Verify

Toggle each type and watch which lines it contributes.

## Checked

2026-10-27 against the Blender 5.2 manual (Line Art Modifier page and Object Properties Line Art page). Confirmed the edge type list and descriptions, Allow Overlapping Types, illumination filtering, crease options and object usage and crease override. Removed the unconfirmed 140 degree crease default, the claim that Edge Marks need no seams, the subdivision gotcha and the intersection flag default.
Method: documentation only; no commands were run.
