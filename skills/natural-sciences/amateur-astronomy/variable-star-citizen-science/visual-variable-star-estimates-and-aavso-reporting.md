---
id: natural-sciences.amateur-astronomy.variable-star-citizen-science.visual-variable-star-estimates-and-aavso-reporting
name: visual-variable-star-estimates-and-aavso-reporting
category: natural-sciences
field: amateur-astronomy
product: variable-star-citizen-science
tags: [variable-star-citizen-science, variable-stars, aavso, vsp, variable-star-plotter, comparison-stars, chart-id, magnitude-estimation, fractional-method, argelander, webobs, aavso-format, julian-date, mira-variables, cataclysmic-variables, dslr-photometry, citizen-science, occultation-timing, iota, exoplanet-transits, purkinje-effect, observer-code]
level: intro
status: draft
description: "Make visual variable-star magnitude estimates that AAVSO can use: get the right VSP chart, interpolate between comparison stars, avoid the classic biases, and submit via WebObs."
sources: ["AAVSO Visual Observing Manual (aavso.org)", "AAVSO WebObs and Variable Star Plotter help pages", "IOTA occultation observer's handbook"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Visual variable-star estimates and AAVSO reporting

**Goal:** honest, reproducible brightness estimates of variable stars that go into the
AAVSO International Database and get used by researchers — one of the few places a
backyard observer's data is genuinely scientific.

## 1. Set up
- Register with the **AAVSO** to get an observer code.
- Start with easy, large-amplitude stars recommended for beginners (bright **Mira** variables
  such as R Leonis or chi Cygni, *check the current AAVSO beginner target list*).
- Equipment: naked eye or binoculars for bright stars; a telescope for fainter ones.

## 2. Get the right chart
Use the **Variable Star Plotter (VSP)** on the AAVSO site:
- Enter the star name; choose a field of view and limiting magnitude that suit your
  instrument (e.g. a "D"-scale chart for small scopes).
- Charts show **comparison stars** labelled with their magnitude **without the decimal
  point** (`84` = mag 8.4) — chosen to avoid confusion with stars' own labels.
- Note the **Chart ID** printed on the chart — it must go with every report. Use only
  AAVSO comparison stars; other catalogues' magnitudes will make your estimates
  inconsistent with everyone else's.

## 3. Making an estimate
1. Find the field and identify the variable by star-hopping (see
   natural-sciences.amateur-astronomy.telescope-observing.collimating-a-reflector-and-star-hopping).
2. Pick one comparison star **brighter** and one **fainter** than the variable, as close
   in brightness and position as possible.
3. **Interpolate**: if the variable sits about 40% of the way from the brighter (8.4) to the
   fainter (9.1) star, the estimate is 8.4 + 0.4 × 0.7 ≈ 8.7. Record to 0.1 mag.
4. Record **date and time** (UTC; converted to Julian Date at submission), the comps used,
   chart ID, and notes on conditions (moon, haze, low altitude).
5. **Don't look up the previous estimates** before observing — knowing the "expected"
   value biases you. Estimate what you see.

## 4. Classic biases and how to avoid them
- **Colour / Purkinje effect:** red stars (most Miras) appear brighter the longer you stare.
  Use quick glances, or slightly defocus so star images are discs rather than points.
- **Position angle:** compare stars side by side horizontally rather than one above the
  other, if possible; tilt your head or the binoculars.
- **Altitude:** stars near the horizon are dimmed by extinction — don't use comparison stars
  at very different altitudes, and note low-altitude observations.
- **Fatigue and anticipation:** make each estimate independently, not from memory of
  last night.

## 5. Submit
Through **WebObs** (individual entry or a file in AAVSO Visual Format). Required fields
include star name, date/time (JD), magnitude, comparison stars, chart ID and notes. If you
couldn't see it, submit a **"fainter than"** observation (e.g. `<11.5` = fainter than the
faintest comp you could see) — those are useful too.

## 6. Beyond visual
- **DSLR/CMOS photometry** for more precision: AAVSO's DSLR manual and VPHOT; requires
  calibration frames and transformation coefficients.
- **Exoplanet transit** timing (AAVSO Exoplanet Section, ExoClock, NASA's Exoplanet Watch).
- **Occultation timing** (IOTA and regional groups): accurate GPS-linked video timing of
  stars disappearing behind asteroids or the Moon; reports go to IOTA/regional coordinators.

## Gotchas
- Using a chart with the wrong orientation (binocular/mirror reversal) and misidentifying
  the variable.
- Local time instead of UTC.
- Rounding comparison values or using non-AAVSO magnitudes.
- Reporting only positive detections (biases light curves at minimum).

## Verify
- [ ] Chart ID recorded and comps are AAVSO-sequence stars from that chart.
- [ ] Estimate brackets the variable between one brighter and one fainter comp.
- [ ] Time recorded in UTC; JD correct on submission.
- [ ] Red stars estimated with quick glances or defocus.
- [ ] Non-detections submitted as "fainter than" values.
