---
id: creative-arts.visual-art.procreate.pressure-curve-and-smoothing-settings
name: pressure-curve-and-smoothing-settings
category: creative-arts
field: visual-art
product: procreate
tags: [visual-art, procreate, procreate-pressure, pressure-curve, smoothing, apple-pencil, procreate-prefs, pressure-and-smoothing]
level: practitioner
status: draft
description: "Tune the Procreate pressure curve and smoothing in Pressure and Smoothing preferences so Apple Pencil or stylus strokes match your hand."
sources: ["https://procreate.com/handbook"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Pressure and smoothing settings in Procreate

**Goal:** make light and heavy strokes map to the line weight and opacity you expect, and remove hand jitter, using the app-wide settings (as opposed to per-brush dynamics; see `creative-arts.visual-art.procreate.brush-dynamics-and-apple-pencil-response`).

## Steps
1. Open **Actions (wrench) > Prefs > Pressure and Smoothing**. (Handbook section on Prefs; menu labels may differ slightly by version.)
2. **Pressure curve:** a graph maps input pressure (horizontal) to output pressure (vertical). Drag the curve up in the low end to make light touches register more; drag it down for a firmer feel. A straight diagonal is neutral.
3. **Smoothing:** a global smoothing slider averages input to reduce jitter. It works together with each brush's own StreamLine and Stabilization, so heavy global smoothing plus a stabilised brush feels sluggish.
4. Use the **test area** in the panel, scribbling light to hard, and re-adjust until a natural stroke gives the full range of tone.
5. Non-Apple styluses and finger drawing do not report the same pressure data; set curve expectations accordingly. Third-party pressure-sensitive styluses vary in support.

## Gotchas
- Changing the curve changes **every** brush at once; if only one brush feels wrong, edit that brush's Apple Pencil settings instead.
- A very bent curve causes all-or-nothing strokes with no mid-tones.
- Pencil input latency is not a pressure setting; do not blame the curve for lag.

## Verify
- [ ] A feather-light stroke leaves a thin or faint mark, a hard stroke a thick or opaque one, with a smooth gradient between.
- [ ] A slow straight line has no visible jitter at your chosen smoothing.
