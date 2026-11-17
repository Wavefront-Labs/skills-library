---
id: creative-arts.photography-fine-art.adobe-lightroom.white-balance-selector-and-temp-tint
name: white-balance-selector-and-temp-tint
category: creative-arts
field: photography-fine-art
product: adobe-lightroom
tags: [adobe-lightroom, white-balance-selector, lightroom-develop, white-balance, temp-tint, grey-card, lightroom-classic]
level: practitioner
status: draft
description: "Set white balance in Lightroom Classic with the White Balance Selector, temp/tint sliders and presets, then make deliberate creative shifts across a series."
sources: ["https://helpx.adobe.com/lightroom-classic/user-guide.html (Adjust image tone and color; White balance)", "https://helpx.adobe.com/lightroom-classic/help/apply-develop-settings.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# White Balance Selector and temp/tint

## Neutral starting point
1. Press `W` (or click the eyedropper in the Basic panel). The Loupe shows a grid of sampled RGB values.
2. Click a target that should be neutral: a grey card or WhiBal shot in the same light, or a light-grey (not blown white) object. Specular highlights and pure white give poor results.
3. Toolbar option "Auto Dismiss" returns to the hand tool after one click.

## Sliders
- **Temp**: blue <-> yellow. On raw files it is in Kelvin (2000-50000); on JPEG/TIFF it is a relative -100..+100 scale.
- **Tint**: green <-> magenta; fluorescent and LED light usually needs +Tint (magenta).
- **WB presets** (raw only): As Shot, Auto, Daylight, Cloudy, Shade, Tungsten, Fluorescent, Flash, Custom.

## Creative choice
- After neutral, decide intentionally: warm the golden hour (+300 to +600 K), keep blue hour cold, leave tungsten windows warm in night scenes.
- In a series, set one reference frame then sync White Balance only (Sync > tick White Balance) to frames in the same light; adjust per light change.
- Mixed light: set global WB for the dominant source and correct the other locally with a mask (masks have their own Temp/Tint).

## Gotchas
- Monitor must be calibrated to D65 before judging white balance.
- Snow and fog should read slightly cool or neutral, never yellow; the meter of truth is the RGB readout (R=G=B).

## Verify
- [ ] Hovering over the neutral reference shows R, G and B within 1-2% of each other.
