---
id: creative-arts.photography-fine-art.adobe-lightroom.calibration-panel-primaries
name: calibration-panel-primaries
category: creative-arts
field: photography-fine-art
product: adobe-lightroom
tags: [adobe-lightroom, calibration-panel, lightroom-color, primaries, process-version, lightroom-classic]
level: practitioner
status: draft
description: "Use the Lightroom Classic Calibration panel to shift red, green and blue primaries, fix shadow tint and build a consistent colour signature across a series."
sources: ["https://helpx.adobe.com/lightroom-classic/user-guide.html (Calibration panel)", "https://helpx.adobe.com/lightroom-classic/help/apply-develop-settings.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Calibration panel primaries

The Calibration panel (bottom of Develop) shows the **Process Version** and adjusts how the profile maps the camera's red, green and blue primaries. It acts on all colours that contain each primary, so it moves the whole palette coherently in a way HSL cannot.

## Controls
- **Shadows Tint**: green/magenta cast only in the shadows (some sensors render green shadows).
- **Red / Green / Blue Primary**: Hue and Saturation for each.

## Recipes
- **Clean, rich colour** (popular landscape start): Blue Primary Saturation +20 to +40; Blue Primary Hue -10 to -20 for deeper, cleaner skies. Then lower global Saturation slightly.
- **Warmer skin, cleaner greens**: Red Primary Hue +5 to +10 and Green Primary Saturation -10 to calm vivid foliage.
- **Teal and orange feel**: Red Primary Hue +20, Blue Primary Hue -50, Blue Saturation +30. Use gently.

## Workflow
- Calibration sits at the end of the panel stack but should be set **early** for a series, because it changes how HSL and colour grading appear.
- Save as a develop preset containing Calibration only, and apply to every frame of a project to fix a signature palette.

## Gotchas
- Calibration settings are relative to the chosen profile; switching profile changes the result.
- Large Blue Primary Saturation pushes blue skies out of print gamut: soft-proof with gamut warning.

## Verify
- [ ] Gamut warning in soft proof shows no large out-of-gamut areas after calibration changes.
