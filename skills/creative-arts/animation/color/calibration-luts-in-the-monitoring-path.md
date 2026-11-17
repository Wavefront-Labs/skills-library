---
id: creative-arts.animation.color.calibration-luts-in-the-monitoring-path
name: calibration-luts-in-the-monitoring-path
category: creative-arts
field: animation
product: color
tags: [calibration-lut, monitor-calibration, 3d-lut, lut-box, resolve-monitor-lut, displaycal, colour-management, video-monitoring]
level: advanced
status: draft
description: "Put a display calibration 3D LUT in the right place in the monitoring path (monitor, LUT box or the grading app's output) so it corrects viewing only, never the render."
sources:
  - https://displaycal.net/
  - https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_19_Reference_Manual.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Calibration LUTs in the monitoring path

**Goal:** the calibration correction is applied once, to what the monitor shows, and never baked into
deliverables.

## Where the LUT can live

| Location | Pros | Cons |
|---|---|---|
| Monitor's internal LUT (reference monitors, some prosumer displays via vendor software) | correction in hardware, no app config, all sources corrected | needs a supported display |
| External LUT box (e.g. a Blackmagic or Teradek LUT box) between video I/O card and monitor | any monitor, hardware | extra box, 33-point limits on some |
| Grading app's monitor LUT (Resolve: Project Settings > Color Management > Lookup Tables > Video monitor lookup table) | free | only that app's video output is corrected |
| OS ICC profile | corrects the desktop for colour-managed apps | does not apply to video outputs; unmanaged apps ignore it |

## Making the LUT

DisplayCAL > *3D LUT* tab: source colour space Rec.709 ITU-R BT.709, tone curve BT.1886 (or the target), format
`.cube` (Resolve) or the LUT box's format, size 33 or 65. Measure through the same signal path you will use (video
card output, not the desktop GPU) (see `creative-arts.animation.color.displaycal-monitor-profiling`).

## Rules

1. In Resolve the video monitor LUT and the viewer LUT are **separate** from timeline LUTs; never put a calibration
   LUT on a node.
2. One correction only: do not use an ICC profile and a LUT box on the same signal.
3. Name LUTs with the display serial and date; a LUT for one panel is wrong for another of the same model.

## Verify

Render a test pattern from the timeline with the calibration LUT enabled for monitoring: the rendered file's pixel
values equal the source pattern (the LUT did not bake in), and the monitor measures on target with the LUT active.
