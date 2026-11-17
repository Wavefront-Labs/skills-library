---
id: creative-arts.film-live-action.davinci-resolve.log-wheels-hue-curves-and-color-warper
name: log-wheels-hue-curves-and-color-warper
category: creative-arts
field: film-live-action
product: davinci-resolve
tags: [davinci-resolve, resolve, film-live-action, log-wheel-ranges, log-softness, log-palette, curves-use, hue-curves, lum-vs-sat-use, color-warper, colour-warper, color-slice, colour-slice, hue-vs-hue, sat-vs-sat]
level: practitioner
status: draft
description: "Go beyond the primary wheels in Resolve: tuning log wheel ranges and softness, hue and lum curves for targeted fixes, and Color Warper and Color Slice for shaping colour."
sources:
  - "https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_Reference_Manual.pdf (Resolve Reference Manual - Log palette, Curves palette, Color Warper, Color Slice)"
  - "The Colorist Guide to DaVinci Resolve (Blackmagic official training)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Log wheels, hue curves and Color Warper

**Goal:** precise tonal and colour shaping - separating skies from skin, shadows from
mids - without keys and windows.

## 1. Log wheels: ranges and softness
Log palette: **Shadow, Midtone, Highlight** wheels plus **Offset**. Under the palette:
- **Low Range** (top of the shadow zone) and **High Range** (bottom of the highlight zone)
  define where the bands split - defaults ~0.333/0.550.
- **Low Soft / High Soft** (in the palette options) widen or narrow the transitions.
- Practical: for a film-like split-tone, warm the highlights and cool the shadows with
  narrow bands so mids (skin) stay untouched; raise Low Range if shadows include faces.
- Log wheels work best in a scene-referred, log working space (DaVinci Intermediate,
  ACEScct) - offsets behave like exposure.
Watch the parade while moving each wheel to see exactly which part moves.

## 2. Curves for targeted fixes
- **Hue vs Hue**: shift one hue (pull green foliage toward yellow; fix magenta skin).
- **Hue vs Sat**: desaturate one colour (a loud red car).
- **Hue vs Lum**: darken blue skies (introduces noise at extreme values - small moves).
- **Lum vs Sat**: desaturate deep shadows and bright highlights for a film feel; fixes
  colour noise in blacks.
- **Sat vs Sat**: compress over-saturated colours (neons, LEDs) while leaving low-sat areas.
- **Sat vs Lum**: darken saturated colours (density-like look).
Use the eyedropper (pick in viewer) to place points; adjust with **soft** wide ranges.

## 3. Color Warper (Resolve 18+)
A mesh grid over a hue/saturation (or chroma/luma) space: drag control points to move
colours - one colour into another, with neighbours following smoothly.
- **Hue-Saturation** mode: pull a hue around the wheel and in/out in saturation.
- **Chroma-Luma** mode: change brightness of colours (density).
- Pin points (lock) to protect skin and neutrals; adjust grid resolution for precision.
Great for "colour palette" looks (e.g. collapse greens and cyans into a teal family).

## 4. Color Slice (Resolve 19+)
Subtractive-style controls per **hue slice** (red, skin, yellow, green, cyan, blue, magenta):
**density**, saturation and hue per vector, with a global saturation/density and a
dedicated skin slice - a quick way to get film-like density in colours.

## Gotchas
- Hue vs Lum extremes causing noise and artefacts; prefer Color Warper Chroma-Luma or a key.
- Log wheel ranges left default when faces sit in the "shadow" band.
- Curves applied on a node before the colour space transform (unpredictable).
- Warper moves without pinning skin.

## Verify
- [ ] Log ranges set to the image's tonal split; skin unaffected unless intended.
- [ ] Curves used with soft ranges; noise checked.
- [ ] Warper/Slice moves pin skin and neutrals.
- [ ] Changes viewed on scopes and a calibrated monitor.
