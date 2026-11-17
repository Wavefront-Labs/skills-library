---
id: creative-arts.photography-fine-art.adobe-lightroom.non-destructive-dodge-and-burn-layers
name: non-destructive-dodge-and-burn-layers
category: creative-arts
field: photography-fine-art
product: adobe-lightroom
tags: [adobe-lightroom, dodge-and-burn-layer, edit-in-photoshop, soft-light-layer, curves-dodge-burn, photoshop]
level: practitioner
status: draft
description: "Dodge and burn non-destructively in Photoshop with 50% grey Soft Light/Overlay layers or curve layers, after editing from Lightroom, and evaluate with a check layer."
sources: ["https://helpx.adobe.com/photoshop/user-guide.html (Blending modes; Dodge and Burn tools)", "Ansel Adams, The Print (dodging and burning)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Non-destructive dodge and burn layers

## Method A: 50% grey layer
1. Alt/Option-click the New Layer icon: Mode **Soft Light** (gentle) or Overlay (stronger), tick **Fill with Soft-Light-neutral color (50% gray)**. Name `D&B`.
2. Brush, soft edge, **Opacity 5-10%**, Flow 100 (or Flow low with opacity 100). Paint white to dodge, black to burn (`X` swaps). Build in many strokes.
3. Alternatively use the Dodge/Burn tools on the grey layer at Exposure 5-10%, Range Midtones.

## Method B: Curves pair (cleaner colour)
1. Curves layer pulled up (one stop brighter) named `Dodge`, mask filled black (Ctrl/Cmd+I).
2. Curves layer pulled down named `Burn`, mask black.
3. Paint white on the masks at low opacity. Set both layers to Luminosity blend mode to avoid saturation shifts.

## Micro dodge and burn (retouching skin, texture)
- Use a temporary **check layer**: Black & White adjustment + Curves with steep contrast above everything, to see uneven tones. Delete or hide before saving.

## Darkroom craft
- Guide the eye: burn edges and bright distractions, dodge the subject's key light. Keep changes subtle enough that a viewer sees light, not technique.
- Keep a print map (notes of what was dodged/burned) for editions.

## Gotchas
- Soft Light on 50% grey can shift saturation in dark areas; switch to Curves method for colour work.
- Merged/flattened TIFFs lose this flexibility; save PSD/TIFF with layers as the master.

## Verify
- [ ] Toggle the D&B group: the image gains depth and direction with no visible blotches at 100% or haloes along edges.
