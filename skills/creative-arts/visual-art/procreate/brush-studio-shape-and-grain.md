---
id: creative-arts.visual-art.procreate.brush-studio-shape-and-grain
name: brush-studio-shape-and-grain
category: creative-arts
field: visual-art
product: procreate
tags: [visual-art, procreate, brush-studio, procreate-brushes, brush-shape, brush-grain, moving-grain, texturized-grain, custom-brush, shape-editor, grain-editor]
level: practitioner
status: draft
description: "Build custom Procreate brushes from shape and grain: importing shape and grain sources, moving vs texturized grain, scatter, rotation, scale and depth, and testing in the drawing pad."
sources: ["https://procreate.com/handbook/procreate/brushes/brush-studio-settings/", "https://procreate.com/handbook/procreate/brushes/brush-studio/", "https://procreate.com/handbook"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Brush Studio: shape and grain

**Goal:** make a Procreate brush whose mark and texture you control (Procreate
Handbook, Brush Studio settings: Shape and Grain sections).

## How a Procreate brush works
A stroke is a series of stamps of the **shape** (the outline of each dab), filled
with the **grain** (the texture inside). Spacing, jitter and dynamics (in Stroke
Path and other sections) arrange the stamps.

## Shape
1. Brush Library > + (new brush) opens Brush Studio; or duplicate an existing brush
   and edit the copy.
2. **Shape > Shape source > Edit**: Import from Photos/Files or the Source Library.
   Shapes are greyscale: **white = paint, black = transparent** (use Invert if
   your image is black on white).
3. Shape behaviour: **Scatter** (rotates each stamp randomly), **Rotation**
   (follow stroke vs fixed), **Count** (stamps per dab), **Randomized**, **Azimuth**
   (follows Pencil tilt direction), **Flip X/Y**, **Roundness** (with pressure/tilt).
4. Shape filtering: anti-aliasing options.

## Grain
1. **Grain > Grain source > Edit**: import a seamless greyscale texture (white = paint).
   Use Make Tileable in the Grain Editor to avoid seams.
2. **Moving vs Texturized**:
   - *Moving*: grain rolls along with each stamp (like a paint roller); good for
     organic, consistent texture.
   - *Texturized*: grain stays fixed to the canvas like paper texture; strokes reveal
     the same texture beneath (like pencil on toothy paper).
3. Settings: **Scale**, **Zoom** (follows canvas zoom or not), **Depth**,
   **Movement**, **Rotation**, **Offset jitter**, **Blend mode**, **Brightness/Contrast**.

## Testing
Use the Drawing Pad at the top of Brush Studio; draw light-to-heavy strokes and
curves. Rename the brush in About this brush; sign it.

## Gotchas
- Editing a default brush directly: you lose the original. Duplicate first.
- Non-tileable grain: visible repeating seams.
- Shape image with grey background: unintended square stamps.

## Verify
- [ ] Shape and grain import as intended (white = paint).
- [ ] Grain mode chosen for the effect (moving vs texturized).
- [ ] Brush duplicated and renamed, original kept.
