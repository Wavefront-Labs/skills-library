---
id: creative-arts.photography-fine-art.large-format-cameras.bellows-factor-and-reciprocity-correction
name: bellows-factor-and-reciprocity-correction
category: creative-arts
field: photography-fine-art
product: large-format-cameras
tags: [large-format-cameras, view-camera-focusing, bellows-extension-compensation, bellows-factor, reciprocity-failure, long-exposure-film, close-up-exposure]
level: practitioner
status: draft
description: "Correct large-format exposure for bellows extension at close focus and for film reciprocity failure at long times, with formulas and manufacturer tables."
sources: ["Leslie Stroebel, View Camera Technique, 7th ed. (Focal Press) (exposure)", "https://www.ilfordphoto.com/ (Ilford reciprocity failure data)", "https://imaging.kodakalaris.com/ (Kodak film datasheets - reciprocity)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Bellows factor and reciprocity correction

## Bellows extension
At close focus the lens is farther from the film, so the image dims.
- **Bellows factor** = (extension / focal length)^2. Stops = 2 x log2(extension / focal length).
- Example: 150 mm lens racked to 225 mm: (225/150)^2 = 2.25 x = about +1.2 stops.
- Negligible (under 1/3 stop) beyond about 10x the focal length subject distance.
- Tools: measure the extension (lens board to film plane) with a tape; or a bellows factor card ("QuickDisk"
  placed in the scene and measured on ground glass).

## Reciprocity failure (film)
At long exposures film loses effective speed. Example published adjustments:
- **Ilford** (HP5, FP4, Delta): adjusted time Tc = Tm^p with p about 1.31 (HP5 Plus) / 1.26 (FP4 Plus) /
  1.48 (Pan F) - check the current datasheet. 10 s metered on HP5 Plus -> about 20 s.
- **Kodak Tri-X/T-Max**: table: e.g. 10 s metered -> +2 stops and reduced development.
- Fuji Acros II needs no correction up to 120 s.
- Colour films also shift colour (filtration required).

## Order of operations
Apply bellows factor first to get the metered time, then apply reciprocity to that time.

## Gotchas
- Contrast increases with reciprocity failure - reduce development (N-) as datasheets advise.
- Digital spot meters don't know about either; write corrections on the exposure record.

## Verify
- [ ] Close-up and long exposures produce shadow density matching normal exposures.
