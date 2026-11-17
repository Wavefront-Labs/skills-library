---
id: creative-arts.photography-fine-art.art-photography.inverse-square-law-and-falloff
name: inverse-square-law-and-falloff
category: creative-arts
field: photography-fine-art
product: art-photography
tags: [art-photography, quality-of-light, inverse-square-law, light-falloff, background-control, light-distance]
level: practitioner
status: draft
description: "Use the inverse square law to control light falloff across a subject and background: distances, stops, and placing lights for even or dramatic fall-off."
sources: ["Hunter, Biver, Fuqua, Light Science and Magic, 5th ed. (Routledge) ch.2", "https://en.wikipedia.org/wiki/Inverse-square_law"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Inverse square law and falloff

Illumination from a point-like source falls with the square of distance:
double the distance = **1/4 the light = -2 stops**. x1.4 distance = -1 stop.

## Practical uses
- **Even light across a group**: move the light farther away; the ratio between near and far
  persons shrinks (light at 2 m, people 2 and 3 m: 1.2 stops difference; light at 6 m,
  people 6 and 7 m: 0.45 stop).
- **Dark background without a black backdrop**: light close to subject, background far
  behind; subject at 1 m and background at 4 m = 4 stops darker.
- **Lighter background**: move subject close to background or light the background separately.

## Procedure
1. Measure subject-to-light and background-to-light distances.
2. Compute stops difference: 2 x log2(d2/d1).
3. Adjust light distance (and power to keep subject exposure).
4. Confirm with an incident meter at each position or with test frames.

## Gotchas
- Large softboxes close to the subject behave less than point-like; falloff is gentler than
  the formula until you are about 2-3x the box diagonal away.
- The sun is effectively infinitely far: no falloff, which is why daylight looks even.

## Verify
- [ ] Measured stop difference between subject and background matches your plan.
