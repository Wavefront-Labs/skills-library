---
id: creative-arts.graphic-design.adobe-photoshop.object-selection-and-select-subject
name: object-selection-and-select-subject
category: creative-arts
field: graphic-design
product: adobe-photoshop
tags: [graphic-design, adobe-photoshop, photoshop, photoshop-selections, selection-tools, object-selection-tool, select-subject, select-sky, quick-selection, magic-wand, remove-background, cutout]
level: practitioner
status: draft
description: "Make fast first-pass selections in Photoshop with Select Subject, Object Selection and Select Sky, then clean them up, knowing when AI selection is enough and when it is not."
sources:
  - https://helpx.adobe.com/photoshop/using/making-quick-selections.html
  - https://helpx.adobe.com/photoshop/using/select-subject.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Object selection, Select Subject and Select Sky

**Goal:** a usable selection in seconds, refined only where the job needs it.

## The tools, fastest first
1. **Select > Subject** (or the Select Subject button in the Options bar of any selection
   tool). In Preferences > Image Processing choose **Cloud** for better edges on hair,
   **Device** for speed/offline.
2. **Object Selection tool (W)** - drag a rectangle or lasso loosely around an object; with
   **Object Finder** on, hover to see detected objects highlighted and click to select.
   Shift+click/drag adds, Alt/Option subtracts.
3. **Select > Sky** - for sky replacement masks (or Edit > Sky Replacement directly).
4. **Quick Selection tool** - paint over the area; good for fixing what AI missed.
5. **Magic Wand** - only for flat colour areas (tolerance 10-32, Contiguous on).

## Turn the selection into a mask
Never delete pixels. Click **Add layer mask** with the selection active. To refine:
Select > Select and Mask (hair, fur) - see the select-and-mask skill.

## Judge whether it is good enough
- Put a contrasting solid colour layer underneath and zoom to 100% and 200%.
- Look for: halos (colour fringe from old background), chewed edges on hard products,
  gaps between fingers/arms, missing thin parts (straps, antennae).
- Hard-edged products (bottles, phones, packaging) for e-commerce or print cut-outs:
  AI edges are often slightly soft or wobbly - redo with the Pen tool (path to selection).

## Fix-ups
- Paint the mask: black hides, white reveals, X swaps colours. Use a hard brush on hard
  edges, soft on soft.
- Halo: Layer > Matting > Defringe (rasterised layers) or in Select and Mask use
  **Decontaminate Colors** (creates a new layer, destructive-ish; keep the original).
- Shrink a slightly loose mask: Select and Mask > Shift Edge -10 to -30%.

## Gotchas
- Select Subject picks the most salient thing - with several people it may take all or one.
  Use Object Selection on each instead.
- Selections are lost on deselect; save with Select > Save Selection if you will need it again
  (or keep it as a mask).

## Verify
- [ ] Viewed against black, white and a mid colour at 100%: no halos, no gaps.
- [ ] Selection stored as a layer mask, original pixels intact.
