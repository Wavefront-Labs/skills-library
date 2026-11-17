---
id: creative-arts.film-live-action.cinematography.colour-temperature-white-balance-and-gels
name: colour-temperature-white-balance-and-gels
category: creative-arts
field: film-live-action
product: cinematography
tags: [cinematography, film-live-action, dp, director-of-photography, gaffer, colour-temperature, color-temperature, kelvin, white-balance, gels, cto, ctb, plus-green, minus-green, mired, mired-shift, colour-meter, color-meter, tungsten, daylight, 3200k, 5600k, mixed-lighting, led-colour, cri, tlci, ssi, rgbw-led, skypanel, practicals, fluorescent, sodium-vapour, magenta-shift, green-spike, tint, warm-cool-contrast, gel-selection, gel-swatch, mixed-source-balance, window-balance, daylight-tungsten-mix, cri-tlci, led-spectrum, practical-bulbs, bulb-matching, practical-colour, custom-white-balance, in-camera-wb, white-balance-setting]
level: practitioner
status: draft
description: "Control colour on set: Kelvin and mired, white balance and tint, CTO/CTB/plus-green gel maths, matching or deliberately mixing daylight, tungsten, LED and practicals, judging LEDs by TLCI/SSI."
sources:
  - "American Cinematographer Manual, 10th ed. - Color temperature, filters and gels; Lighting chapters"
  - "https://www.rosco.com/ (Rosco gel transmission and mired shift data)"
  - "https://www.leefilters.com/ (Lee Filters colour correction guide)"
  - "https://theasc.com/ (ASC - Spectral Similarity Index)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Colour temperature, white balance and gels

**Goal:** every source in the frame is the colour you intended relative to the camera's
white point - matched for invisibility, or offset for a deliberate warm/cool story - and
no source has a green spike that ruins skin.

## 1. The numbers
- **Kelvin** describes the warm-cool axis only: candle ~1900 K, tungsten 3200 K,
  "warm white" LED 2700-3000 K, sunrise/sunset 2500-3500 K, HMI/noon daylight 5600 K,
  overcast 6500-7500 K, open shade 8000-10000 K.
- The **green-magenta axis** (tint) is separate: fluorescents, cheap LEDs and sodium
  lamps sit off-axis. A colour meter (Sekonic C-800) reads both, plus CRI/TLCI/SSI.
- **Mired** = 1,000,000 / K. Gels shift by a fixed mired amount, so the same gel changes
  warm sources less in Kelvin than cool ones. Full CTO ≈ +131 mired (5600 -> 3200 K);
  full CTB ≈ -131 mired (3200 -> 5600 K); 1/2, 1/4, 1/8 cuts are available.

## 2. Camera white balance
Set the camera to the **key light's** colour (3200 or 5600 preset, or a custom value)
and let everything else fall where you want it. Shooting log/RAW, white balance is
metadata for RAW but baked for most log codecs - so set it deliberately. Use **tint**
to pull a green cast out of a fluorescent-lit location when the sources can't be gelled.
Don't auto-white-balance; it will change shot to shot.

## 3. Match or mix - decide, then execute
**Matching** (invisible): gel the minority sources to the majority.
- Daylight windows with tungsten units: CTB the tungsten (loses ~1.5 stops) or, better,
  use HMI/daylight LED and leave windows alone. Or gel the windows with CTO (large, slow,
  but keeps tungsten fast) when the interior is the majority.
- Fluorescent locations: **minus-green** on the fluorescents (sleeves) or **plus-green**
  on your lights to match, then dial out with camera tint. Replace tubes with
  high-CRI/cinema tubes if the budget allows.
- Practicals: lamps with tungsten or warm LED bulbs read warm against a 5600 K balance -
  usually wanted; use dimmers (tungsten warms as it dims) or lower-K bulbs for more.
**Mixing** (deliberate): a cool moonlit exterior against a warm interior; a sodium street
against daylight. Decide the split in stops and Kelvin, write it on the lighting plan,
and keep it consistent across the scene's setups so the grade isn't fixing it per shot.

## 4. LED quality and RGBW fixtures
- Judge LEDs by **TLCI** (camera-based, >90 good) or **SSI** (ASC Spectral Similarity
  Index, compares to a reference like tungsten/daylight) rather than CRI. Low-quality LEDs
  can read "white" to a meter yet render skin grey-green on camera.
- RGBW/tunable fixtures (SkyPanel, Vortex, Astera) dial Kelvin, +/-green and gels from
  a library - but a dialed "CTO" is not spectrally identical to a gel on tungsten; match
  by eye on the monitor, not by the number, when mixing with real gels.
- Keep LEDs on the same output mode and firmware; dim via DMX rather than mains.

## 5. Working method
1. Meter (or eyeball on a calibrated monitor with the show LUT) each source's K and tint.
2. Decide the camera white point and the intended offset per source.
3. Gel/dial, then check skin on the vectorscope - skin should sit on the skin-tone line
   regardless of your creative balance.
4. Record the plan (K per source, gels) in the camera/lighting report for the colourist.

## Gotchas
- Mixing warm and cool with no plan - skin becomes two colours between master and close-up.
- CTB on tungsten without accounting for the light loss.
- Dimmed tungsten going orange mid-take.
- Trusting a 95 CRI number on a cheap panel.
- Open shade exteriors that go blue when the camera is balanced for sun.

## Verify
- [ ] Camera white balance set manually and noted; not auto.
- [ ] Every source's K/tint known and gelled or dialed to plan.
- [ ] Skin on the vectorscope skin line in each setup.
- [ ] Plan recorded for the colourist.
