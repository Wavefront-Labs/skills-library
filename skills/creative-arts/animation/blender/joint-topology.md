---
id: creative-arts.animation.blender.joint-topology
name: joint-topology
category: creative-arts
field: animation
product: blender
tags: [blender, joint-topology, joint-loops, shoulder-topology, character-modeling, deformation, edge-flow]
level: advanced
status: docs-checked
description: "Model joint topology that bends well: three-loop elbows and knees, wedge loops for volume, shoulder and hip flow, wrists and testing with an armature."
sources:
  - https://docs.blender.org/manual/en/latest/animation/armatures/skinning/parenting.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/structure.html
  - https://docs.blender.org/manual/en/latest/editors/3dview/display/overlays.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# joint-topology

Goal: elbows, knees and shoulders that bend without collapsing or candy-wrapper twisting.

## Elbows and knees

- **Three loops** at the joint: one at the pivot, one above, one below. Spacing slightly tighter on the inside (bend side) than the outside.
- Extra **wedge loops** on the outer side (elbow tip, kneecap) add volume when bent; on the inner side, a loop that collapses into a crease reads as skin folding.
- Loops perpendicular to the limb, evenly spaced on the rest of the limb.

## Shoulders and hips

- Shoulder: loops flow from the chest over the deltoid into the arm; the armpit needs enough loops to stretch when the arm lifts. Model in an A-pose (arms angled down) so the shoulder is mid-range.
- Hip: loops from the groin around the buttock into the thigh; an extra diagonal loop at the front helps leg raises.

## Wrist and neck

Twisting joints need even loops along the length (twist distributes across them with twist bones); avoid poles on the forearm.

## Test

1. Quick armature (`Shift A → Armature`), parent with *Automatic Weights* (`Ctrl P`).
2. Pose strong bends, arm raise, leg raise. Watch for: volume loss, inner-surface intersections, stretched faces.
3. Fix with loop placement first; correctives (shape keys driven by rotation) only after topology is right.

## Gotchas

- A pole on the bend line creates a pinch; move it away along the limb.
- T-pose shoulders look fine at rest but collapse when arms go down.

## Verify

A strongly bent test pose shows maintained thickness at the elbow tip, a clean crease on the inside and no flipped faces (no red in the Face Orientation overlay).

## Checked

2026-10-27, Blender manual 5.2 (blender-v5.2-release RST). Confirmed: parenting an object to an armature With Automatic Weights (Ctrl P) assigns bone-heat weights; Face Orientation overlay shows back faces in red. Corrected: the overlay check no longer refers to blue. Removed: loop counts, angles and the dense-joint weight claim. The loop-flow guidance is modelling practice from experience and is not stated in the manual; the numeric counts, ratios and angles that no documentation covers were removed.

Method: documentation only; no commands were run.
