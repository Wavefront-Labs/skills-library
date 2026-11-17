---
id: creative-arts.animation.blender.shape-key-animation
name: shape-key-animation
category: creative-arts
field: animation
product: blender
tags: [blender, shape-keys, shape-key-animation, shape-key-keyframes, shape-key-editor, blinks, morph-animation]
level: practitioner
status: docs-checked
description: "Keyframe shape keys in Blender: keying values, the Shape Key Editor, how shape key animation shares the object's action via slots, and glTF export of shape key animation."
sources:
  - https://docs.blender.org/manual/en/5.2/animation/shape_keys/workflow.html
  - https://docs.blender.org/manual/en/5.2/editors/dope_sheet/modes/shape_key.html
  - https://docs.blender.org/manual/en/5.2/animation/actions.html
  - https://docs.blender.org/manual/en/5.2/addons/scene_gltf2.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# shape-key-animation

Goal: animate shape key values directly (when they are not driven by a rig).

## Keying

- In Object Data > Shape Keys, hover a key's Value and press **I** (or use the context menu Insert Keyframe). The Basis has no value and cannot be keyed.
- **Dope Sheet > Shape Key Editor** mode shows the shape keys of the active object; each row is a key and each marker a point where its value changes. Move or scale keys there; names, values and relative settings are in the Sidebar.
- Shape key data is "closely related" to its mesh and object, so keying it reuses the action already assigned to the object (when the data has a single user) and creates its own slot in that action. Meshes with several users get separate actions. See `action-slots`.
- Absolute shape keys are animated by keying **Evaluation Time** instead.

## Timing patterns

- Blink: fast close with Linear or Bezier ease, short hold, slower open (tune by eye).
- Morph: Bezier interpolation; offset the keys of different shapes by a frame or two for overlapping action.
- Widen the key's **Range** to push values past 0 to 1 for overshoot.

## Export

- glTF: shape key value animation is supported. Shape key animation controlled by drivers that use bone transformations is sampled only if the mesh object is a direct child of the armature. Animation of other properties (physics, lights, materials) is ignored.
- For FBX and Alembic behaviour check the manual page of the exporter you use; this skill does not state specifics.

## Gotchas

- Show Only Errors lists channels that animate a property that does not exist.

## Verify

The Shape Key Editor shows keys on the expected frames; the exported file plays the morphs in a viewer.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release source): Shape Key Editor description, Basis not keyable, action reuse and slots for shape key data, glTF shape key animation notes. Removed as unconfirmed: View > Show Sliders, slider-drag auto keying, frame-count blink timing, FBX bake settings, Alembic claim, "driver wins" claim. Corrected: shape key animation no longer lives in a separate action by default; it shares the object's action in its own slot.
Method: documentation only; no commands were run.
