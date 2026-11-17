---
id: creative-arts.photography-fine-art.darkroom-practice.f-stop-printing-and-print-size-changes
name: f-stop-printing-and-print-size-changes
category: creative-arts
field: photography-fine-art
product: darkroom-practice
tags: [darkroom-practice, enlarging, f-stop-timing, print-size-exposure-change, test-strip-method, f-stop-timer, inverse-square-enlarging]
level: practitioner
status: draft
description: "Make test strips in f-stop increments and recalculate exposure when enlarging or reducing print size, so dodges and burns scale correctly."
sources: ["Gene Nocon, Photographic Printing (f-stop printing)", "https://www.rhdesigns.co.uk/ (RH Designs f-stop timer manual)", "Ansel Adams, The Print (Little, Brown)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# F-stop printing and print-size changes

## F-stop timing
Linear test strips (5, 10, 15, 20 s) give uneven steps: 5->10 is a full stop, 15->20 is 0.4 stop.
**F-stop steps** are equal ratios: each 1/3 stop = x1.26; 1/6 stop = x1.12.

Example in 1/3 stops from 8 s: 8, 10, 12.7, 16, 20, 25.4 s.

## Test strip procedure
1. Expose a strip in incremental steps (cover progressively), each step adding 1/3 stop (with an f-stop
   timer like RH Designs StopClock/Analyser it does the arithmetic).
2. Place the strip across important highlight and shadow areas.
3. Choose base exposure for the highlights; then set contrast for shadows.
4. Express dodges and burns as fractions of a stop (e.g. "burn sky +2/3 stop") - they transfer between
   print sizes and papers.

## Changing print size
Exposure scales with the **square of magnification ratio** (column height distance lens-to-paper):
new time = old time x (new lens-to-paper distance / old distance)^2.
Practical: measure image width of the same detail: new time = old time x (new width / old width)^2.
8x10 at 20 s -> 16x20 (width doubles) = 80 s (+2 stops). Open the aperture 1-2 stops to keep times reasonable.

## Gotchas
- Reciprocity failure in paper at very long or short times; retest after big changes.
- Very short times (< 5 s) make dodging impractical - stop down.

## Verify
- [ ] Printing notes in stops; size change exposure calculated and confirmed with one strip.
