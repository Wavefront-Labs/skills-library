---
id: creative-arts.film-live-action.color-grading.look-development-references-tests-and-show-lut
name: look-development-references-tests-and-show-lut
category: creative-arts
field: film-live-action
product: color-grading
tags: [color-grading, film-live-action, look-references, grade-references, mood-board, look-test, camera-test-grade, look-on-tests, building-show-lut, lut-building, lmt-creation, bleach-bypass, stylised-looks, cross-process]
level: practitioner
status: draft
description: "Develop a show look with the DP and director: reference boards, grading camera tests, stylised looks like bleach bypass, and building the show LUT or ACES LMT."
sources:
  - "The Colorist Guide to DaVinci Resolve (Blackmagic official training) - look development"
  - "https://www.acescentral.com (ACES - Look Modification Transforms and pipeline docs)"
  - "Alexis Van Hurkman, Color Correction Look Book"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Look development: references, tests and the show LUT

**Goal:** a look agreed before principal photography, expressed as a technically clean
transform that set, dailies and the final grade all share.

## 1. References and the look book
- Collect **frames** from films, photography, painting - with the DP and director - and
  organise by scene type (day int, night ext, flashback). Annotate what you like in
  each: contrast, colour separation, skin, black density, highlight roll-off.
- Distil into 3-6 adjectives and a palette ("dense blacks, warm skin, cyan-green
  shadows, low saturation in greens").
- Agree the **display target** early (SDR Rec.709, P3 theatrical, HDR PQ) - looks are built
  for a display.

## 2. Grade the camera tests
The DP shoots tests (lenses, filters, exposure, wardrobe, make-up, set colours) in prep.
Grade them in a colour-managed pipeline:
1. Balance neutrally (charts, grey card).
2. Build the look on top (contrast curve, colour separation, saturation roll-off, film
   emulation if wanted).
3. Test the look across exposures (-2 to +3 stops) and skin tones; the look must not
   break when exposure varies.
Review on a calibrated display with the DP/director; iterate.

## 3. Stylised looks
- **Bleach bypass** (skipping the bleach in film processing): lower saturation, higher
  contrast, silvery highlights. Digital recipe: luminance layer blended (overlay/soft light)
  over the image, desaturate, add contrast; keep skin from going grey.
- **Cross-process** (E6 film in C41 chemistry): shifted colours, high contrast, odd
  highlights - curves per channel.
- **Day-for-night**, **sepia/monochrome toning**, **teal-orange** split. Build stylisation
  as separate, labelled nodes so intensity is adjustable.

## 4. Build the show LUT / LMT
- In ACES: express the look as an **LMT** (applied before the Output Transform) - CLF
  or a LUT in ACEScct.
- In a camera-log pipeline: a **show LUT** from camera log to display (e.g. LogC4 to
  Rec.709) that includes the look - export from Resolve (*Generate LUT* from the node tree,
  33/65-point `.cube`). Keep a **neutral version** and the **look-only** version.
- Make variants per display (SDR, HDR) and per camera if mixing cameras.
- Version and name: `SHOW_LogC4_to_709_LOOK_v03.cube`.

## Gotchas
- Looks designed on tests shot at one exposure - fall apart on set.
- LUTs with clipping/ banding (hard curves in 17-point cubes).
- No neutral version for VFX and dailies troubleshooting.
- Look references never shared with the dailies colourist.

## Verify
- [ ] Reference board with annotations and a display target.
- [ ] Look tested across exposures and skin tones.
- [ ] Stylised elements on separate adjustable nodes.
- [ ] Show LUT/LMT exported, versioned, with neutral and per-display variants.
