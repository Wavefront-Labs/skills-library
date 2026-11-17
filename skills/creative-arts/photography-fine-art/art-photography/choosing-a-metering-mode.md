---
id: creative-arts.photography-fine-art.art-photography.choosing-a-metering-mode
name: choosing-a-metering-mode
category: creative-arts
field: photography-fine-art
product: art-photography
tags: [art-photography, exposure-control, metering-modes, matrix-metering, evaluative-metering, centre-weighted, spot-metering, highlight-weighted-metering, light-meter, middle-grey]
level: practitioner
status: draft
description: "Pick matrix/evaluative, centre-weighted, spot or highlight-weighted metering for a scene and know what each meter is averaging to mid-grey."
sources: ["https://www.ppa.com/cpp", "Ansel Adams, The Camera (exposure chapter)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choosing a metering mode

Every reflected-light meter answers one question: *what exposure renders the area I
measured as middle grey (about 18% reflectance, Zone V)?* Modes differ only in **which
area** is measured and how it is weighted.

| Mode | Measures | Use when | Fails when |
|---|---|---|---|
| Matrix / evaluative | whole frame in zones, compared to a scene database, weighted toward the focus point | fast-changing, average scenes | large bright/dark areas it guesses wrong (snow, black backdrop) |
| Centre-weighted | ~60-80% weight on central circle | portraits with subject centred; predictable, repeatable | subject off-centre |
| Spot (1-5% of frame) | tiny circle, often linked to AF point | deliberate tonal placement, backlit subjects, Zone System | you meter something not mid-toned and do not compensate |
| Highlight-weighted (Nikon) / similar | brightest areas | stage lighting, spot-lit subjects; protects highlights | shadows go very dark |

## Procedure
1. Ask: is the scene mostly mid-tone? -> matrix is fine; check the histogram.
2. Bright main subject on dark ground (or reverse)? -> spot-meter the subject and place it:
   white skin about +1, snow +1.7 to +2, black cloth -1.5 to -2 relative to the meter.
3. Repeated studio/portrait series? -> centre-weighted or manual exposure; matrix may
   shift exposure between frames as composition changes.
4. Lock exposure (AE-L) or switch to manual once found, so recomposing does not move it.
5. Confirm with the histogram and blinking highlights, not the LCD brightness.

## Gotchas
- Spot metering on many bodies follows the active AF point; on some it is fixed centre.
  Check your menu.
- Incident meters (handheld, dome toward camera) avoid the reflectance problem entirely
  and are the most reliable for people and still life.
- JPEG preview histograms understate raw headroom by roughly 0.5-1 stop.

## Verify
- [ ] You can say what area was metered and what tone it should be.
- [ ] Histogram confirms no unwanted clipping in highlights that matter.
