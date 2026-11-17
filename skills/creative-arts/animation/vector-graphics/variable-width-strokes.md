---
id: creative-arts.animation.vector-graphics.variable-width-strokes
name: variable-width-strokes
category: creative-arts
field: animation
product: vector-graphics
tags: [variable-width-stroke, width-tool, power-stroke, taper, line-weight, brush-lines, vector-drawing]
level: practitioner
status: draft
description: "Create brush-like variable-width lines in vector art: Width tool and profiles, Inkscape Power and Taper Stroke, Harmony pencil lines, and export limits."
sources:
  - https://helpx.adobe.com/animate/user-guide.html
  - https://docs.toonboom.com/
  - https://inkscape.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Variable-width strokes

Uniform strokes look mechanical; line weight that changes along the line gives drawn, inked character.

## By application
- **Illustrator**: the Width tool (Shift+W) changes thickness at points along a stroke; width profiles on the Stroke panel apply a preset (for example, tapered ends). Brushes (calligraphic, art brushes) also vary width.
- **Animate**: includes a Width tool and variable-width profiles for strokes; check the user guide for your version.
- **Inkscape**: Path Effects > Power Stroke and Taper Stroke create variable-width outlines from a path. The result is a filled shape produced by a live effect; Path > Object to Path bakes it.
- **Toon Boom Harmony**: pencil lines are vector shapes with thickness controlled by the pencil tool settings and pressure; the Contour Editor and Pencil Editor tools adjust thickness. See the Harmony drawing documentation.
- **Pressure tablets** give variable width during drawing in most software; check the brush's pressure mapping.

## Export limits
- Plain SVG strokes have only a single width; variable width is not part of the strokes spec. To export, **outline** the stroke (`outlining-strokes-to-fills.md`) or expand the effect to a path.
- Some animation targets (Lottie, game engines) keep only the constant stroke; confirm what the destination supports.

## Practice
1. Taper line ends in the direction of motion (thin at the end of a stroke), and thicken on the shadow side.
2. Keep line weight consistent across a model sheet: define a few weights (heavy outer contour, medium interior, light detail).
3. Test at final output size and the smallest size the show will be seen.

## Verify
- [ ] Line weights follow the model sheet.
- [ ] The export format shows the same line weight as the source.
