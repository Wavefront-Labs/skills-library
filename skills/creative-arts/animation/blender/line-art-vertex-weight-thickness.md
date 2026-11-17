---
id: creative-arts.animation.blender.line-art-vertex-weight-thickness
name: line-art-vertex-weight-thickness
category: creative-arts
field: animation
product: blender
tags: [blender, line-art, line-art-vertex-weight, line-art-thickness, weight-transfer, line-weight]
level: practitioner
status: docs-checked
description: "Vary Line Art stroke thickness and opacity: composition line thickness/opacity, vertex weight transfer from mesh groups, and Thickness modifier mapping."
sources:
  - https://docs.blender.org/manual/en/latest/grease_pencil/modifiers/generate/line_art.html
  - https://docs.blender.org/manual/en/latest/grease_pencil/modifiers/deform/thickness.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# line-art-vertex-weight-thickness

Goal: line weight that varies by part (thicker silhouettes, thin interior lines, fading lines).

## Composition

Line Art modifier base options: **Line Radius** (radius given to generated strokes) and **Opacity**. Use separate modifiers per edge type for different base weights.

## Vertex Weight Transfer

1. On the source mesh, assign a vertex group whose name starts with a common text (for example `lineweight`).
2. Line Art → **Vertex Weight Transfer**: *Filter Source* (vertex groups whose name starts with this text are transferred into weight groups on the strokes), *Match Output* (use the same group names) or, with it off, a *Target* group name. If several groups are copied into one target, the highest weight is kept.
3. Add a **Thickness** modifier after Line Art and restrict it with the *Vertex Group* influence filter so the transferred weights limit where it applies. The Thickness modifier has *Uniform Thickness* (absolute) and *Thickness Factor* (value added or subtracted).

## Other variation

- Separate Line Art modifiers or layers per collection or edge type with different *Line Radius*.
- Grease Pencil modifiers share Influence Filters: layer, layer pass, material, material pass, vertex group and custom curve (the curve controls influence along each stroke from start to end).

## Verify

Invert the vertex group filter on the Thickness modifier and confirm the thick and thin regions swap.

## Checked

2026-10-27 against the Blender 5.2 manual (Line Art Modifier page: Composition and Vertex Weight Transfer; Thickness modifier; Grease Pencil modifier influence filters). Confirmed Line Radius, Opacity, Filter Source, Match Output, Target and the highest-weight rule, Thickness modifier fields and the Vertex Group filter. Removed unconfirmed claims about prefix matching across objects, creating the target group first, low-poly coarseness and chaining across objects, and the Noise and curve tapering suggestions.
Method: documentation only; no commands were run.
