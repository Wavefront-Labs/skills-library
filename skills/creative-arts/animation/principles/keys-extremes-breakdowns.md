---
id: creative-arts.animation.principles.keys-extremes-breakdowns
name: keys-extremes-breakdowns
category: creative-arts
field: animation
product: principles
tags: [animation, pose-to-pose-method, keys-extremes-breakdowns, keys, extremes, breakdowns, inbetweens, planning, numbering, 2d, cg]
level: practitioner
status: draft
description: "Plan a shot as keys (storytelling poses), extremes (limits of motion) and breakdowns (the in-between that defines the path), with Williams-style numbering and circled keys."
sources:
  - https://books.google.com/books?vid=ISBN9780865478978
  - https://books.google.com/books?vid=ISBN9780786860708
  - https://en.wikipedia.org/wiki/Inbetweening
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Keys, extremes and breakdowns

Goal: build a shot from a clear hierarchy of drawings/poses so the story reads from the
fewest poses and every later pass only refines. Richard Williams' distinction is the
industry vocabulary.

## Definitions (Animator's Survival Kit)
- **Key** - a storytelling pose; the drawings you would show to explain the shot. Circled on
  the chart.
- **Extreme** - the point where motion changes direction (top of a jump, the end of a swing).
  Often also a key; marked with a box or a circled number with "X" in some studios.
- **Breakdown** - the first in-between between two extremes; decides the path and the character
  of the move (it is "the passing position"). Underlined on the chart.
- **Inbetween** - everything else, drawn to the chart's spacing.

## Method
1. Thumbnail the shot to find 2-6 keys that tell the story with no motion.
2. Time the keys to the dialogue/action on the exposure sheet or timeline (stepped).
3. Add extremes wherever a part of the body changes direction.
4. Add breakdowns - this is where the motion gets its personality (see
   `creative-arts.animation.principles.designing-the-breakdown`).
5. Write timing charts on each key: how many inbetweens and where they favour.
6. Only then inbetween or spline.

## Numbering
- Drawings numbered by frame on ones (1, 3, 5... for twos). Keys circled, breakdowns
  underlined, inbetweens plain.
- In CG, mirror this with key colors (Maya: key/breakdown tick types; Blender: keyframe types
  Keyframe / Breakdown / Moving Hold / Extreme / Jitter, set with R in the Dope Sheet).

## Failure modes
- Too many keys: the shot is pose-to-pose but stiff; let breakdowns do the work.
- Missing extremes: arcs flatten because the direction change happens between keys.
- Treating breakdowns as mid-points: a 50 % breakdown is a wasted opportunity.

## Verify
- [ ] Keys alone (stepped) tell the story to a viewer.
- [ ] Every direction change has an extreme.
- [ ] Each breakdown is deliberately off-centre or off-path to shape the move.
- [ ] Charts exist for every key-to-key interval.

Related: `creative-arts.animation.principles.applying-timing-and-spacing`,
`creative-arts.animation.principles.stepped-blocking-to-spline`.
