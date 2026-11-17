---
id: creative-arts.photography-fine-art.art-photography.photographing-star-trails
name: photographing-star-trails
category: creative-arts
field: photography-fine-art
product: art-photography
tags: [art-photography, night-photography, star-trails, starstax, intervalometer-stacking, polaris, circumpolar]
level: practitioner
status: draft
description: "Shoot star trails by stacking many short exposures (StarStaX), placing Polaris for circles, and avoiding gaps, dew and battery failure."
sources: ["https://markus-enzweiler.de/software/starstax/", "https://www.photopills.com/articles/star-trails-photography-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Photographing star trails

## Plan
- Point toward **Polaris** (northern hemisphere) or the south celestial pole (Sigma Octantis area)
  for concentric circles; east/west gives diagonal streaks.
- Total time sets arc length: 15 deg per hour. 1 hour = 15 deg arcs; 2-3 h for strong circles.
- Moonlit nights light the landscape; new moon gives more stars.

## Capture (stacking method)
1. Manual focus on stars, manual exposure: e.g. 30 s, f/4, ISO 400-800.
2. Continuous drive with a locked remote, or intervalometer with 1 s interval (as short as the camera allows) to minimise gaps.
3. Disable long-exposure noise reduction (it creates gaps equal to exposure time).
4. Shoot 120-360 frames. Spare battery or USB power; lens heater.
5. A few dark frames (lens cap on) at the end for hot pixel subtraction.

## Stacking
StarStaX: load images, Lighten blend mode (or Gap Filling), add dark frames, export.
Photoshop: load as layers, Lighten blending (slow with hundreds).

## Gotchas
- Aircraft lights make dashed lines; remove those frames.
- Single multi-hour exposures on digital produce heavy noise/heat; stacking is preferred.

## Verify
- [ ] Trails continuous without gaps; foreground clean.
