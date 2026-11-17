---
id: creative-arts.photography-fine-art.adobe-lightroom.capture-one-color-editor
name: capture-one-color-editor
category: creative-arts
field: photography-fine-art
product: adobe-lightroom
tags: [adobe-lightroom, capture-one-color-editor, capture-one-workflow, skin-tone-tool, colour-range, capture-one]
level: practitioner
status: draft
description: "Use the Capture One Color Editor in basic, advanced and skin tone modes to pick and shift colour ranges, smooth and use them on layers."
sources: ["https://support.captureone.com/hc/en-us/articles/8039270422173-Color-Editor", "https://support.captureone.com/hc/en-us/articles/8807981446045-Perfecting-skin-tones"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Capture One Color Editor

Color tool tab > **Color Editor**. Three modes.

## Basic
- Eight colour ranges (Red, Orange, Yellow, Green, Cyan, Blue, Magenta and an All slider) with Hue, Saturation, Lightness. Similar to Lightroom HSL.
- Use the picker to choose the range that matches a sampled colour.

## Advanced
1. Pick the colour with the eyedropper on the image. A wedge appears on the colour wheel.
2. Adjust the wedge: drag the edges to widen or narrow the hue range and the inner/outer arcs for saturation range.
3. **Smoothness** controls the falloff (prevents banding).
4. **View selected color range** (tick) shows which areas are affected, greying out the rest.
5. Apply Hue rotation, Saturation and Lightness for that slice only. Add several slices.

## Skin Tone
1. Pick skin; wedge set around it.
2. Uniformity sliders (Hue, Saturation, Lightness) pull all skin pixels toward the picked value, evening blotchy redness.
3. Adjust amount to keep natural variation (Uniformity 20-50).

## Layers and styles
- Color Editor works on layers: mask a jacket and change only its colour.
- Save as a style or preset to reuse a colour grade; right-click > Create Masked Layer from Selection makes a mask from the selected colour range.

## Gotchas
- Narrow ranges with low smoothness show hard edges; check at 100%.
- Strong skin uniformity looks painted; check eyes and lips keep their colour.

## Verify
- [ ] With "View selected color range" on, only the intended colour is active; final shows no banding in gradients.
