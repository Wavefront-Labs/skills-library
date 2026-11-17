---
id: creative-arts.photography-fine-art.adobe-lightroom.brush-masks-and-auto-mask
name: brush-masks-and-auto-mask
category: creative-arts
field: photography-fine-art
product: adobe-lightroom
tags: [adobe-lightroom, brush-mask, lightroom-masking, auto-mask, dodge-and-burn, local-adjustments, lightroom-classic]
level: practitioner
status: draft
description: "Paint local adjustments in Lightroom Classic with the Brush mask: size, feather, flow, density, Auto Mask and erase, for dodging and burning like a darkroom."
sources: ["https://helpx.adobe.com/lightroom-classic/user-guide.html (Masking; Brush)", "Ansel Adams, The Print (dodging and burning)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Brush masks and Auto Mask

Masking > Brush (`K`). Two brush settings slots (A and B) plus Erase (hold Alt/Option).

## Settings
- **Size**: `[` and `]`. **Feather**: Shift+`[` / Shift+`]`; high feather (70-100) for dodging, low for edges.
- **Flow**: how fast paint builds with repeated strokes. Low flow (20-40) lets you build up gradually like dodging under an enlarger.
- **Density**: the maximum opacity the stroke can reach.
- **Auto Mask**: confines paint to areas similar in colour/tone to where the brush centre is. Use for edges (a building against sky); turn off for broad dodging, otherwise it leaves speckled gaps.
- Pen tablets: pressure sensitivity controls flow.

## Dodge and burn workflow
1. New Brush mask, set Exposure +0.25 (dodge), Flow 25, Feather 90. Paint over areas to brighten.
2. New Brush mask, Exposure -0.25 (burn). Name both.
3. Adjust strength afterwards with the mask's **Amount** slider (scales all its settings).
4. Use Shadows/Highlights inside the mask instead of Exposure to dodge only shadows of a region.

## Gotchas
- Auto Mask on a gradient sky leaves blotches; check with overlay.
- Hundreds of brush strokes slow the catalog and Develop; prefer AI/range masks when possible.
- Erase brush has its own size and feather.

## Verify
- [ ] Overlay shows smooth, feathered coverage with no hard stroke edges; at fit view the dodging is invisible as a technique.
