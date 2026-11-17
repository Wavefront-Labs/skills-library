---
id: creative-arts.comics-and-sequential-art.comic-colouring.selecting-by-flat-colour-for-rendering
name: selecting-by-flat-colour-for-rendering
category: creative-arts
field: comics-and-sequential-art
product: comic-colouring
tags: [comic-colouring, flatting, flats, flat-selection, select-by-color, magic-wand, contiguous-off, clipping-masks]
level: practitioner
status: draft
description: "Use flats as selection masks while rendering: magic wand settings (tolerance 0, anti-alias off, contiguous on/off), saving selections, and clipping render layers."
sources:
  - https://openlibrary.org/search?q=DC+Comics+Guide+to+Coloring+and+Lettering+Comics
  - https://helpx.adobe.com/photoshop/using/making-quick-selections.html
  - https://help.clip-studio.com/en-us/First_Topic.htm
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Selecting by flat colour for rendering

**Goal:** paint shadows and highlights inside exact regions without spilling over.

## Magic wand settings (Photoshop names; CSP Auto Select is similar)
- **Tolerance 0** (flats are exact colours).
- **Anti-alias OFF** (flats are aliased; anti-alias adds partial edges).
- **Sample: current layer** with FLATS active (or "Sample all layers" off).
- **Contiguous ON**: select one region; **OFF**: select every region of that colour on
  the page (e.g. all of a character's jacket in every panel).

## Workflow
1. With FLATS active, wand-select the region(s).
2. Switch to a render layer above FLATS and paint shadows/highlights; the selection
   keeps them inside.
3. Deselect, repeat for the next region.

## Faster alternatives
- **Save selections** for recurring regions (Select > Save Selection, or alpha
  channels) per page.
- **Clipping mask / Clip to layer below**: a render layer clipped to a flats layer only
  shows inside the flats' pixels. Combine with separate flats layers per character for
  big jobs.
- Select > Color Range with Fuzziness 0 as an alternative for global selections.

## Edge considerations
- Contract/expand selection by 0-1 px only if your render style needs to stay off the
  line; generally keep it exact and let the Multiply line art cover edges.

## Gotchas
- Anti-alias on: grey halos at shape edges after rendering.
- Selecting on the composite instead of the flats layer: picks up line art.

## Verify
- [ ] Renders stay inside regions at 200% zoom; no halos.
- [ ] Global (non-contiguous) selections used for consistent recolours.
