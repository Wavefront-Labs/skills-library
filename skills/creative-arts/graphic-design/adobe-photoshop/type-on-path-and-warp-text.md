---
id: creative-arts.graphic-design.adobe-photoshop.type-on-path-and-warp-text
name: type-on-path-and-warp-text
category: creative-arts
field: graphic-design
product: adobe-photoshop
tags: [graphic-design, adobe-photoshop, photoshop, photoshop-type, photoshop-type-on-path, warp-text, text-on-path]
level: practitioner
status: draft
description: "Set type along paths and inside shapes in Photoshop, and use Warp Text styles: flipping text across the path, baseline shift, and warping as smart objects."
sources:
  - https://helpx.adobe.com/photoshop/using/creating-type-path.html
  - https://helpx.adobe.com/photoshop/using/warping-type.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Type on a path and warped text in Photoshop

## Type on a path
1. Draw a path with the Pen or a shape tool in **Path** mode (or use a shape layer's path).
2. Type tool, hover the path until the cursor shows a wavy line, click, type.
3. Move along the path: **Path Selection tool** (A), drag the start marker (x) or end marker (o).
   Drag across the path to flip text to the other side.
4. Baseline Shift in the Character panel moves text off the path without flipping.
5. Text in a closed shape: hover inside a closed path (cursor in parentheses) and click for area type.

## Warp Text
- Type tool selected > options bar **Create Warped Text**: Arc, Arch, Bulge, Flag, Wave, Fish,
  Rise, Fisheye, Inflate, Squeeze, Twist; Horizontal/Vertical, Bend and distortions.
- Warp stays live and text editable. Shapes cannot be warped this way - use Edit > Transform > Warp.
- For finer control: convert the type layer to a smart object, Edit > Transform > **Warp** with
  a custom grid (3x3, 5x5) - text still editable inside the smart object.

## Gotchas
- Faux bold/italic and warped text can fail in PDF export as live type; check outputs.
- Heavy Arc warps distort letterforms unevenly - for logos draw in Illustrator instead.
- Circle text: use an ellipse path; start point at 12 o'clock looks deliberate.

## Verify
- [ ] Text is still editable.
- [ ] Letter spacing looks even around curves (track +10 to +50 on tight curves).
