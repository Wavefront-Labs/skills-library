---
id: creative-arts.animation.vector-graphics.vector-rigging-for-2d-animation
name: vector-rigging-for-2d-animation
category: creative-arts
field: animation
product: vector-graphics
tags: [vector, vector-graphics, rigging, 2d-rig, cutout-animation, puppet, bones, ik, svg, inkscape, after-effects, duik, moho, spine, dragonbones, toon-boom, mesh-deform, pivot-points, z-order]
level: practitioner
status: draft
description: "Rig layered flat vector art (SVG/curves) into a bone/puppet hierarchy for cutout-style 2D animation: layer prep, pivots, bone chains, mesh deform, IK."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Vector rigging for 2D (cutout) animation

**What it is:** turning a flat, layered vector illustration — not a single path, a
*stack* of separate parts (torso, upper arm, forearm, hand, head, jaw...) — into a
puppet that an animator can pose and move without redrawing. This sits downstream of
`shapes-paths` (which builds the clean vector art) and is distinct from
`vector-asset-optimisation-for-animation` (which is about export weight, not
poseability) and `svg-pipeline-for-motion-graphics` (which is procedural motion
graphics, not a character puppet). Any 2D rigging tool works from the same mental
model below — Adobe After Effects + DUIK, Moho (Anime Studio), Toon Boom Harmony,
Spine, DragonBones, or hand-rolled SVG+bones in a game engine. Concrete steps below
are written for the AE/DUIK and Moho workflows since those are the ones I've actually
rigged in; treat the Harmony/Spine specifics as **unconfirmed by me — status: draft**
and check current docs before relying on exact menu names.

## 1. Prep the artwork before it ever touches a bone
- **Separate every part that must move independently onto its own layer**, each drawn
  *larger than its visible silhouette* at the joints (the classic "shoulder pad"
  overlap) so a rotation doesn't reveal a gap. Elbows, knees, shoulders, and the
  jaw/neck all need this overlap margin.
- **Draw each part in its full range of motion**, not just the rest pose, so you catch
  missing coverage (a sleeve that's too short when the arm bends) before rigging, not
  after.
- Convert strokes to paths and simplify (fewer anchors) per `shapes-paths` — a bone
  deform amplifies every kink a sloppy path already had.
- Decide **z-order (depth) up front**: far arm behind torso behind near arm is a
  layer-stacking decision, not something a bone can fix later. Re-stacking after
  rigging means re-parenting everything above the moved layer.

## 2. Pivots are the single most consequential decision
Every joint's pivot (anchor point / registration point) must sit exactly at the real
anatomical joint, not at the layer's bounding-box center (the default in most tools).
A pivot off by even a few px reads as a limb swinging from the wrong socket the moment
you rotate it.
- In AE: Pan-Behind tool, snap to the joint using the underlying art as a guide (zoom
  in; eyeball-snapping on a hip joint is the #1 source of "why does this leg skate").
- In Moho: the bone's base point IS the pivot — place the bone so its root sits on the
  joint and its tip reaches toward the next joint (the bone's length matters for which
  mesh points it influences).
- **Gotcha:** if you re-pivot a layer *after* you've already keyframed it, every
  existing keyframe's rotation value now orbits around the new point — re-pivot before
  you animate, not mid-shot.

## 3. Bone hierarchy and parenting
Build the hierarchy root-to-extremity, matching real anatomy so FK rotation composes
correctly: hip → root; spine → hip; shoulder → spine; upper-arm → shoulder; forearm →
upper-arm; hand → forearm. Each child's transform is relative to its parent, so
rotating the shoulder correctly carries the whole arm with it — this is *why* you rig
instead of hand-animating 8 disconnected layers.
- **FK (forward kinematics)** — rotate from the root outward; natural for arcing,
  sweeping limb motion (a wave, a walk's arm swing). Default for most of a cutout rig.
- **IK (inverse kinematics)** — place the end effector (hand/foot) and the chain solves
  the joint angles; essential for feet that must stay planted on the ground or hands
  that must stay locked to a held prop. Rig legs with an IK chain + a pole/knee target
  so the knee doesn't flip direction unpredictably; rig arms FK unless the character is
  gripping something fixed.
- Keep a **separate "no-flip" pole target** on every IK knee/elbow — without one, the
  solver will occasionally snap the joint to the wrong side on a big pose change.

## 4. Mesh deform for bending parts (not just rigid rotation)
A rigid layer rotated at the elbow looks like a hinge with no flesh. For anything that
should visibly bend (upper arm, torso, a tail), apply a **deformable mesh** over the
art (AE's Puppet Pin/Mesh tool, Moho's "Flexi-Bind" / smart bones, Spine's weighted
mesh) and bind mesh points to bones with falloff weights, heavier near the bone, fading
toward the neighboring joint's influence zone — this is literally the same weight-
painting concept as 3D skinning, just in 2D.
- **Gotcha:** a bend with too-sharp weight falloff creases the art like folded paper;
  too-soft falloff and the limb barely deforms. Preview mid-range poses (45°, not just
  rest and full extension) while tuning weights — artifacts usually hide at the
  extremes you're not looking at.
- Mouth/jaw and eyelids are usually simpler: swap-layer (discrete mouth shapes per
  viseme) rather than mesh-deform, since speech shapes are categorical, not a smooth
  bend — see `lip-sync` for the viseme set.

## 5. Z-depth tricks and the "turnaround" problem
A 2D puppet rotating past ~45° toward profile breaks the illusion (parts that should
go behind now overlap wrong). Options, roughly in order of effort:
- Build and swap to a **dedicated profile/3-quarter layer set** for big turns (most
  robust, most art).
- Fake depth with **per-part z-position in a pseudo-3D space** (AE 3D layers, or
  Harmony's z-depth) so a camera move or slight turn re-sorts automatically without a
  full redraw — works for small turns only.
- Accept the limitation and **block staging to avoid big turns** on a 2D cutout rig —
  often the cheapest real answer for a flat character.

## 6. Controller layer and animator-facing rig
Don't hand the animator raw bones/layers — expose a controller set: named sliders or
null/control shapes for brow, mouth-shape index, IK/FK switch per limb, and a global
root control that moves the whole puppet without breaking IK foot locks. Group and
colour-code controls so a timeline full of keys is still legible months later.

## Verify
- [ ] Every independently-moving part is its own layer, drawn with joint overlap
      margin, in multiple test poses (not just rest).
- [ ] Every pivot sits on the real joint, set *before* any keyframing.
- [ ] Hierarchy matches anatomy root-to-extremity; legs/feet on IK with a pole target,
      arms FK unless gripping something fixed.
- [ ] Mesh-deform weights checked at a mid-range pose (e.g. 45° elbow bend), not just
      the extremes.
- [ ] A plan exists for turns past ~45° (swap set, pseudo-3D depth, or staged to avoid
      it) — not discovered live in animation.
- [ ] Animator-facing controls are named/exposed, not raw bone manipulation.

See also: `shapes-paths.md` (the clean vector art this rigs), `svg-pipeline-for-
motion-graphics.md` (procedural motion vs. a posed puppet),
`vector-asset-optimisation-for-animation.md` (export weight of the rigged asset),
and `../blender/acting-performance.md` / `../blender/lip-sync.md` for the
performance layer once the rig exists (the acting principles transfer directly;
only the control mechanism differs).
