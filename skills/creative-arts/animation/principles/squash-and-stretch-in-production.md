---
id: creative-arts.animation.principles.squash-and-stretch-in-production
name: squash-and-stretch-in-production
category: creative-arts
field: animation
product: principles
tags: [animation, squash-and-stretch, volume-preservation, weight, impact, rubber-hose, rigging, deformation, blendshapes, lattice, cartoon-physics, flour-sack, rig-controls]
level: practitioner
status: draft
description: "How much to squash/stretch, on which rig controls, so impacts read as weight instead of a rubber-hose wobble."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Squash and stretch in production

Squash and stretch is the principle most new animators overdo or apply in
the wrong place: either everything wobbles like it's made of rubber (the
"rubber hose" failure that gave the principle its bad reputation outside
hand-drawn shorts), or it's skipped on CG/rigged work entirely because
"the rig doesn't support it," producing stiff, dead impacts. This skill is
about budgeting *how much*, *where*, and *on what controls*, in a real
production pipeline (rig-based or hand-drawn) — not restating that the
principle exists.

## The volume rule
The core constraint that keeps it from looking like rubber: **volume is
conserved**. If something squashes 20% shorter on impact, it must get
correspondingly wider (not infinitely — enough to sell "same amount of
stuff, different shape"). If it stretches 30% longer mid-fall, it gets
thinner. Animate this as a ratio, not independent axes:
- Simple rig rule of thumb: scale Y to 0.8 → scale X and Z to roughly
  1/sqrt(0.8) ≈ 1.12 each (true volume-preserving inverse-scale), or a
  cheaper practitioner shortcut of just inverse-scaling X/Z by the same
  delta (0.8 down → 1.2 up) — looks close enough for most shots and is one
  driver instead of a square-root expression.
- Break the rule deliberately for comedy/cartoon-physics (Tex Avery-style
  stretch with no corresponding thinning reads as a gag, not a mistake) —
  but that's a choice to name in the shot notes, not a default.

## Where to apply it (budget per shot, not per character)
- **Hero squash/stretch beats**: impacts (landing, catching, getting hit),
  takes (a surprised recoil), and stretch-on-anticipation (winding up to
  jump). These are the frames worth spending rig/shape-key budget on.
  Typically 1–3 per shot, not continuous.
- **Secondary/ambient squash**: a torso compressing slightly on a footstep,
  a belly jiggle after landing — subtle, often under 5% scale delta, there
  to support weight not call attention to itself.
- **Don't squash the whole rig uniformly.** Squash is usually localized:
  the torso/root on a landing, a limb at the point of contact, a face shape
  on an exaggerated take. Scaling every bone in the hierarchy by the same
  amount is what produces the rubber-hose look — the deformation needs a
  gradient (more at the impact point, less as you move away from it) not a
  flat multiplier.

## How, by pipeline
- **Rig-based (Blender/Maya rigs):** squash/stretch on the root or
  COG (center-of-gravity) control for whole-body impacts; on IK stretch
  bones (if the rig has stretchy IK) for limb reach/snap; corrective
  blendshapes/shape keys layered on top near full squash to fix volume
  loss the skin weights alone won't handle (a knee or elbow at full squash
  often needs a shape key correction, not just scale).
  - Verified pattern (Blender): keyframe scale on the COG empty, set
    volume-preserving inverse scale on the orthogonal axes as a driver
    expression (`1/sqrt(cog.scale.y)`) so animators only touch one slider.
  - Gotcha: scaling a bone non-uniformly inside an armature can pinch
    child-bone skin weights at the joint — test the extreme pose before
    committing the shot; add a corrective shape key if it pinches.
- **Hand-drawn / 2D:** redraw the volume at the extreme rather than
  scaling a puppet — squash/stretch is drawn as a *shape change*, which is
  why 2D squash reads more convincing by default: the artist is already
  preserving perceived mass by eye, not fighting a uniform-scale rig.
- **Cutout/rigged 2D (e.g. bone-based 2D rigs):** same volume-ratio rule as
  3D rigs, but watch texture stretching on stretch frames — UV distortion
  is the 2D equivalent of the rig pinching.

## Gotchas
- Squash/stretch without a settle afterward (no follow-through back to
  rest volume) looks like a glitch, not a bounce — pair with
  `creative-arts.animation.principles.anticipation-and-follow-through-staging`
  for the recovery frames.
- Faces: squash/stretch on facial shapes (a take, a scream) needs to
  respect topology — stretching a mouth shape key too far can break UVs or
  push verts through other geometry; always check at the shot's actual
  camera angle, not just front-on in the rig view.
- Realistic/semi-realistic characters tolerate far less squash/stretch
  than cartoon ones before it looks like a rendering glitch rather than a
  stylistic choice — scale the effect down by render style, not just by
  "is this a cartoon."
- Uncertain: the 1/sqrt volume-preservation formula and the Blender COG
  driver pattern are verified on a hand-built rig; the "5%/1-3 hero beats
  per shot" budgeting numbers are practitioner heuristics, not measured
  across a large sample — treat as a starting point to recalibrate per
  show style.

## Verify
- [ ] Every squash/stretch beat has a corresponding inverse scale on the
      orthogonal axis (volume ratio check), unless the break is deliberate
      and noted.
- [ ] Deformation is localized/graduated at the impact point, not a flat
      scale on the whole rig.
- [ ] Extreme pose checked for skin-weight pinching or shape-key topology
      breaks at the actual camera angle used in the shot.
- [ ] Hero squash/stretch beats counted per shot and deliberate (not
      incidental to every pose).
- [ ] Squash/stretch beat resolves with a settle/follow-through, not a
      hard cut back to rest.

Related: `creative-arts.animation.principles.twelve-principles` (squash &
stretch as principle #1), `creative-arts.animation.principles.applying-timing-and-spacing`
(how many frames the squash/recovery takes), `creative-arts.animation.principles.anticipation-and-follow-through-staging`
(the wind-up stretch and the settle after impact).
