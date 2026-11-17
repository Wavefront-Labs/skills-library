---
id: creative-arts.animation.blender.mocap-layering
name: mocap-layering
category: creative-arts
field: animation
product: blender
tags: [blender, motion-capture, mocap-layering, mocap-override, nla, additive-layer, combine-blending]
level: practitioner
status: docs-checked
description: "Hand-key fixes and exaggeration over mocap in Blender without touching the base: NLA push-down, Combine-blended override layers, layered recording, and baking the result for export."
sources:
  - https://docs.blender.org/manual/en/latest/editors/nla/index.html
  - https://docs.blender.org/manual/en/latest/editors/nla/sidebar.html
  - https://docs.blender.org/manual/en/latest/editors/nla/tracks.html
  - https://docs.blender.org/api/current/bpy.ops.nla.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# mocap-layering

Goal: keep dense mocap intact and put animator tweaks on a separate, sparse layer.

## Setup

1. Retargeted mocap action on the rig (see `bone-mapping-retarget`). **Push Down Action** in the NLA creates a track below the Action Track with the action as a strip and leaves the Action Track empty; it is the base strip (Replace blending).
2. New action for the layer: in the NLA, the active action slot now empty; key adjustments directly — the active action is evaluated on top of the NLA stack.
3. Set the active action's blending to **Combine**: in the NLA, select the Action Track, then Sidebar > **Edited Action** > **Blending** — values then combine with the tracks below instead of replacing them.
4. Keys at 0 offset where the fix should fade out; peaks where the correction is needed (e.g. raise arm 10° at frame 120-140).
5. Push Down the layer when done; it becomes another strip (Combine). More layers stack above.

## Overrides (replace)

To fully replace a section (bad hand capture): a layer strip with Replace and blend in/out frames, keyed only on the hand bones.

## Bake

Select controls, Bake Action (Visual Keying, "Overwrite current action" off) to combine everything into one action for export, or rely on FBX NLA/All Actions settings (see `fbx-animation-export`).

## Gotchas

- Combine picks the method per property: Quaternion rotation uses quaternion multiplication (and always drives all four channels, so Insert Single Keyframe inserts all four keys), Axis/Angle adds, Scale is proportional (value / default), and other properties add the offset from the default. Add, Subtract and Multiply are plain per-value operations, so prefer Combine for rotation and scale layers.
- Replace overwrites the values from lower tracks (blended by Influence when below 1), so a layer in Replace that has keys on bones you did not mean to touch (Whole Character keying) overrides the mocap there — key only the bones you need (Available or selected keying).
- Tweak Mode (Tab on a strip) on the base strip edits the dense mocap itself — avoid.

## Verify

Mute the layer track: original mocap returns unchanged; unmute: corrections visible only in the intended frames.

## Checked

2026-10-27. Documentation release: Blender manual 5.2 (branch blender-v5.2-release) and the bpy.ops.nla.bake reference. Confirmed: Push Down Action behaviour and Tweak Mode via Tab (editors/nla/tracks.rst); Sidebar > Edited Action panel (visible when the Action Track is selected) with Blending Replace, Multiply/Subtract/Add and Combine and the per-property Combine formulas, plus Blend In/Out (editors/nla/sidebar.rst); Bake Action options Visual Keying and Overwrite Current Action (API reference). Wrong in the old text: the panel is Edited Action (there is no Animation Data panel for this), and the Combine/Add description of euler and scale behaviour did not match the documented formulas. The 10 degree and frame 120-140 example is illustrative.

Method: documentation only; no commands were run.
