---
id: creative-arts.theatre.lighting-design.led-colour-mixing-for-stage
name: led-colour-mixing-for-stage
category: creative-arts
field: theatre
product: lighting-design
tags: [theatre, lighting-design, lighting-colour, led-colour-mixing, led-fixtures, rgbw, rgbal, lime, cri, tm-30, colour-picker, gel-match, colour-temperature, eos, colour-palettes]
level: practitioner
status: draft
description: "Mix colour with LED fixtures: emitter sets (RGBW, RGBAL, 7-colour), gel-match and CCT modes, rendering metrics (CRI, TM-30), consistent palettes across fixture types."
sources:
  - "https://www.etcconnect.com/Products/Lighting-Fixtures/"
  - "https://www.ies.org/standards/standards-theory/ies-tm-30-20/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# LED colour mixing for stage

## Emitter sets
- **RGB**: saturated colours good, whites and pastels poor (spiky spectrum, bad
  skin).
- **RGBW / RGBA**: adds white/amber for better whites and warm tints.
- **RGBAL** (amber + lime) and **7- or 8-colour** systems (e.g. ETC Lustr series,
  combining emitters such as red, red-orange, amber, lime/mint, green, cyan, blue,
  indigo — the exact set varies by model and generation) give fuller
  spectra, better skin and pastels.
- **Variable white** fixtures (warm + cool white) for tunable CCT.

## Control modes
- **Direct emitter control**: each colour channel separately — full control,
  most parameters.
- **Hue/Saturation/Intensity** or **x,y** colour picker on the console (e.g. ETC
  Eos colour picker with fixture profile calibration) — fast, consistent across
  fixture types if profiles are good.
- **Gel-match**: many fixtures/consoles offer Lee/Rosco filter emulation —
  useful starting points, not exact matches.
- **CCT mode**: set colour temperature (e.g. 2700-6500 K) with +/- green
  (tint) correction.

## Rendering quality
- **CRI** (Ra) is a basic index; **TM-30** (IES) Rf (fidelity) and Rg (gamut)
  describe rendering better; TLCI for camera work.
- For faces, prefer full-spectrum modes (with lime/amber/white) and check skin
  under the actual mix.

## Building palettes
1. Make **colour palettes** on the console (see Eos palettes skill) for each
   look: e.g. "Warm Front", "Night Blue", "Skin Pink".
2. Calibrate visually across fixture types (an LED wash and an LED profile
   won't match at the same numbers); adjust per type within the palette.
3. Check at **low intensity**: LEDs can step or shift colour when dimmed;
   enable smoothing/dimming curves (e.g. "square law") and higher refresh rates
   for cameras.

## Gotchas
- RGB-only washes on faces — greenish/grey skin.
- Mismatched whites between LED and tungsten — use CTO/CTB on tungsten or tune
  LED CCT.
- Colour shifts during fades (path through odd colours) — set fade paths/colour
  mixing paths on the console.

## Verify
- [ ] Palettes created and visually matched across fixture types.
- [ ] Skin checked under each key colour with performers.
- [ ] Dimming smooth at low levels.
