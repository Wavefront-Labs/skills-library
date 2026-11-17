---
id: creative-arts.animation.principles.smear-frames-and-multiples
name: smear-frames-and-multiples
category: creative-arts
field: animation
product: principles
tags: [animation, smear-frames, multiples, squash-and-stretch, motion-blur, speed-lines, fast-action, cartoon, 2d, cg, smear-rig]
level: practitioner
status: draft
description: "Use smears, multiples and speed lines to carry very fast motion between poses that are too far apart for inbetweens, in 2D and in CG smear rigs."
sources:
  - https://books.google.com/books?vid=ISBN9780865478978
  - https://books.google.com/books?vid=ISBN9781560100843
  - https://en.wikipedia.org/wiki/Squash_and_stretch
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Smear frames and multiples

Goal: make a 1-3 frame move between two distant poses read as continuous motion instead of
a pop. When the gap between two drawings is bigger than the object itself, the eye loses
it; a smear or multiple fills the gap on one frame.

## The three tools
1. **Smear** - one drawing stretched along the path from the previous position to the next,
   thick at the leading end, tapering or dissolving at the trailing end. Use for a whole body
   or limb whipping across frame (Chuck Jones' Road Runner, the Dexter's Lab head turns).
2. **Multiples** - the moving part drawn 2-4 times along its path on the same frame (several
   hands, several legs in a spin-out). Use for repeated or rotating parts: feet in a scramble,
   a fist in a flurry, a head shake.
3. **Speed lines / drybrush** - lines trailing along the path with the object drawn solid at
   the leading position. Use when the object must stay on-model (a logo, a hero face).

## How to place them
- Put the smear on the frame(s) *between* keys where spacing exceeds about one object width.
  A 2-frame whip usually needs exactly one smear frame.
- Follow the arc: the smear is the arc itself, curved, not a straight streak.
- Leading edge is on the next pose's silhouette; trailing edge starts at the previous pose.
- Keep it to 1 frame at 24 fps (2 at most). On a still frame it looks grotesque - that is fine.
- Shoot it on ones even in a show animated on twos; a smear held for two frames reads as a
  deformed drawing.

## CG equivalents
- Smear rigs: lattice or curve deformers on the limb, a stretch attribute keyed for one frame,
  or duplicated geometry ghosts (multiples) toggled visible per frame.
- Motion blur alone is not a smear: render motion blur blurs everything with the shutter, a
  designed smear is directional and shaped. Many stylized CG features key both.
- Blender: Grease Pencil drawn over the 3D frame, or a shape key/lattice keyed for the single
  frame; Maya: a smear deformer or blendshape keyed on/off with stepped tangents.

## Failure modes
- Smearing slow motion: smears belong only where spacing is huge. Otherwise it looks broken.
- Straight smears on an arcing action: the path visibly snaps.
- Smear frames with detail (eyes, pattern) intact: the eye catches the detail and the frame
  reads as a mistake. Simplify inside the smear.
- Forgetting to restore volume on the following frame.

## Verify
- [ ] Playing at speed, the fast move reads as one motion, no pop or strobe.
- [ ] Stepping frame by frame, each smear sits on the arc between its neighbours.
- [ ] Smears last 1 frame (2 max) and are shot on ones.
- [ ] Removing the smear frame makes the move noticeably worse (otherwise it is not needed).

Related: `creative-arts.animation.principles.bouncing-ball-exercise`,
`creative-arts.animation.principles.squash-and-stretch-in-production`.
