---
id: creative-arts.animation.blender.dilate-erode-matte-cleanup
name: dilate-erode-matte-cleanup
category: creative-arts
field: animation
product: blender
tags: [blender, mattes, dilate-erode, matte-cleanup, keying, compositor]
level: practitioner
status: docs-checked
description: "Clean up mattes with the Dilate/Erode node: Size, Type (Steps, Threshold, Distance, Feather), Falloff, opening and closing recipes, and a core/edge matte split."
sources:
  - https://docs.blender.org/manual/en/latest/compositing/types/filter/dilate_erode.html
  - https://docs.blender.org/manual/en/latest/compositing/types/keying/keying.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# dilate-erode-matte-cleanup

Goal: fill holes, remove specks and set edge softness on mattes.

## Dilate/Erode node (Filter category)

Expands or shrinks a mask with a morphological operator. Inputs: **Mask** (greyscale), **Size** (positive dilates, negative erodes), **Type**:
- **Steps**: each pixel takes the maximum (dilate) or minimum (erode) in a surrounding square. Keeps the grey levels; round shapes become squarish. Not iterative: it is performed once whatever the Size.
- **Threshold**: first makes pixels black or white at 50 percent grey, then uses a circle. Loses grey levels; rounds off sharp corners. **Falloff Size** controls how much the edges are blurred afterwards.
- **Distance**: maximum or minimum within a circle. Preserves grey levels; suits rounded shapes.
- **Feather**: blurs the image, with a **Falloff** curve for the blurred edges.
Output: **Mask**.

The Keying node also has built-in Dilate Size, Feather Size and Feather Falloff controls in its Postprocess panel.

## Cleanup recipes

- **Specks in the background**: erode then dilate by the same amount to remove small white dots. Dilate then erode fills small holes in the subject.
- **Edge choke**: a small negative Size removes a fringe from a key.
- **Core and edge split**: a heavily eroded, hard version is the core; the original soft matte is the edge. Combine them with a Math node set to Maximum, so hair keeps its soft edge while the body has no holes.
- **Clamp** the matte (for example with a Math node clamp) so values stay in 0 to 1 after operations.

## Order

Key or roto, then cleanup, then edge choke, then a small blur only if needed, then Set Alpha.

## Gotchas

- Large erode values eat thin detail (hair, fingers). Use the core and edge split instead.
- Steps mode makes square corners and can look jagged on rounded edges; prefer Distance or Feather for final edges.
- Sizes are in pixels, so judge the result at full resolution.

## Verify

Sample the matte: background exactly 0, subject core exactly 1, edge widths as intended. Then check the composite over a contrasting background.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch).
Confirmed: Dilate/Erode inputs Mask, Size, Type (Steps, Threshold, Distance, Feather), Falloff Size, Falloff and their described behaviour; Keying node Dilate and Feather controls. Removed the Edge setting name, the Falloff curve list and the -1 to -2 px value, which the page does not give.
Method: documentation only; no commands were run.
