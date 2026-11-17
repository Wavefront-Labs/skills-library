---
id: creative-arts.photography-fine-art.adobe-lightroom.capture-sharpening-and-masking-slider
name: capture-sharpening-and-masking-slider
category: creative-arts
field: photography-fine-art
product: adobe-lightroom
tags: [adobe-lightroom, capture-sharpening, lightroom-detail, sharpening-mask, detail-panel, lightroom-classic]
level: practitioner
status: draft
description: "Apply capture sharpening in the Lightroom Classic Detail panel: amount, radius, detail and the Alt-drag masking slider to sharpen edges but not noise or skies."
sources: ["https://helpx.adobe.com/lightroom-classic/user-guide.html (Sharpen photos)", "Bruce Fraser and Jeff Schewe, Real World Image Sharpening (Peachpit) - capture/creative/output sharpening model"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Capture sharpening and the masking slider

Capture sharpening restores softness from the sensor's anti-aliasing filter and demosaicing. It is the first of three stages (capture, creative/local, output). Judge it at **100% (1:1)** only.

## Sliders (Detail panel)
- **Amount** (default 40 on raw): strength.
- **Radius** (0.5-3.0, default 1.0): width of the edge halo. Fine-detail subjects (landscape, architecture) 0.7-1.0; soft subjects (portraits) 1.2-1.5.
- **Detail** (default 25): how much fine texture is sharpened. High (50-100) for textured landscape; low (10-25) for portraits and noisy files.
- **Masking** (default 0): restricts sharpening to edges. **Hold Alt/Option while dragging**: white areas get sharpened, black areas are protected. Raise until smooth skin and sky are black (often 40-80).

Alt/Option-drag on Amount, Radius and Detail too: the preview turns greyscale to show only the sharpening effect.

## Starting points
| Subject | Amount | Radius | Detail | Masking |
|---|---|---|---|---|
| Landscape, low ISO | 50-70 | 0.8 | 40-60 | 20-40 |
| Portrait | 35-50 | 1.2-1.4 | 15-25 | 60-80 |
| High ISO after Denoise | 30-40 | 1.0 | 15 | 50+ |

## Gotchas
- AI Denoise produces its own sharpening-friendly output; reduce Detail and use Masking afterwards.
- Sharpening increases visible noise in skies: masking is the fix, not lower Amount everywhere.
- Capture sharpening does not compensate for output size or paper; that is the output sharpening step.

## Verify
- [ ] At 100%, edges are crisp with no white halo lines and smooth areas show no added grain.
