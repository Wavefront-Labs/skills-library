---
id: creative-arts.animation.blender.relative-absolute-shape-keys
name: relative-absolute-shape-keys
category: creative-arts
field: animation
product: blender
tags: [blender, shape-keys, relative-shape-keys, shape-key-basis, relative-to, absolute-shape-keys, shape-key-evaluation-time, morph-sequence]
level: practitioner
status: verified
description: "Set up Blender shape keys: Basis, Relative To (stacked shapes), and Absolute keys driven by Evaluation Time for morph sequences like blooming or melting."
sources:
  - https://docs.blender.org/manual/en/5.2/animation/shape_keys/introduction.html
  - https://docs.blender.org/manual/en/5.2/animation/shape_keys/shape_keys_panel.html
  - https://docs.blender.org/manual/en/5.2/animation/shape_keys/workflow.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# relative-absolute-shape-keys

Goal: choose between independent sliders (Relative) and a single timeline of shapes (Absolute).

## Relative

- The stack is a list of keys; the **Basis** is the first (top-most) key, holds the original vertex positions, has no weight value, cannot be keyed and is the default Reference Key for new keys.
- **Value**: blend between the key and its reference key (0.0 = reference, 1.0 = the shape); **Range** (`slider_min` 0 and `slider_max` 1 by default) clamps it, so widen the Range to extrapolate below 0 or above 1 (run: Value 2 with slider_max 3 moved a vertex twice as far as Value 1, and Value -1 with slider_min 0 clamped to 0).
- **Relative To**: the Reference Key a shape deforms from (usually Basis). Setting it to another key (for example `smile_wide` relative to `smile`) makes the deformation only the extra. Internally keys are stored as snapshots, so replacing the Reference Key subtracts the difference between the new and old reference from that key's deformation.
- The panel's **+** button always adds a copy of Basis. **Shape Key Specials > New Combined** (called New Shape from Mix on the workflow page) adds a key from the currently visible mix.
- **Clear Shape Keys** (X) sets all values to zero. **Shape Key Lock** (pin icon) shows the active key without blending and is switched on automatically in Edit Mode; **Shape Key Edit Mode** shows the current blend instead of the full active key when you enter Edit Mode.

## Absolute

- Untick **Relative**. Each key's Value is the **Evaluation Time** (in frames) at which it is fully active; keys are timed by list order at a constant interval, and the result interpolates between the previous and next key (run: Basis, k1, k2 get `frame` 0, 10, 20; Evaluation Time 10 gives k1, 15 lands halfway between k1 and k2, and 25 stays at k2). API: `Key.use_relative`, `Key.eval_time`, `ShapeKey.frame`.
- Animate **Evaluation Time** with keyframes or a driver to morph through the sequence (flower blooming, melting).
- **Interpolation** per key (`KEY_LINEAR` by default, `KEY_CARDINAL`, `KEY_CATMULL_ROM`, `KEY_BSPLINE`): Linear, Cardinal, Catmull-Rom or B-Spline.
- **Re-Time Shape Keys** (clock icon, "Reset Timing" in the workflow steps) resets the timing after keys were removed or reordered.

## Choosing

Faces, correctives and blinks suit Relative; a progressive morph of a prop suits Absolute.

## Gotchas

- Shape keys cannot add or remove vertices; finish topology before creating keys. Vertices added later are recorded at their creation position in every key.
- The Mute checkbox excludes a key from the mix. Lock Shape protects a key from edits (most tools abort on a locked key).
- Make Basis and Apply to Basis (Specials menu) change the base shape and recompute the other keys relative to it.

## Verify

Relative: each Value from 0 to 1 moves only the intended region. Absolute: scrubbing Evaluation Time passes through each shape in order.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release source), Shape Keys introduction, panel and workflow pages: Basis behaviour, Value/Range/Relative To, specials names, Lock/Edit Mode toggles, Absolute workflow, Re-Time, interpolation types. Removed as unconfirmed: the "modifiers cannot be applied while keys exist" remark. Corrected: specials menu item names (New Combined) and that Basis cannot be keyed.
Run check, 2026-11-01, Blender 4.5.14 LTS headless (bpy, factory settings): Basis as default relative_key; k1 value 1 moved a vertex by 1; k2 relative to k1 with both at 1 added only the difference (x 4 against 2 for k1 alone); k2 at 0.5 relative to Basis gave 2.5; absolute timing and interpolation as quoted; slider range clamping; ShapeKey properties (name, frame, value, interpolation, vertex_group, relative_key, mute, lock_shape, slider_min, slider_max); operators shape_key_add, shape_key_clear, shape_key_retime, shape_key_move, shape_key_mirror, shape_key_transfer, shape_key_lock exist. Not run (confirmed from the manual only): menu names (New Combined, Make Basis, Apply to Basis), the Lock and Edit Mode toggles, and topology limits.

Method: manual text and shipped UI scripts confirmed from documentation; the listed behaviour run headless in Blender 4.5.14.
