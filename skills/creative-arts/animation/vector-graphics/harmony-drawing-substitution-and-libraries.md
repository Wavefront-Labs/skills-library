---
id: creative-arts.animation.vector-graphics.harmony-drawing-substitution-and-libraries
name: harmony-drawing-substitution-and-libraries
category: creative-arts
field: animation
product: vector-graphics
tags: [drawing-substitution, harmony-libraries, mouth-swaps, toon-boom-harmony, cut-out-rig, templates]
level: practitioner
status: draft
description: "Swap drawings on a Harmony cut-out rig with drawing substitution: drawing naming, timing columns, mouth sets, Library templates and reuse across scenes."
sources:
  - https://docs.toonboom.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Drawing substitution and libraries (Toon Boom Harmony)

A cut-out part, such as a head or hand, usually has several drawings (angles, mouth shapes, hand poses) held in a single Drawing node. **Drawing substitution** chooses which drawing shows on which frame, by entering a drawing name in the node's timing column.

## Set-up
1. Inside the Drawing node, create a drawing per variant and give each a clear name (for mouths, use the viseme names from `mouth-chart-and-viseme-set-design.md`: `A`, `B`, ... `X`).
2. In the Timeline, expose the drawing you want on each frame by typing its name or number in the cell; hold cells to hold the drawing.
3. Use the Library view and the Drawing Substitution tools to preview and swap quickly while you animate.
4. For the mouth, drive timing from the exposure sheet (`reading-dialogue-onto-an-exposure-sheet.md`).

## Libraries and templates
- The **Library** stores **templates**: a character, a rig or a piece of animation saved so it can be dragged into any scene. Create one by selecting nodes and dragging them to the Library, or using the save-as-template command.
- Use templates for characters, props, and standard rigs, so edits in one place carry through through updating the template and re-importing.
- Name templates consistently, versioned, with the Library folders under the project's naming scheme.
- Note: a template inserted into a scene is a copy; changes to the Library version do not update existing scenes automatically.

## Gotchas
- Inconsistent drawing names break scripts and reuse. Agree on one convention.
- Substitution does not move pivots: draw all variants around the same registration point.
- Colour palettes must be shared between variants, or use palette styles for variants.

## Verify
- [ ] Every variant is named per the convention and registers at the same pivot.
- [ ] A saved template imports into a clean scene and plays correctly.
