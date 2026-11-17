---
id: creative-arts.photography-fine-art.adobe-lightroom.capture-one-layers-and-masks
name: capture-one-layers-and-masks
category: creative-arts
field: photography-fine-art
product: adobe-lightroom
tags: [adobe-lightroom, capture-one-layers, capture-one-workflow, ai-masking, luma-range, capture-one]
level: practitioner
status: draft
description: "Use Capture One layers and masks: adjustment, healing and clone layers, AI masks, brush, gradient, luma range refinement and layer opacity for local work."
sources: ["https://support.captureone.com/hc/en-us/categories/360000279017-User-guide (Layer adjustments)", "https://support.captureone.com/hc/en-us/articles/360002619458-Applying-Styles-and-Presets-to-Layers"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Capture One layers and masks

Capture One is layer-based like Photoshop: the **Background** layer holds global edits; each adjustment layer holds local edits plus its own mask and **opacity** slider.

## Layer types (Layers tool, `+` menu)
- **Adjustment layer** (filled or empty mask): most tools (Exposure, HDR, Color Balance, Color Editor, Curve, Clarity, Sharpening, Noise) work per layer.
- **Healing layer** and **Clone layer**: for retouch; or use the Heal/Clone brushes that create them automatically. Clone copies exactly; Heal blends.
- Layer opacity scales the whole effect.

## Masks
- **Brush** (`B`): size, hardness, opacity, flow; Auto Mask for edges. Erase with `E`.
- **Gradient mask** (`G`) linear and **Radial** (`T`).
- **AI masks**: Magic Brush (paint over an area of similar colour/tone), AI Select Subject/Background/Sky in recent versions.
- **Refine**: Refine Mask (edge-aware radius), Feather Mask, **Luma Range** (restrict mask to a tonal range with falloff, like a luminosity mask), Invert Mask.
- `M` toggles mask display; Alt/Option-drag colour of overlay in preferences.

## Workflow
1. Global edits on Background.
2. New filled layer > Luma Range to target highlights > Exposure -0.4 = sky/highlight burn.
3. Name layers ("Sky burn", "Face dodge").
4. Copy layers to other images via Copy/Apply with "Layers" included (they paste as masks in the same positions; AI masks recompute where supported).

## Gotchas
- Luma Range applied to a brushed mask is live and can be re-edited; flattening it with "Apply Luma Range" is permanent.
- Too many layers slow rendering; merge ideas into fewer layers.

## Verify
- [ ] Toggling each layer's checkbox shows only the intended region changing, with smooth mask edges at 100%.
