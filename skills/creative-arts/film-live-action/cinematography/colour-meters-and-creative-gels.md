---
id: creative-arts.film-live-action.cinematography.colour-meters-and-creative-gels
name: colour-meters-and-creative-gels
category: creative-arts
field: film-live-action
product: cinematography
tags: [cinematography, film-live-action, colour-meter-use, spectrometer, cc-index, party-gels, creative-gels, colour-contrast-lighting, tlci, cri, ssi, plus-green, minus-green]
level: practitioner
status: draft
description: "Measure and design colour on set: colour meters and spectrometers (CCT, CC index, TLCI/SSI), correcting green/magenta, and creative gels and colour contrast."
sources:
  - "https://www.sekonic.com/c-800 (Sekonic C-800 SpectroMaster - CCT, CC index, CRI/TLCI/SSI)"
  - "https://www.oscars.org/science-technology/projects/spectral-similarity-index-ssi (AMPAS - Spectral Similarity Index)"
  - "https://us.rosco.com/en/products/catalog/roscolux (Rosco - gel catalogue and CTB/CTO/plus-minus green)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Colour meters and creative gels

**Goal:** know the true colour of every source, fix the mismatches you don't want, and
add the colour you do want on purpose.

## 1. What a colour meter tells you
A colour meter / spectrometer (e.g. Sekonic C-800/C-7000, UPRtek) reads a source and gives:
- **CCT** (Kelvin) - the blue/orange axis.
- **CC index / Delta uv** - the green/magenta axis (positive = green, needs magenta);
  meters can display the **correcting gel** directly (e.g. "1/4 Minus Green").
- **CRI (Ra, R9)**, **TLCI**, **SSI**: colour rendering. TLCI 90+ and SSI (vs tungsten
  or daylight reference) 75+ are generally good for camera; low R9 = poor reds (skin).
- Spectral graph: spikes and gaps (cheap LEDs, fluorescent, sodium).

## 2. Workflow on location
1. Meter existing sources: windows (daylight varies 5000-7500 K and more in shade),
   practicals, overheads (fluorescent/LED panels often +green), street lights (sodium/
   LED).
2. Decide the **base white balance** for the scene (camera Kelvin + tint).
3. Correct sources that should read neutral: CTB/CTO fractions on lamps or windows,
   **minus green** (magenta) on fluorescents, or set RGB/tunable fixtures to match the
   measured CCT and tint.
4. Re-meter after gelling; note values in the lighting log.
Gels fade, especially blues: replace when they look washed.

## 3. Creative colour (party gels)
- **Colour contrast**: warm key vs cool ambient (classic day interior), teal night vs
  sodium orange, complementary pairs (cyan/red, blue/amber).
- **Motivated colour**: neon signs, police lights, TV glow, fire - match the practical's
  colour in your unit.
- Saturated gels (e.g. Rosco/Lee primaries, "party gels") or RGB LED effects; keep skin
  out of extreme saturation unless intentional - saturated light on skin clips a single
  channel quickly.
- Expose saturated colours carefully: check the camera's RGB parade - blue and red channels
  clip before luma shows it.
- Decide with the colourist: build colour in camera or neutral capture and push in grade?
  Strong in-camera colour limits later choices but looks more organic.

## 4. Tunable LEDs
Set CCT and +/- green numerically on the fixture or console (see DMX skill); meter
anyway - different fixture brands at "5600K" don't match.

## Gotchas
- Trusting "5600K" labels; fixtures and windows differ.
- Ignoring the green/magenta axis; skin turns sickly.
- Saturated blue light clipping the blue channel on faces.
- Faded gels mid-shoot changing the colour between days.

## Verify
- [ ] Sources metered for CCT and CC; corrections applied and re-metered.
- [ ] Colour rendering (TLCI/SSI) checked on key fixtures.
- [ ] Creative colour scheme agreed with director and colourist.
- [ ] RGB parade checked on saturated scenes.
