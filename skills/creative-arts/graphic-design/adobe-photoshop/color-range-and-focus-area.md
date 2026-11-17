---
id: creative-arts.graphic-design.adobe-photoshop.color-range-and-focus-area
name: color-range-and-focus-area
category: creative-arts
field: graphic-design
product: adobe-photoshop
tags: [graphic-design, adobe-photoshop, photoshop, photoshop-selections, selection-tools, color-range-selection, focus-area, localized-color-clusters, fuzziness, skin-tones, highlights-shadows-selection]
level: practitioner
status: draft
description: "Select by colour and tone with Select > Color Range (fuzziness, localized clusters, skin tones, highlights/shadows) and by sharpness with Focus Area, then turn results into masks."
sources:
  - https://helpx.adobe.com/photoshop/using/selecting-color-range-image.html
  - https://helpx.adobe.com/photoshop/using/select-focus-area.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Color Range and Focus Area selections

**Goal:** soft, accurate selections of a colour, tone or in-focus subject that object-based tools cannot do well.

## Color Range (Select > Color Range)
- **Select: Sampled Colors** - click in the image or preview with the eyedropper; Shift/+ eyedropper
  adds, Alt/- subtracts.
- **Fuzziness:** how far from the sampled colour to include (20-60 typical). Lower = tighter.
- **Localized Color Clusters** + **Range:** restricts the selection to areas near your clicks -
  essential when the same colour appears elsewhere (a red shirt but not the red sign).
- Presets: Reds, Yellows... (no fuzziness control), **Highlights / Midtones / Shadows** with
  range and fuzziness sliders, **Skin Tones** (with Detect Faces).
- Preview: Selection Preview: Grayscale or Black Matte to see soft edges.
- OK, then add a **mask** to an adjustment layer: e.g. Hue/Saturation on just the selected colour.

## Typical uses
- Recolour a product colour (select colour -> Hue/Saturation or Solid Color in Color mode).
- Select a sky or flat background with gradients.
- Select highlights for luminosity-style masks (or use Blend If, see that skill).
- Remove white paper from scanned line art (select white, delete or mask).

## Focus Area (Select > Focus Area)
Selects the in-focus parts of a shallow-depth-of-field photo.
- **In-Focus Range** slider (auto first, then adjust); Image Noise Level for noisy images.
- Add/subtract with the brush; **Soften Edge**; then Select and Mask for refinement.
Useful for product or portrait shots against a blurred background where Select Subject struggles.

## Gotchas
- Color Range on a whole image can grab speckles; clean with a mask brush or Median/Minimum on the mask.
- Results are partial selections (soft) - good for adjustments, poor for hard cut-outs.
- Works on the composite for "Sampled Colors" only if the right layer is active; check Sample All Layers behaviour.

## Verify
- [ ] Mask viewed alone (Alt/Option+click mask): selected area white, no stray speckles where unwanted.
- [ ] Adjustment applied through the mask affects only the intended colour/area.
