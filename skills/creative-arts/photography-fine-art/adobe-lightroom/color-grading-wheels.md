---
id: creative-arts.photography-fine-art.adobe-lightroom.color-grading-wheels
name: color-grading-wheels
category: creative-arts
field: photography-fine-art
product: adobe-lightroom
tags: [adobe-lightroom, color-grading-wheels, lightroom-color, color-grading, split-toning, lightroom-classic]
level: practitioner
status: draft
description: "Tint shadows, midtones and highlights with Lightroom Classic Color Grading wheels, using blending and balance controls for subtle split-tone looks."
sources: ["https://helpx.adobe.com/lightroom-classic/user-guide.html (Color Grading panel)", "https://helpx.adobe.com/lightroom-classic/help/apply-develop-settings.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Color Grading wheels

Color Grading (replaced Split Toning in 2020) has Shadows, Midtones, Highlights wheels plus a Global wheel. View selector at top: 3-way, or one wheel at a time (larger, more precise).

## Controls
- Drag the centre point for **Hue** and **Saturation**; the outer handle sets hue only at the current saturation.
- **Luminance** slider under each wheel lightens/darkens that region.
- **Blending** (default 50): how much the regions overlap. Lower = sharper separation; higher = smoother.
- **Balance** (-100..+100): shifts the split point between shadows and highlights.
- Hold **Shift** while dragging to change saturation only; hold **Ctrl/Cmd** for fine movement. Double-click a value to reset.

## Recipes (keep saturation low: 5-20)
- **Classic warm/cool**: Shadows hue ~220 (blue), sat 8; Highlights hue ~45 (amber), sat 12.
- **Toned B&W**: with a Monochrome profile, Highlights hue ~45 sat 10 and Shadows hue ~40 sat 5 gives a selenium/sepia print feel; split hues for a split-toned print.
- **Unify a series**: a light Global tint (sat 3-6) applied to all frames binds mixed light conditions.

## Gotchas
- High saturation shifts skin and neutrals immediately; check a neutral patch with the RGB readout.
- Presets from Split Toning still map into Shadows/Highlights with Midtones at zero.

## Verify
- [ ] Toggle the panel eye: the grade reads as atmosphere, not a colour cast, and greys in the image remain near neutral where intended.
