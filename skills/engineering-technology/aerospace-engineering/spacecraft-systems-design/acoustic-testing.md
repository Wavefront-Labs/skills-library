---
id: engineering-technology.aerospace-engineering.spacecraft-systems-design.acoustic-testing
name: acoustic-testing
category: engineering-technology
field: aerospace-engineering
product: spacecraft-systems-design
tags: [acoustic-test, reverberant-chamber, vibroacoustics, oaspl, launch-environment, environmental-testing]
level: practitioner
status: draft
description: "Plan a spacecraft acoustic test: reverberant chamber levels from the launcher, duration, tolerance, which hardware it governs and how to cover it analytically."
sources:
  - "NASA GSFC-STD-7000 (GEVS)"
  - "launch vehicle user's guides"
  - "Wertz and Larson, Space Mission Analysis and Design"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Acoustic testing

**Goal:** verify hardware, especially large and light structures, against the launch acoustic environment.

## Environment
The launch vehicle user's guide provides the maximum predicted acoustic spectrum under the fairing in one-third octave bands, with an overall level (OASPL) typically in the region of 135 to 145 dB. Qualification and protoflight levels add margin on top of the prediction (GEVS gives the margin approach); duration is on the order of a minute or two; confirm the standard.

## Why it matters
Lightweight, large-area hardware (solar arrays, antennas, radiators, thermal blankets, panels) responds strongly to acoustics and often is governed by it rather than by shaker vibration. Acoustic loads also excite equipment on those panels.

## Procedure
1. Collect the predicted acoustic spectrum and fill effects (the fairing fill factor correction for the spacecraft size).
2. Choose test method: reverberant chamber with horns; or direct-field acoustic testing (DFAT) with loudspeaker arrays; lower cost and more flexible but the control tolerance and the field uniformity need care.
3. Control the field with several microphones and check the tolerance of the spectrum (for example plus and minus 3 dB in one-third octave bands, per the programme's tolerance).
4. Instrument with accelerometers on panels and large appendages; inspect before and after, run functional tests.
5. Use vibroacoustic analysis (statistical energy analysis or finite element/boundary element) to derive random-vibration environments for units mounted on panels (see random-vibration-loads-and-miles-equation).

## Gotchas
- Avoid over-test of delicate hardware in the chamber: correlate with acoustic analysis.
- Cleanliness and venting in the chamber.
- Acoustic noise may also affect deployables stowed; check release devices.

## Verify
- [ ] The measured field spectrum is within the tolerance and the panel responses fit the predicted levels.
