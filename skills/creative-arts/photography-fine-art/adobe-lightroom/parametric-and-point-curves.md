---
id: creative-arts.photography-fine-art.adobe-lightroom.parametric-and-point-curves
name: parametric-and-point-curves
category: creative-arts
field: photography-fine-art
product: adobe-lightroom
tags: [adobe-lightroom, point-curve, lightroom-color, tone-curve, parametric-curve, rgb-curves, lightroom-classic]
level: practitioner
status: draft
description: "Shape contrast with Lightroom Classic tone curves: parametric regions and splits, point curve, per-channel RGB curves, targeted adjustment and fades."
sources: ["https://helpx.adobe.com/lightroom-classic/user-guide.html (Tone Curve panel)", "https://helpx.adobe.com/photoshop/using/curves-adjustment.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Parametric and point curves

The Tone Curve panel has four modes (icons at top): **Parametric**, **Point**, and **Red/Green/Blue** point curves.

## Parametric
- Sliders for Highlights, Lights, Darks, Shadows. Three split handles under the graph move the boundaries between regions.
- Safe, smooth; good for gentle global contrast.
- Targeted Adjustment Tool (circle icon, or `Ctrl/Cmd+Alt/Option+Shift+T`): drag up/down on an area of the photo to move the region containing it.

## Point curve
- Click to add points; drag to move; right-click > Delete Control Point. Up to 16 points.
- **Classic S-curve**: point at quarter-tone pulled down slightly, three-quarter-tone pushed up. Keep the slope steepest where the subject's tones lie.
- **Matte/fade**: raise the bottom-left endpoint (black output to ~5-10%) for lifted blacks; lower the top-right for muted whites. Check against print: a faded black on matte paper can look grey.
- Presets: Linear, Medium Contrast, Strong Contrast. Save custom curves via the Point Curve menu.

## RGB curves
- Per-channel for colour toning or cross-processing: e.g. Blue curve: lift shadows (blue in shadows), lower highlights (yellow in highlights).
- Also corrects colour casts that vary with tone (a cool shadow cast that WB cannot fix).

## Gotchas
- Curves apply after Basic sliders; set Basic first so the curve shapes a correct base.
- Strong curves raise saturation in contrast areas; consider the Luminosity-blend effect by lowering Saturation in Color Mixer.
- Point and parametric curves stack.

## Verify
- [ ] Toggle the panel switch: the change is the intended contrast, with no posterisation in smooth skies.
