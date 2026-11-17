---
id: computing-software.game-programming.game-physics.ragdoll-and-physics-animation-blending
name: ragdoll-and-physics-animation-blending
category: computing-software
field: game-programming
product: game-physics
tags: [game-physics, ragdoll, powered-ragdoll, blend-ragdoll, animation-blending, active-ragdoll, get-up, physical-animation, ragdoll-transition, bone-mapping, ik, hit-reaction, game-programming, active-ragdolls]
level: advanced
status: gated
description: "Transition characters between animation and ragdoll physics without a visible pop, including powered/active ragdolls that stay partly animated."
sources: ["https://github.com/jrouwe/JoltPhysics", "https://nvidia-omniverse.github.io/PhysX/physx/5.4.1/docs/AdvancedCollisionDetection.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Ragdoll and physics/animation blending

**Goal:** switch a character between animated and physically-simulated (dead
weight) states, and back, without a jarring pop — and know the "powered
ragdoll" middle ground most AAA hit reactions actually use instead of either
pure extreme.

## The three states, not two
- **Fully animated**: bones driven entirely by the animation system; no
  physics simulation on the skeleton.
- **Full ragdoll**: every bone is a separate rigid body connected by joints
  (see `computing-software.game-programming.game-physics.constraint-solvers-and-joints`
  for how those joints behave), falling and colliding under physics alone,
  used for death/unconscious states where no intentional motion remains.
- **Powered/active ragdoll** (described by the skill author as the production middle ground for combat hit reactions (gated: unconfirmed, source is paywalled or blocked)): the skeleton is
  simulated as a ragdoll, but each joint has a motor driving it toward the
  pose the animation *would* have at that moment — so a hit staggers the
  character physically (physical reaction to impact force, limbs flailing
  believably) while the character still visibly tries to recover its stance,
  used for hit reactions in combat games that still need the character
  playable/responsive seconds later rather than lying there.

## The transition pop, and why it happens
Snapping from an animated pose straight into a ragdoll initialized at rest (or
vice versa) is visually jarring because the ragdoll's bones don't inherit the
animated skeleton's **velocity** — a character running full speed that gets
ragdolled appears to instantly stop and flop, because only position was
copied, not momentum. Fix: on ragdoll activation, compute each bone's linear
and angular velocity from the last 1-2 animation frames (position delta /
frame time) and set it as the rigid body's initial velocity before releasing
control to physics — this single step is responsible for most of the
difference between a ragdoll that looks "stiff then pops" and one that looks
like genuine momentum carrying through the hit.

## Blending back to animation (the "get up" problem)
Going from ragdoll back to animated control (character gets up after being
knocked down) has the same pop risk in reverse: the ragdoll's final resting
pose rarely matches any authored "get up" animation's start pose. Standard
approach: sample the ragdoll's resting bone transforms, pick (or procedurally
select, e.g. face-down vs face-up) the matching get-up animation, and **blend**
from the ragdoll pose into the animation's first pose over a short window
(a few frames of pose interpolation, not an instant cut) rather than snapping
directly into the animation. Jolt's `Ragdoll` offers `GetPose` (read the simulated pose to blend from),
`SetPose` and `DriveToPoseUsingKinematics`; other engines need custom code or their own blend utility.

## Bone mapping and joint setup gotchas
- The ragdoll's rigid-body hierarchy must map 1:1 to the skinning skeleton's
  bones used for the hit-reaction/get-up animations — a ragdoll built on a
  different bone count/naming than the animation rig silently fails to blend
  correctly (bones snap to origin or don't move).
- Collision layers: ragdoll bones should not collide with their jointed neighbours
  (they fight their own joint constraint) — set up a collision
  filter excluding directly-connected bones, enabling only non-adjacent
  self-collision if needed for a specific look. Jolt's `RagdollSettings::DisableParentChildCollisions` builds a `GroupFilterTable` that does exactly this
  (`DisableCollision(joint, parent joint)`), and PhysX's docs recommend filtering CCD between limbs of one ragdoll.
- Mass distribution: a torso bone with its full-body mass and a hand bone with
  a tiny fraction is correct human proportion but is also the exact large
  mass-ratio case flagged in the constraint-solver skill as explosion-prone —
  cap the mass ratio between any two directly jointed ragdoll bones even if it
  slightly misrepresents real anatomy, trading accuracy for stability (in a 1D solver test with 10 iterations the residual error
  grew from 0.0003 m/s at 1:10 to 0.096 at 1:100 and 3.5 at 1:1000).

## Verify
- [ ] Ragdoll activation inherits velocity from the preceding animation frames;
      a character ragdolled mid-sprint visibly carries momentum, not an instant
      stop.
- [ ] Ragdoll-to-animation blend uses a short pose-interpolation window, not an
      instant snap to the get-up animation's first frame.
- [ ] Ragdoll bone hierarchy matches the animation skeleton exactly; verified by
      triggering ragdoll on every major hit-reaction animation, not just one.
- [ ] Adjacent ragdoll bones don't self-collide and explode on activation; mass
      ratios between directly jointed bones are capped.

## Checked (2026-10-22)
- Computed in numpy: bone linear velocity from two frames ((x1 - x0) / dt = 8 m/s for an 8 m/s bone) and angular velocity from the quaternion delta (2.9997 rad/s for 3 rad/s at 60 Hz, a small-angle approximation), supporting the 'inherit velocity from the last 1-2 frames' step.
- Jolt master `Ragdoll.h` (`DisableCollision` in the group filter table created for the ragdoll, `SetPose`, `GetPose`, `DriveToPoseUsingKinematics`); Jolt README lists animated ragdolls. PhysX 5.4.1 AdvancedCollisionDetection page: filter CCD between ragdoll limbs. Mass-ratio figures from my 1D stack solver (see constraint-solvers-and-joints).
- Removed the Unreal 'Blend Physics' and Unity `Animator` write-back claims (not checkable here). The claim that powered ragdolls are what shipped combat games use is an industry practice statement I could not source, hence the gated marker and status; the get-up blending procedure itself is design guidance.
