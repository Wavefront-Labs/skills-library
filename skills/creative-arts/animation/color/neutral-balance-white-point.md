---
id: creative-arts.animation.color.neutral-balance-white-point
name: neutral-balance-white-point
category: creative-arts
field: animation
product: color
tags: [white-balance, neutral-balance, white-point, d65, colour-temperature, primary-grading, resolve, scopes, grey-balance]
level: practitioner
status: draft
description: "Neutralise colour casts and set the white point in a grade: find a true neutral, balance with offset/gain, use temperature/tint, and know when a cast is the look."
sources:
  - https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_19_Reference_Manual.pdf
  - https://www.itu.int/rec/R-REC-BT.709
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Neutral balance and white point

**Goal:** neutrals (whites, greys, blacks) read neutral unless the colour script says otherwise, so the deliberate
looks sit on a clean base.

## Find a neutral

- Pick something that should be colourless in the fiction: a white wall, grey concrete, black outlines, a white
  shirt. In CG animation, line art and greyscale props are excellent neutrals.
- Do not balance on skin, sky or the hero colour.

## Balance

1. **Blacks:** with the RGB parade (see `creative-arts.animation.color.rgb-parade-balancing`), Lift or Offset so the
   bottom of R, G and B traces line up.
2. **Whites:** Gain so the tops line up on the neutral highlight.
3. **Mids:** Gamma for the mid-grey patch; check on the vectorscope that neutrals sit on the centre dot
   (see `creative-arts.animation.color.vectorscope-and-skin-tone-line`).
4. In Resolve, the Primaries **Temp/Tint** controls (and the white-balance picker on the Camera Raw or Primaries
   palette) shift along the blackbody/green-magenta axes, which reads more natural than raw RGB moves.
5. In ACEScct, Offset per channel is the cleanest balance (see `creative-arts.animation.color.printer-lights-offset-grading`).

## White point

- SDR Rec.709 and sRGB deliveries use **D65** (6504 K) white. The grading display must be calibrated to D65
  (see `creative-arts.animation.color.displaycal-monitor-profiling`); a 5500 K monitor makes every grade too blue
  on everyone else's screen.
- DCI cinema uses the DCI white (about 6300 K, greenish); P3-D65 for streaming HDR.

## When a cast is the look

Night scenes are graded blue, sunsets warm; this is a creative offset on top of a neutral base, done on a later
node so it can be dialled per shot. Note the intent in the colour script so nobody "corrects" it.

## Verify

Neutral reference objects plot on the vectorscope centre and the parade channels overlap on them, on the base
balance node, before any look nodes.
