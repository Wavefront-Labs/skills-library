---
id: creative-arts.comics-and-sequential-art.inking.removing-non-photo-blue-from-scans
name: removing-non-photo-blue-from-scans
category: creative-arts
field: comics-and-sequential-art
product: inking
tags: [inking, ink-corrections, line-art-prep, non-photo-blue-removal, blueline-dropout, channel-mixer, hue-saturation, blue-pencil]
level: practitioner
status: draft
description: "Drop non-photo blue pencils or printed bluelines out of scanned inks: colour scan, keep the right channel or use Hue/Saturation, then threshold, with checks for leftover blue."
sources:
  - https://en.wikipedia.org/wiki/Non-photo_blue
  - https://helpx.adobe.com/photoshop/using/channel-basics.html
  - https://openlibrary.org/search?q=DC+Comics+Guide+to+Inking+Comics
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Removing non-photo blue from scans

**Goal:** blue pencil roughs or blueline prints vanish completely, leaving only ink.

## Background
Non-photo blue was chosen because old graphic-arts (lith) film didn't register it.
Digital scanners do see it, so you remove it in software.

## Method A: channel (fastest, very clean)
1. **Scan in RGB colour** (not greyscale), 600 ppi.
2. Open Channels; view the **Blue** channel alone (in some cases Green or a mix works
   better; light blue is brightest in the blue channel, black ink stays dark in all).
3. Select the Blue channel > Select All > Copy; create a new greyscale document or
   use Image > Mode > Grayscale after deleting the other channels (Image > Mode >
   Multichannel, delete Red and Green), or use Channel Mixer (Monochrome, Blue 100%).
4. Apply Levels/Threshold as for normal line art.

## Method B: Hue/Saturation
1. Image > Adjustments > Hue/Saturation, choose Cyans and Blues ranges, push
   Lightness to +100 and Saturation down.
2. Widen the range sliders if some blue remains.
3. Convert to greyscale and threshold.

## Tips
- Darker blue pencils (or heavy pressure) don't drop out fully; use light pressure,
  true non-photo blue leads/pencils.
- Printed bluelines: print in a light cyan (e.g. C 30-50%) so they drop easily.
- Avoid blue ink highlights or colour notes you want to keep.

## Verify
- [ ] At 100% zoom no blue residue or grey ghost lines after threshold.
- [ ] Fine ink lines unaffected.
