---
id: creative-arts.animation.blender.bone-edit-symmetrize
name: bone-edit-symmetrize
category: creative-arts
field: animation
product: blender
tags: [blender, rigging, bone-extrude, bone-subdivide, fill-between-joints, armature-symmetrize, bone-naming, left-right-naming, auto-name, x-axis-mirror]
level: practitioner
status: docs-checked
description: "Build skeletons fast in Blender armature Edit Mode: extrude (E, Shift-E mirrored), subdivide, fill between joints (F), L/R naming, Auto-Name, X-Axis Mirror and Symmetrize."
sources:
  - https://docs.blender.org/manual/en/5.2/animation/armatures/bones/editing/extrude.html
  - https://docs.blender.org/manual/en/5.2/animation/armatures/bones/editing/naming.html
  - https://docs.blender.org/manual/en/5.2/animation/armatures/bones/editing/symmetrize.html
  - https://docs.blender.org/manual/en/5.2/animation/armatures/bones/editing/subdivide.html
  - https://docs.blender.org/manual/en/5.2/animation/armatures/bones/editing/fill_between_joints.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# bone-edit-symmetrize

Goal: a clean, symmetric, correctly named skeleton in minutes.

## Creating bones (Armature Edit Mode)

- **E** extrudes a connected child from each selected tip (E R and E S rotate or scale while extruding). **Shift-E** is mirror extrude: with the X-Axis Mirror option enabled each extruded tip produces two bones named with _L and _R suffixes. Cancelling an extrude leaves zero-length bones that are removed on leaving Edit Mode; undo instead.
- **Ctrl-RMB** adds a bone when at least one bone is selected (root and parenting depend on the active element).
- **Subdivide** (Armature > Subdivide, Number of Cuts n gives n + 1 bones per selected bone) forms a connected chain, for spines, tails and tentacles.
- **Fill Between Joints** (F): with a root and a tip, or two tips or two roots selected, creates one bone between them; with one joint selected the bone runs to the 3D cursor. Two joints of the same bone, or more than two joints, give an error.
- **Separate Bones** (P) moves the selected bones to a new armature object.

## Naming

- Separators for left/right: none (handLeft/handRight), "_", ".", "-" or space, with L, R, left or right in either case; the short L/R code needs a separator ("handL" does not work). The marker may also come before the name. Blender strips number extensions such as .001 before mirroring or flipping.
- **Auto-Name** (Armature > Names): Left/Right adds .L to bones whose root has positive X and .R for negative X (the tip decides when the root is at X 0; a bone with both joints at X 0 gets only a period). Front/Back uses .Bk (positive Y) and .Fr (negative Y); Top/Bottom uses .Top and .Bot.
- **Flip Names** (Armature > Names): swaps left/right markers in selected bone names.
- Rename with the Name field in Bone Properties or by double-clicking in the Outliner.

## Symmetry

- **X-Axis Mirror** (an armature editing option) mirrors edits live and relies on the naming convention.
- **Symmetrize** (Armature > Symmetrize): mirrors the selected bones along X using the naming convention, left to right or right to left depending on the selection (if matching bones are selected on both sides it mirrors right to left). Opposite bones that do not exist are created and existing ones are overwritten; bones that cannot be identified as left or right are ignored. Bone and constraint properties are adjusted to mirror their behaviour; for Action constraints keyframes are added to the target Action; drivers are not created or affected. Bone collection assignments are symmetrized too, following the naming convention.

## Gotchas

- Centre bones (spine, head) cannot be identified as left or right and are ignored by Symmetrize; leave them without an L/R marker.
- Symmetrize overwrites existing opposite-side bones that have matching names.
- Mirror extrude only gives pairs when X-Axis Mirror is enabled.

## Verify

Symmetrize produces the opposite-side bones with mirrored names and properties; check a few pairs in Pose Mode.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release). Confirmed on the Extrude, Naming, Symmetrize, Subdivide and Fill Between Joints pages: E, Shift-E with X-Axis Mirror, Ctrl-RMB, Subdivide cuts, F fill rules, naming separators, Auto-Name suffixes, Flip Names, Symmetrize behaviour. Removed unconfirmed Join, snapping, world-origin and Paste Flipped claims, and the Shift-D Duplicate shortcut.

Method: documentation only; no commands were run.
