---
id: creative-arts.animation.blender.creature-rigging
name: creature-rigging
category: creative-arts
field: animation
product: blender
tags: [blender, creature-rigging, quadruped, spline-ik, tentacle, chain, rigify, metarig, extra-limbs, stretchy-rig, non-biped, tail, digitigrade, glitch, censor, armature]
level: advanced
status: docs-checked
description: "Rig non-biped Blender characters: quadrupeds, spline-IK tentacles/chains, extra limbs, stretchy cartoon rigs, and the broken 'Warden' glitch entities for a cel show."
sources:
  - https://docs.blender.org/manual/en/latest/addons/rigify/rig_types/limbs.html
  - https://docs.blender.org/manual/en/latest/addons/rigify/rig_types/spines.html
  - https://docs.blender.org/manual/en/latest/animation/constraints/tracking/spline_ik.html
  - https://docs.blender.org/manual/en/latest/animation/constraints/tracking/stretch_to.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# SKILL: Creature & non-standard rigging (Blender)

**Goal:** rig the characters that aren't a biped — a production's quadruped animals,
the chain/tentacle appendages, extra-limbed oddities, and the glitched **"Warden"**
entities (deliberately broken geometry that stutters and tears) — into animator-friendly,
reusable library rigs. The biped workflow in `rigging.md` is the foundation; this skill
is the deviations from it. The deform principles (`advanced-deformation.md`) and UI
conventions (`rig-ui-controls.md`) carry over unchanged — rig once, reuse every shot.

## Start from a metarig, then break anatomy deliberately

Rigify's power for odd anatomy is its **modular rig types** — you don't hand-build from
zero. Build a custom metarig by placing Rigify **sample bone groups** and generating:

- `limbs.leg` / `limbs.paw` for digitigrade quadruped legs (`limbs.paw` needs a chain of
  four or five connected bones: thigh, shin, paw, optional digit, toe; `limbs.front_paw` and
  `limbs.rear_paw` are derivatives for front and rear paws).
- `spines.basic_spine` chained for long flexible spines, and `spines.basic_tail` for tails.
- `limbs.simple_tentacle` for tentacles, antennae, chains: a bendy, stretchy b-bone chain
  (at least two connected bones) with an optional Automation Axis that makes later control
  bones copy the local rotation of earlier ones.
- `basic.super_copy` for one-off control bones.

Generate, then the generated rig gives you IK/FK, stretch and switches for free.
**Reuse the metarig approach for odd anatomy:** a six-legged creature is just the leg
sample instanced six times with the parenting repointed; an extra arm is one more
`limbs.arm`. Build the metarig, generate, done — far faster and more maintainable than a
bespoke armature, and it inherits Rigify's UI (`rig-ui-controls.md`).

## Quadrupeds

- **Leg structure is digitigrade:** hip → thigh → shin → **ankle/hock → long foot
  (metatarsal) → toe**. The animal's visible "knee" bends *backward* because it's the
  ankle. Rigify's paw/leg samples place this correctly; if hand-building, the IK chain
  runs thigh→shin→foot with the pole vector controlling the hock direction.
- **Four legs = front pair + back pair**, each an IK leg with its own foot-roll control.
  Front legs often get a shoulder/scapula control bone (floating, not socketed) for the
  sliding-shoulder look of real quadrupeds.
- **The spine carries the motion.** A `spines` chain with **FK + a drivable curve** lets
  the back arch and dip through a gallop. Add a **tail** as a `simple_tentacle`.
- **Ground contact:** foot IK targets parented to a ground/root control so feet pin while
  the body moves over them. This is the quadruped version of the biped foot setup in
  `rigging.md`.
- **Weighting / deform:** same edge-loops-support-the-joint rule and twist bones as
  `advanced-deformation.md`, applied to a horizontal spine and four limbs.

## Spline IK for tentacles, tails, chains, tongues

The core non-biped tool. **Spline IK** makes a bone chain follow a Bézier/NURBS curve,
so the animator shapes a *curve* (few handles) instead of posing dozens of bones.

Concrete setup:
1. Build a straight **deform bone chain** down the appendage (`tent_01…tent_12`),
   connected.
2. Add a **curve** running along it with a handle roughly per 2–3 bones.
3. On the **last bone** of the chain, add a **Spline IK** constraint:
   - **Target:** the curve. **Chain Length:** the number of bones in the chain.
   - **Y Scale Mode:** `Bone Original` (keeps the bones' original length) or `Fit Curve`
     (stretches the bones to cover the entire curve); `None` resets bones to rest length.
   - **XZ Scale Mode:** `Volume Preservation` (works like Stretch To) so the tentacle
     thins as it stretches (`advanced-deformation.md` volume logic); `Inverse Scale` sets
     X and Z to the inverse of the Y scale. **Use Original Scale** applies these on top of
     Pose Mode scales, and **Use Curve Radius** uses the curve point radii as extra X/Z
     scaling.
   - **Even Divisions** on makes each bone cover the same distance along the curve
     regardless of rest length. **Chain Offset** keeps the chain at its starting location
     instead of moving to the curve.
4. **Drive the curve** with **hook modifiers**: add empties/control bones as hooks on the
   curve's control points so the animator poses control bones, the hooks move the curve,
   Spline IK follows. Parent those controls into a tidy control collection.
5. **Twist:** practice is to expose a twist control (for example the curve point tilt, or
   the end control bone's roll) for a corkscrewing tentacle; check the result in the
   viewport.

A tongue, a whip, an elephant trunk, a snake, a vine — all the same rig. For a *short*
secondary chain that just needs drag (a small tail), the jiggle-bone approach from
`hair-simulation.md` is cheaper than full spline IK.

**FK/IK hybrid on a tentacle.** Pure spline IK is great for shaping a held pose but
awkward for arcing overlap. Rigify's `limbs.simple_tentacle` is an FK-style b-bone chain
with tweak controls and an optional Copy Rotation automation — animators pose the broad
curl in FK and let the tip overlap follow. Expose an **FK/IK or stretch slider** on it (`rig-ui-controls.md`) so
a single appendage can switch between "precisely placed" (IK/curve) and "loose and
whippy" (FK + jiggle) per shot. Set the **bone roll** consistently down the chain before
generating, or the FK twist will corkscrew unpredictably.

## Extra limbs & asymmetric anatomy

- **Each extra limb is an independent IK/FK unit** (another Rigify `limbs.arm`/`leg`),
  parented to the appropriate spine/torso bone. Give each its own IK switch and pole so
  the animator controls them independently.
- **Asymmetric creatures break the X-mirror assumption** — you can't mirror weights or
  drivers for a one-of-a-kind limb. Rig and weight each unique limb by hand; name
  clearly (`armL_upper`, `armL2_upper`, `tentacleBack_01`) so there's no ambiguity.
- Keep a **consistent naming + collection scheme** even for weird anatomy so
  `rig-ui-controls.md` can build a picker and selection sets on top.

## Stretchy / rubber-hose cartoon rigs

For full squash-and-stretch cartoon bodies:

- **Stretch-To** constraints on deform bones (`Maintain Volume` = `XZ`) give
  rubber-hose limbs that fatten/thin with length.
- **IK with Stretch** (enable **Stretch** on the IK constraint; it only affects bones whose
  `IK Stretch` value is greater than 0) so pulling the IK target past full extension *stretches* the limb
  instead of locking — the core cartoon-limb behaviour.
- **B-Bones** down the limb/spine for curving rubber-hose arcs and bulgy squash
  (`advanced-deformation.md`).
- Clamp with **Limit Scale** so a wild pull can't stretch to infinity and tear the mesh.

## The "Warden" glitch entities

The Warden creatures are *meant* to look broken — tearing geometry, stutter, popping
limbs. Rig them so the brokenness is **art-directable and repeatable**, not an accident:

- **Base deform rig underneath** (a chain or simple_tentacle metarig) so the entity still
  moves with intent; the glitch is a *layer on top*, not the absence of a rig.
- **Glitch displacement layer:** drive mesh distortion with **geometry nodes / a
  Displace modifier fed by noise**, with the noise's offset/strength exposed as a rig
  **custom property** (`rig-ui-controls.md`) so animators dial the glitch amount per
  shot and keyframe stutters. Driving Displace strength off a stepped/`noise` f-curve
  gives the stutter; keyframe it on 2s or 3s for the deliberate "broken frame-rate" feel.
- **Separation / tearing:** rig limbs/segments to **detach** — give a segment a control
  bone with a drivable **translation offset** and a visibility/scale control so the
  animator can pop a piece off and snap it back. Use **Limit** constraints as the cage so
  the tear reads as intentional corruption, not random explosion.
- **Keep it reusable:** all glitch controls as named custom properties + control bones in
  their own collection, documented, so the same Warden asset glitches consistently across
  every shot (and can be driven by the automated pipeline).

## Cross-links

- Biped foundation (armature, IK/FK, weights, naming) this builds on: `rigging.md`.
- Clean deformation, twist bones, volume preservation on odd anatomy:
  `advanced-deformation.md`.
- Bone shapes, collections, picker, custom properties for these rigs:
  `rig-ui-controls.md`.
- Cheap jiggle-chain alternative for small secondary appendages: `hair-simulation.md`.
- Face controls if the creature has one: `facial-rig.md`.

## Verify

Stress test each rig type on its locked asset:

1. **Quadruped gait.** Block a 4-frame gallop. **Pass:** digitigrade legs bend the right
   way (ankle back), feet pin to ground while the body translates over them, spine arches
   through the stride, tail drags. No knee flipping, no foot sliding.
2. **Spline-IK range.** Curl the tentacle into a full loop and a corkscrew via the curve
   controls. **Pass:** chain follows smoothly with no bone popping, Even Divisions keeps
   spacing uniform, Volume Preserve thins the stretched sections, twist reads clean. Fail
   → check Chain Length and XZ Scale Mode.
3. **Extra-limb independence.** Pose two same-side limbs into opposing actions. **Pass:**
   each IK/pole controls its own limb with no cross-talk; naming unambiguous.
4. **Stretch limit.** Pull a stretchy IK target far past full extension. **Pass:** limb
   stretches with volume loss and clamps before the mesh tears (Limit Scale cage holds).
5. **Warden glitch control.** Dial the glitch custom property 0→1 and keyframe a stutter
   on 3s. **Pass:** distortion/tearing scales smoothly with the property, the base motion
   stays readable underneath, and the same dialled value reproduces the identical glitch
   in a fresh shot (proves it's art-directed and reusable, not random).

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release RST).
Confirmed: Rigify rig types limbs.leg, limbs.paw (four or five bones), limbs.front_paw/rear_paw, spines.basic_spine, spines.basic_tail, limbs.simple_tentacle, basic.super_copy; Spline IK Chain Length, Even Divisions, Chain Offset, Use Curve Radius, Y Scale Mode (None/Fit Curve/Bone Original), XZ Scale Mode (None/Bone Original/Inverse Scale/Volume Preservation), Use Original Scale; Stretch To Maintain Volume; IK Stretch needs bone IK Stretch > 0. Fixed: simple_tentacle is a b-bone chain, not a spline/IK type; "Volume Preserve" is Volume Preservation; Y Scale Mode has no "Inverse Scale". Removed: the 12-bone example, the Spline IK twist-source claim and the "Volume XZ" label (no doc coverage).
Method: documentation only; no commands were run.
