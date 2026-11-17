---
id: creative-arts.graphic-design.adobe-photoshop.mask-density-and-feather
name: mask-density-and-feather
category: creative-arts
field: graphic-design
product: adobe-photoshop
tags: [graphic-design, adobe-photoshop, photoshop, photoshop-masking, layer-mask, mask-density-feather, properties-panel, mask-edge, invert-mask, disable-mask, mask-refine, view-mask]
level: practitioner
status: draft
description: "Control Photoshop layer masks from Properties (density, feather, invert) and handle masks fast: view, disable, load, move and copy between layers."
sources:
  - https://helpx.adobe.com/photoshop/using/masking-layers.html
  - https://helpx.adobe.com/photoshop/using/adjust-mask-opacity-edges.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mask density, feather and mask management

**Goal:** soften or weaken a mask without repainting it, and handle masks quickly.

## Properties panel (select the mask thumbnail)
- **Density** 100% = the mask fully hides black areas; lower = black areas partly show through.
  Use to dial back the strength of a masked adjustment or reveal a bit of the original.
- **Feather** (px): softens the mask edge non-destructively; change any time. Typical: 0.5-2 px
  for cut-outs, 20-200 px for vignettes and gradual adjustments.
- **Select and Mask...** opens refinement for the mask edge (see select and mask skill).
- **Color Range** button: rebuilds the mask from colour.
- **Invert**: flip hidden/visible.

## Handy mask moves
| Action | Win | Mac |
|---|---|---|
| View the mask alone | Alt+click thumbnail | Opt+click |
| Mask as red overlay | Alt+Shift+click / \ key | Opt+Shift+click / \ |
| Disable/enable mask | Shift+click thumbnail | Shift+click |
| Load mask as selection | Ctrl+click thumbnail | Cmd+click |
| Move mask to another layer | drag thumbnail | drag |
| Copy mask to another layer | Alt+drag | Opt+drag |
| Copy inverted | Alt+Shift+drag | Opt+Shift+drag |
| Fill mask black/white | Alt+Backspace / Ctrl+Backspace (with colours D, X) | Opt+Delete / Cmd+Delete |

## Painting masks well
- Soft round brush at low flow (5-20%) builds gradual transitions; hard brush for edges.
- Paint with grey for partial transparency; or use Overlay brush mode to protect edges.
- Apply filters to masks: Gaussian Blur (extra feathering in places), Minimum/Maximum to
  shrink/grow (Preserve: Roundness).

## Group masks
Mask a group to affect all layers inside at once (e.g. a vignette on a whole composite) while
individual layers keep their own masks.

## Gotchas
- Density and feather in Properties are stored separately from the painted mask; when you
  Apply/rasterise or export to apps that ignore them, results can differ.
- Unlinked masks (chain off) do not follow the layer when moved.

## Verify
- [ ] Mask edges inspected alone (Alt/Option+click) - no unintended grey areas or holes.
- [ ] Feather/density adjustments used instead of repainting where possible.
