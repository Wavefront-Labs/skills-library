---
id: creative-arts.photography-fine-art.adobe-lightroom.luminance-color-and-depth-range-masks
name: luminance-color-and-depth-range-masks
category: creative-arts
field: photography-fine-art
product: adobe-lightroom
tags: [adobe-lightroom, range-mask, lightroom-masking, luminance-range, color-range, depth-range, lightroom-classic]
level: practitioner
status: draft
description: "Restrict Lightroom Classic masks by luminance, colour or depth range, with smoothness and the range eyedropper, to target highlights, hues or distance."
sources: ["https://helpx.adobe.com/lightroom-classic/user-guide.html (Masking; Range masks)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Luminance, colour and depth range masks

Range masks can be created on their own (Create New Mask > Luminance/Color/Depth Range) or used to **intersect** an existing mask (Mask > Intersect with > ...).

## Luminance Range
- Click the eyedropper on a tone or drag a rectangle. Or set the range bar handles (0-100) and the inner **Smoothness** (feather) handles.
- "Show Luminance Map" displays the selection as a greyscale map.
- Typical: intersect a Sky mask with luminance 60-100 to darken only bright clouds, or a gradient with 0-30 to open only shadows.

## Color Range
- Click a colour (Shift-click up to five samples) or drag a box. **Refine** slider narrows or widens the hue match.
- Typical: shift green foliage only, desaturate one distracting colour, or warm skin within a Person mask.

## Depth Range
- Available only for photos with embedded depth maps (iPhone Portrait-mode HEIC). Selects by distance for foreground/background separation.

## Tips
- Range masks are pixel-based and follow image detail closely: no painting around branches.
- Combine with a gradient for "darker bottom, but only in the shadows".
- Global equivalent of a luminance mask: Tone Curve or Color Grading; use range masks when you need locality.

## Gotchas
- Narrow ranges with low smoothness produce posterised edges; keep smoothness above about 20.
- Color Range fails on low-saturation areas (grey sky); use luminance instead.

## Verify
- [ ] Overlay (O) shows the intended tones or hues selected with smooth transitions; toggling the mask produces no visible edge lines.
