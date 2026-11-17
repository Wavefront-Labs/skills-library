---
id: creative-arts.animation.color.grading-viewing-environment
name: grading-viewing-environment
category: creative-arts
field: animation
product: color
tags: [viewing-environment, monitor-calibration, surround, bias-lighting, ambient-light, grading-suite, d65, bt2035, review-room]
level: practitioner
status: draft
description: "Set up a grading or review room so judgments transfer: D65 bias lighting, surround luminance, ambient levels, neutral walls and viewing distance per SMPTE/ITU guidance."
sources:
  - https://www.itu.int/rec/R-REC-BT.2035
  - https://www.itu.int/rec/R-REC-BT.1886
  - https://www.smpte.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Viewing environment for grading

**Goal:** the room does not distort perception, so a grade made here looks the same in other calibrated rooms.

## Specification (SDR reference viewing, after ITU-R BT.2035 / SMPTE ST 2080-3 practice)

| Item | Target |
|---|---|
| Display peak white | 100 cd/m2 (BT.1886 SDR) |
| Surround / bias light behind display | D65 colour, about 10% of display white (around 10 cd/m2) |
| Ambient light on screen | as low as practical, never direct light on the screen |
| Wall and desk colours | neutral mid-grey, matte |
| Viewing distance | about 3-3.2x picture height for HD |
| Light sources | high-CRI (95+) D65 fixtures only; no daylight from windows |

## Why each matters

- **Surround:** a pitch-black room makes the eye adapt so images look higher contrast and brighter; graders then
  under-expose. A dim D65 surround sets a stable adaptation.
- **Coloured walls** shift perceived white balance (a green wall makes grades go magenta).
- **Daylight** changes through the day; grades made at 3 pm and 8 pm disagree.

## Animation studio practice

- Review rooms (dailies, sweatbox) should match the grading room spec at least for surround and display calibration,
  or approved colours drift between rooms (`creative-arts.animation.pipeline.dailies-review`).
- Artist desks: at least D65 calibrated displays and bias lights; full spec is for grading and final review.
- For web-first (YouTube) shows, also check on a typical consumer phone and laptop at the end, but grade in the
  controlled room.

## Verify

Measure the surround with the probe in ambient mode: D65 within a few hundred kelvin and luminance near 10% of
display white; ambient on the screen face below about 5 lux.
