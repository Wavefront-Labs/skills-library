---
id: creative-arts.visual-art.digital-illustration.tablet-pressure-curves-and-setup
name: tablet-pressure-curves-and-setup
category: creative-arts
field: visual-art
product: digital-illustration
tags: [visual-art, digital-illustration, digital-brushes, brush-engine, pressure-curve, tablet-setup, wacom, krita, clip-studio-paint, pen-pressure, windows-ink, mapping]
level: intro
status: draft
description: "Set up a drawing tablet: driver, proportional mapping, Windows Ink vs WinTab, pressure curves in Krita and Clip Studio, and fixing lost pressure."
sources: ["https://docs.krita.org/en/reference_manual/preferences/tablet_settings.html", "https://www.wacom.com/en-us/support"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tablet pressure curves and setup

**Goal:** a tablet that responds predictably, so light pressure gives light marks
and full pressure arrives without straining (Krita Manual, tablet settings;
Clip Studio Paint user guide, pen pressure settings).

## Driver and mapping
1. Install the current manufacturer driver (Wacom, Huion, XP-Pen); remove old ones.
2. **Mapping**: map the tablet area to one monitor; enable "force proportions"
   so a circle on the tablet is a circle on screen.
3. Pen buttons: set to useful functions (e.g. eyedropper, undo, pan) rather than
   right-click if you rarely use it.

## API (Windows)
- **Windows Ink** vs **WinTab**: apps support one or both. Krita: Settings >
  Configure Krita > Tablet settings lets you choose. If pressure does not work,
  try the other API and toggle Windows Ink in the driver.
- macOS uses one API; check accessibility permissions after updates.

## Pressure curves
- **Driver curve** (global): sets overall firmness ("soft" = less pressure
  needed).
- **App curve**: Krita global curve in tablet settings, plus each brush preset's
  pressure curves for size/opacity; Clip Studio: File > Adjust pen pressure
  detection level (Windows) / Clip Studio Paint > Adjust pen pressure (macOS),
  where you draw strokes and it fits a curve; per sub tool settings too.
- Set one curve globally first (drivers or app, not heavily both) then fine-tune
  per brush.

## Testing
Draw a stroke from lightest to heaviest pressure; you should get a smooth taper
from thin/light to full without a "jump" or needing to press very hard.

## Gotchas
- Pressure lost after a driver update or OS update: reinstall driver, restart app.
- Double curve stacking (driver very soft + app very soft): twitchy, hard to control.
- Screen tablets: calibrate pen parallax in the driver.

## Verify
- [ ] Mapping proportional; correct monitor.
- [ ] Smooth pressure ramp across the full range.
