---
id: creative-arts.photography-fine-art.art-photography.expose-to-the-right-with-the-histogram
name: expose-to-the-right-with-the-histogram
category: creative-arts
field: photography-fine-art
product: art-photography
tags: [art-photography, exposure-control, expose-to-the-right, ettr, histogram, highlight-clipping, blinkies, raw-exposure, noise, uni-wb]
level: practitioner
status: draft
description: "Read a camera histogram and highlight warnings, expose raw files to the right for clean shadows, and avoid clipping channels that cannot be recovered."
sources: ["https://www.cambridgeincolour.com/tutorials/histograms1.htm", "https://www.ppa.com/cpp"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Expose to the right (ETTR) with the histogram

Digital sensors capture linearly: the brightest stop holds half of all recorded levels,
the darkest stops very few. Exposing as bright as possible **without clipping important
highlights**, then pulling down in raw development, gives cleaner shadows than brightening
an underexposed file.

## Reading the histogram
- X axis: dark (left) to bright (right). Height: how many pixels.
- A spike against the right wall = clipped highlights. Against the left = crushed blacks.
- Use the **RGB (per-channel) histogram**: a red flower or blue sky can clip one channel
  while the luminance histogram looks fine.

## ETTR procedure (raw only)
1. Set picture style to neutral/low contrast so the preview histogram is closer to raw.
2. Turn on highlight alert (blinkies).
3. Increase exposure (shutter time or aperture - not ISO, if you can avoid it) until the
   brightest *important* highlight just blinks, then back off 1/3-2/3 stop.
4. Ignore specular highlights and light sources - they may clip.
5. In Lightroom/ACR pull Exposure or Highlights down to restore the intended tone.

## When not to ETTR
- JPEG capture (no headroom to pull back).
- Fast action where a slower shutter costs sharpness.
- High-contrast scenes already filling the histogram edge to edge - bracket instead.
- ISO-invariant sensors at base ISO already: raising ISO to brighten adds little.

## Gotchas
- The camera histogram is from the embedded JPEG; most raw files hold ~0.5-1 stop more
  highlight data. Learn your body's margin by testing, not by assumption.
- "UniWB" custom white balance makes the preview more raw-like; it turns the screen green.

## Verify
- [ ] RGB histogram touches but does not stack up on the right wall for important tones.
- [ ] In raw development, highlights pulled back show texture, not flat grey.
