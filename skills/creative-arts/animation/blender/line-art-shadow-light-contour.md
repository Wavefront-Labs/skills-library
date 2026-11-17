---
id: creative-arts.animation.blender.line-art-shadow-light-contour
name: line-art-shadow-light-contour
category: creative-arts
field: animation
product: blender
tags: [blender, line-art, line-art-shadow, light-contour, cast-shadow-lines, npr]
level: practitioner
status: docs-checked
description: "Draw light-based lines with Line Art: light reference object, Light Contour and Cast Shadow edge types, shadow region filtering and shadow camera range."
sources:
  - https://docs.blender.org/manual/en/latest/grease_pencil/modifiers/generate/line_art.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# line-art-shadow-light-contour

Goal: light/shadow separation lines and cast-shadow outlines that follow a light.

## Setup

1. Line Art modifier → **Light Reference** subpanel → **Light Object**: the light used to generate Light Contour.
2. Edge Types → Create: enable **Light Contour** (light/shadow separation lines from the light object) and/or **Cast Shadow** (contour lines projected using the light object).
3. **Shadow Camera Size** is the Orthographic Scale of an ortho camera placed at the lamp position and represents the coverage of the shadow "camera"; **Near** and **Far** are its clipping distances. Make it cover the area where shadows are needed.

## Filtering

**Illumination Filtering** (Edge Types panel): None, Illuminated (lines from lit regions), Shaded (lines from shaded regions), Illuminated (Enclosed Shapes) which combines contour, light contour and shadow lines into enclosed shapes. It does not affect cast shadow and light contour lines, since they lie on the border.

## Use with fills

The modifier's *Fill Strokes* option generates filled strokes from detected regions; combine with the enclosed-shapes filter for flat shadow shapes.

## Verify

Move or rotate the light object and confirm the light contour and shadow lines follow it.

## Checked

2026-10-27 against the Blender 5.2 manual (Line Art Modifier page: Edge Types, Light Reference, Fill Strokes). Confirmed Light Object, Light Contour, Cast Shadow, Shadow Camera Size, Near, Far and Illumination Filtering options. Removed unconfirmed claims about sun versus point light handling, "Silhouette Filtering", too-small/too-large shadow camera effects and per-frame cost.
Method: documentation only; no commands were run.
