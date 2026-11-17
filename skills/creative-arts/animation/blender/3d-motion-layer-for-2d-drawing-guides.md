---
id: creative-arts.animation.blender.3d-motion-layer-for-2d-drawing-guides
name: 3d-motion-layer-for-2d-drawing-guides
category: creative-arts
field: animation
product: blender
tags: [blender, 3d-layout, motion-guide, 2d-animation, nla, ik, rigid-body, holdout, freestyle, contact, interaction, mocap, universal-animation-library, python]
level: advanced
status: draft
description: "Build a scene's motion in Blender as a guide for 2D drawings: library clips on NLA, IK contact on shared props, rigid-body falls, holdout occlusion, per-frame prop logs."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# 3D motion layer for 2D drawing guides

**Goal:** give a 2D show correct walking, weight, contact and occlusion by blocking each scene in 3D with
simple rigged bodies, then drawing over it frame by frame. The 3D bodies don't need to look like the
characters. They need to move like them and touch things correctly. Studios use 3D layout under 2D this way.

## Bodies and clips

- Use one shared skeleton for the whole cast, so every library clip fits every character. With Quaternius
  base characters on the 65-bone universal rig, Universal Animation Library clips matched all 65 bones.
- Clips useful for everyday scenes: `Walk_Carry_Loop`, `Walk_Loop`, `Crouch_Idle_Loop`, `PickUp_Table`,
  `Fixing_Kneeling`, `Interact`, `Idle_FoldArms_Loop`. Import the GLB, keep the actions and delete the
  imported objects.
- Sequence with NLA strips: a one-frame "hold" strip (`action_frame_start == end`, extrapolation HOLD) for
  standing still, then the next clip with `blend_in` of 12 to 14 frames for a natural transition.
- Travel by keying the armature object's location linearly over an in-place walk cycle, at about
  1.1 to 1.2 m/s.

**Gotcha:** these rigs store rotation as a quaternion. Setting `rotation_euler` does nothing until
`rotation_mode = "XYZ"`. The symptom is a character walking toward the camera instead of across frame.
Measure the clip's forward axis (hands relative to spine at a carry pose) rather than guessing.

## Contact on shared objects

- Place an empty on each grip point of the prop. Add an IK constraint on the forearm, targeting it, with the
  influence keyed from 0 to 1 over the reach.
- **Use the camera-side hand.** A character facing −X has its left hand toward a camera on −Y.
- **Include the spine in the chain** (chain 5: forearm, upper arm, clavicle and two spine bones). With chain
  2 on a crouch clip, the arm was 0.54 m but the shoulder sat 0.86 m from a can on the floor, so the hand
  stopped 30 to 44 cm short. With the spine included, the back leans in and contact came within 1 to 8 cm.
- Space two crouching characters about 1 m apart, so leaning heads don't collide.
- Measure contact every frame (hand bone tail to target) and log it.

## Falling and rolling objects

- Rigid bodies work for falls out of a container. Parent items to the bag and key them kinematic, then
  switch them dynamic at the tear, staggered by a few frames. They inherit motion, fall, bounce and settle.
- For a scripted path ("one perfect bounce, then into the drain"), key it as ballistic hops and an eased roll
  instead of fighting the simulator. A rolling sphere wouldn't respect the curb collision. Rotate it by
  distance travelled divided by radius so the spin matches.

## Occlusion: things that go behind other things

- Build the occluders as real geometry (grate bars with gaps wider than the object, the pit beneath) and
  render the moving object with the set marked `is_holdout`. The bars then hide it correctly as it drops.
- **Freestyle lines ignore holdouts:** the object's outline kept drawing after it had gone under the road.
  Key `hide_render` once it's fully hidden.
- A keyed `hide_render` overrides a manual hide. Remove the action temporarily when rendering a clean layout
  plate.
- Render the empty set once as `layout.png`. It becomes the base for the painted background, so the painting
  and the motion line up exactly.

## Output for the drawing pass

- Toon render (2-tone shading and Freestyle line) with `film_transparent`, on twos, one camera per beat.
- Per frame, a JSON log of each prop's screen box, its kind (prop, container or hand) and its holder. The
  object continuity checks and the reviewer use it.
- Crop all frames of a shot with one box, never per frame.

See `comfyui.on-model-drawing-from-3d-guides` for drawing over these frames and
`methods.anime-shot-acceptance-and-motion-qa` for checking the result.
