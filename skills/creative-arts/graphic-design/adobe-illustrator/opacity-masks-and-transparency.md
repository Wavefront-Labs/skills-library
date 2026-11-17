---
id: creative-arts.graphic-design.adobe-illustrator.opacity-masks-and-transparency
name: opacity-masks-and-transparency
category: creative-arts
field: graphic-design
product: adobe-illustrator
tags: [graphic-design, adobe-illustrator, illustrator, opacity-mask, transparency-panel, blending-modes, knockout-group, isolate-blending, gradient-fade, transparency-flattening]
level: practitioner
status: draft
description: "Use the Illustrator Transparency panel: opacity masks for gradient fades, clip and invert options, isolate blending and knockout groups, and how transparency flattens on output."
sources:
  - https://helpx.adobe.com/illustrator/using/transparency-blending-modes.html
  - https://helpx.adobe.com/illustrator/using/flatten-transparency.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Opacity masks and transparency

**Goal:** soft fades, partial visibility and blend-mode effects in vector artwork that print and export
predictably.

## Opacity mask (luminance mask)
1. Put the mask shape on top of the artwork, filled with a **black-to-white gradient** (white = visible,
   black = hidden, greys partly visible). Colour fills use their luminance.
2. Select both, Window > Transparency > **Make Mask**.
3. Options:
   - **Clip** (on by default): area outside the mask object is hidden. Turn off to keep outside visible.
   - **Invert Mask** swaps visible and hidden.
   - Click the mask thumbnail to edit the mask, the art thumbnail to edit the art; the link icon controls
     whether they move together.
4. **Release** returns both objects unmasked.

## Opacity and blending modes
- Opacity and blend mode in the Transparency panel apply to the selected object, group, layer, or a single
  fill or stroke (target it in the Appearance panel).
- **Isolate Blending** (on a group): blend modes inside affect only group members, not artwork below.
- **Knockout Group**: members do not show through each other, only through to the background.
- Multiply on a white-filled object turns white transparent: a quick way to overprint line art on colour.

## Output behaviour
- PDF/X-4 and native AI keep live transparency; PDF/X-1a, EPS and older workflows **flatten** it.
  Use View > **Flattener Preview** and a High Resolution flattener preset; check text and strokes near
  transparency (they may be rasterised or outlined).
- Blend modes with **spot colours** can give unexpected separations; check Window > Separations Preview.
- SVG export supports opacity and masks, but complex masks may rasterise or need simplification.

## Gotchas
- A mask made from a coloured object uses luminance: a saturated red reads as mid-grey, giving partial opacity.
- Scaling art without the mask linked misaligns them.
- Transparency on large textures or effects slows printing; keep fades simple and test-print.

## Verify
- [ ] Fade looks right in Overprint Preview and Flattener Preview.
- [ ] Output PDF matches screen (open in Acrobat Output Preview).
