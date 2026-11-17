---
id: creative-arts.animation.blender.mocap-retarget
name: mocap-retarget
category: creative-arts
field: animation
product: blender
tags: [blender, mocap, retarget, armature, rig, animation, motion-capture]
level: advanced
status: verified
description: "Retarget mocap/library motion onto a stylized Blender rig: bone mapping, constraint-based remap, bake, cleanup, and when a cartoon show should NOT use it."
sources: []
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# SKILL: Motion capture → stylized rig retarget (Blender)

**Why:** hand-keying every second of a long episode solo is infeasible; library and
captured motion gives full-body performance to **retarget** onto a stylised rig, then
polish. But retargeting human-realistic motion onto a cartoon body is a craft with sharp
edges — and for a snappy toon show it is often the **wrong** tool (see §6).

## 1. Sources of motion (open/free)

- **Rokoko** free motion library + the free Rokoko Blender add-on (records/cleans, exports
  FBX/BVH, retargets in Blender).
- **Mixamo** (frozen but works): auto-rig + a large clip library — fastest source of
  walks/gestures/idles/reactions.
- **Markerless video→mocap** for bespoke performance with no suit.
- A vendored capture stack (Kinect/LiveScan-class) for custom capture later.

## 2. Prep both skeletons before you map anything

Retargeting fails most often because the two rigs disagree about rest pose, scale, or
axis — not because the mapping is wrong.

1. **Rest pose must match.** Put the target rig in the **same rest pose as the source**
   (both A-pose, or both T-pose). A T-pose source onto an A-pose target offsets every
   shoulder/arm by the A/T delta. If you can't rebuild the rest pose, bake a **rest-offset
   correction** per bone (the difference between source and target rest orientation) and
   apply it in the constraint — this is what Auto-Rig-Pro/Rokoko call "auto-scale / fix
   rest".
2. **Scale & root.** Match world scale and floor height, or feet will float/sink. Align
   the up/forward axes (FBX often imports Y-up into Blender's Z-up — apply the import
   rotation, don't fight it downstream).
3. **Clean the source first.** Trim to the usable range, kill foot jitter and gimbal
   spikes on the *source* clip before retargeting; garbage in multiplies downstream.

## 3. Bone mapping — the core table

Build an explicit **source-bone → target-deform-bone** map for the core chain and reuse
it:

| Source (mocap)        | Target (stylised deform) |
|-----------------------|--------------------------|
| Hips / Pelvis         | pelvis / root            |
| Spine, Spine1, Spine2 | spine, chest             |
| Neck, Head            | neck, head               |
| L/R UpperArm, Forearm, Hand | shoulder→upper_arm→forearm→hand |
| L/R Thigh, Shin, Foot, Toe  | thigh→shin→foot→toe      |

- Map the **deform/FK chain**, not IK controls — then bake into the control rig after.
- **Fingers:** map only if the source actually has clean finger data (most body mocap does
  not). Otherwise leave fingers off the map and pose hands by hand.
- **Save the map as a preset** keyed to your rig's standard bone names so every character
  retargets identically. One map, reused, is the consistency and speed win.

## 4. Doing the remap manually with constraints (no add-on needed)

Rokoko/Auto-Rig-Pro automate this, but the mechanism is just constraints — know it so you
can fix it when the add-on misbehaves:

1. Import the mocap armature (it carries its own skeleton + animation).
2. On each target deform bone add a **Copy Rotation** constraint targeting the mapped
   source bone (space: usually `Local` or `Pose`→`Pose`), plus **Copy Location** on the
   root/pelvis only (hips drive translation; limbs inherit via FK).
3. Add the **rest-offset correction** per bone (a parented empty or a correction rotation)
   so the target holds its own rest shape while following the source's *motion*.
4. Scrub: the stylised rig now mimes the capture live, constraint-driven.

## 5. Bake, then the non-negotiable polish pass

1. **Bake** the constrained motion to keyframes on the target (`Pose → Animation → Bake
   Action`, visual keying, clear constraints). Bake IK on the control rig so animators can
   edit it.
2. **Fix foot sliding / contacts:** lock feet to the ground on plant frames (IK foot lock
   or hand-key the plants); realistic capture drifts, cartoon feet must stick.
3. **Hands & face:** retarget rarely nails fingers; **face comes from audio** (lip-sync,
   see `lip-sync.md`) + hand-keyed expression, never from body mocap. Keep them separate.
4. **Check through the cel shader.** Flat toon shading exposes deformation errors (band
   creasing, candy-wrapper elbows) that a textured preview hides. Clean weights where the
   retargeted range creases.
5. **Stylise the motion:** captured motion is human-natural and *floaty* for toon. Pull
   poses toward stronger silhouettes, add snap (ease into holds), exaggerate key extremes,
   and consider **stepping to 2s** on secondary action so it reads as animation, not
   rotoscope. Retarget gives you the draft; the cartoon lives in this pass.

## 5b. Frame-rate & root-motion conform

- **Conform to 24fps.** Mocap is often captured at 30/60/120fps. Retarget at the source
  rate, then **bake to 24fps whole frames** (set the scene to 24 before the bake, bake
  "visual keying" on every frame). Resampling after keys exist introduces sub-frame
  slides; bake onto the grid once. This matches the lip-sync/camera pipeline, which keys
  on whole 24fps frames.
- **In-place vs travelling.** Decide whether the clip should carry world translation
  (a character actually walks across the set) or play **in place** (locomotion driven by
  the shot's staging). For in-place, zero the hips' XY translation channels after bake and
  let the staging move the root — this lets one walk clip serve many shots without the
  character wandering off its mark.
- **Looping clips** (idle, walk cycle): match first and last pose, bake, then offset the
  end key to equal the start and set the cycle; a visible pop at the loop seam means the
  capture range wasn't a whole cycle.

## 6. When NOT to use mocap on a cartoon show

Mocap is a trap for a snappy, pose-to-pose toon style:

- **Hero acting beats** want hand-keyed pose-to-pose timing — crisp holds, snappy
  transitions, squash/stretch. Realistic mocap's continuous motion fights that; you spend
  more time de-naturalising it than you'd spend keying from scratch.
- **Stylised/non-human proportions** (big head, stub limbs, 4 fingers) retarget badly —
  the human skeleton's joint ratios don't map, elbows/knees land wrong.
- **Short gestures and holds** are faster to key directly than to source, clean, retarget
  and re-stylise.
- **Keep mocap for:** background/crowd cast on library clips, long mundane full-body
  actions (walking a street, sitting, idling), and realistic physical weight you don't
  want to hand-animate. Build a **library of retargeted base clips** (idle/walk/turn/sit/
  gesture/react) per character and compose shots from them + polish — don't recapture.

## Rule

Mocap = the draft performance; the stylise + hand-polish pass is non-negotiable for hero
shots. Background cast may run on clean library clips alone. If re-stylising the capture
costs more than keying the beat, key the beat.

Sources: Rokoko Blender retargeting guide; Mixamo workflow; general constraint-based
retargeting practice.

See also: `lip-sync.md`, `../principles/acting-performance.md`, `rigging.md`,
`cel-shading.md`.

## Verified: dropping a library clip onto a matching rig (and the silent failure)
When the source library and the target character share a skeleton (same bone names and
count — common for "universal" CC0 character/animation sets), retargeting is just
**assigning the action**; no constraint-remap pass is needed. Import the character, import
the animation library, assign the action to the character's armature, then delete the
library's own rig/meshes — the actions persist in the file.

**THE GOTCHA (Blender 4.4+ slotted actions):** assigning `armature.animation_data.action`
alone animates **nothing**. Actions now carry *slots*, and until a slot is bound the rig
sits in rest pose with no error, no warning — every bone reads its rest transform and a
render looks like a T-pose. Diagnosis is confusing because the action is clearly present,
its frame range is right, all 65 bones are keyed and every name matches. Always bind:

```python
rig.animation_data_create()
rig.animation_data.action = act
if hasattr(rig.animation_data, "action_slot") and getattr(act, "slots", None):
    rig.animation_data.action_slot = next(
        (s for s in act.slots if s.target_id_type == 'OBJECT'), act.slots[0])
```

**Verify it actually drives:** don't trust the render — sample a pose bone's
`rotation_quaternion` (or world matrix) at two frames and assert it changed. An unbound
slot returns the identity quaternion at every frame. Proven by applying a walk cycle from
a 120-clip CC0 library onto a separately-sourced 65-bone character: identical bone names,
zero mismatches, and still no motion until the slot was bound — after which the cycle
played correctly (contact / passing / opposite contact, with arm swing and hip rotation).

