---
id: creative-arts.animation.color.displaycal-monitor-profiling
name: displaycal-monitor-profiling
category: creative-arts
field: animation
product: color
tags: [displaycal, monitor-calibration, colorimeter, argyllcms, icc-profile, d65, bt1886, display-calibration, probe]
level: practitioner
status: draft
description: "Calibrate and profile artist and grading monitors with DisplayCAL and a colorimeter: targets for Rec.709/sRGB, measurement settings, verification reports."
sources:
  - https://displaycal.net/
  - https://www.argyllcms.com/doc/ArgyllDoc.html
  - https://www.itu.int/rec/R-REC-BT.1886
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Profiling with DisplayCAL and a probe

**Goal:** every artist and review display shows the show's colours within a known tolerance of the standard.

## Kit

- A colorimeter (X-Rite/Calibrite i1Display Pro or Plus, Datacolor Spyder X2) for routine work; a
  spectrophotometer (i1Pro) to build a correction matrix for wide-gamut panels.
- DisplayCAL (GUI over ArgyllCMS; the maintained fork runs on Python 3, install from displaycal.net or PyPI).

## Targets

| Use | White | Tone response | Luminance |
|---|---|---|---|
| Artist sRGB desktop | D65 | sRGB | 120 cd/m2 (match room) |
| Rec.709 video review | D65 | BT.1886 (gamma 2.4, absolute black) | 100 cd/m2 |
| Web/YouTube previews | D65 | sRGB or gamma 2.2 | 120-160 cd/m2 |

## Procedure

1. Warm the display 30 minutes; reset to its native/standard mode; disable dynamic contrast, eco and HDR.
2. DisplayCAL > Display & instrument: choose the probe and the display's correction (spectral sample, e.g. for
   wide-gamut LED or OLED); wrong corrections give a large white point error.
3. Calibration tab: set white point (D65 xy), tone curve, luminance. Use *Interactive display adjustment* first to
   set RGB gains/brightness on the monitor's OSD close to target, so less correction is done in the GPU's 8-bit LUT.
4. Profiling tab: patch set at least 1000+ patches for an XYZ LUT + matrix profile on good displays.
5. Install the profile. For video pipelines, also create a **3D LUT** for the grading app or LUT box
   (see `creative-arts.animation.color.calibration-luts-in-the-monitoring-path`).

## Verify

DisplayCAL > Verification with the "verify extended" chart: average dE2000 under 1.0 and max under 3.0 for a
grading display (under 2/5 acceptable for artist screens). Save the HTML report with date and probe; recheck
monthly, since panels drift.
