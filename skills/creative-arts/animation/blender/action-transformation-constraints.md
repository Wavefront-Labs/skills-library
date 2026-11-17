---
id: creative-arts.animation.blender.action-transformation-constraints
name: action-transformation-constraints
category: creative-arts
field: animation
product: blender
tags: [blender, constraints, action-constraint, transformation-constraint, transform-mapping, pose-driven, foot-roll, rigging]
level: practitioner
status: docs-checked
description: "Map one transform to another in Blender rigs: the Transformation constraint (Map From/To ranges, mix, extrapolate) and the Action constraint (pose from a control channel)."
sources:
  - https://docs.blender.org/manual/en/5.2/animation/constraints/transform/transformation.html
  - https://docs.blender.org/manual/en/5.2/animation/constraints/relationship/action.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# action-transformation-constraints

## Transformation constraint

- **Map From**: Location, Rotation or Scale of the Target, with X/Y/Z Min and Max per axis (and a Mode for rotation). The input is clamped to this range, then offset and scaled to the Map To range.
- **Map To**: Location, Rotation or Scale of the owner. Each output axis picks an **X/Y/Z Source Axis** (the same input axis may be chosen more than once) and has its own Min and Max.
- **Extrapolate**: off clamps input and output to the Min/Max values; on lets them go beyond. **Mix** (Replace, Multiply for scale, Add for location and rotation, Before/After Original for rotation) defaults to Add for location and rotation and Replace for scale.
- Uses: a slider driving a rotation (manual example: a rail's Y location from -3 m to 3 m drives a gear's X rotation from 0 to 180 degrees), or an eyelid following eye rotation at a fraction of the range.
- Limits from the manual: if a Min is higher than its Max, both are treated as the Max, so reversed mappings are not possible. Target rotations are wrapped into -180..180 degrees and target scales are read as absolute values, so it is not suited to driving something from a gear's full rotation.

## Action constraint

- Owner bones or objects take their transform from an **Action**, evaluated at a frame derived from a target channel: Target, **Channel** (for example Y Location) with its space, **Range Min/Max** mapped to **Frame Start/End** in the Action. Frame End may be lower than Frame Start to play the action in reverse; Range Max may be lower than Range Min. Choose the **Slot** inside the Action.
- **Evaluation Time** sets the Action frame from a number instead of a Target (0 is Frame Start, 1 is Frame End); it can be fixed, keyframed or driven, including by custom properties.
- **Mix**: Replace, Before Original (Full / Aligned / Split Channels) or After Original (Full / Aligned / Split Channels). Aligned avoids shearing under non-uniform scale; Split Channels computes location, rotation and scale separately. The manual warns that modes other than After Original (Full or Aligned) may misbehave on objects without a parent.
- **Object Action** (bone constraint only) uses the Action's object keyframes instead of the bone-named ones.
- Target rotations are wrapped into -180..180 degrees and negative scales are treated as positive.
- Uses: facial controls (a control channel drives a multi-bone pose action), hand curl sliders, corrective poses. For a very simple Action, Copy Transforms may be enough; Drivers cover more complex relationships.

## Workflow (Action constraint)

1. Create action `HandCurl`, key frame 0 = open, frame 10 = closed on finger bones; give it a fake user and unassign it from the armature.
2. On each finger bone: Action constraint, Action = HandCurl (and its Slot), Target = `hand_ctrl`, a Channel such as Y Scale, Range Min/Max 0..1 mapped to Frame Start/End 0..10.
3. Copy the constraint to the other finger bones with Copy to Selected in the constraint header Extras menu.

## Gotchas

- Rotation input beyond 180 degrees wraps, so keep the control within -180..180.
- Pick the Channel space deliberately (World, Local and so on) so it does not change when parents move.
- To copy constraints to other bones or objects use the constraint header's Extras menu, Copy to Selected.

## Verify

Move the control through its range: owner bones reach the mapped pose exactly at min/max; extrapolation behaves as configured.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release). Confirmed on the Transformation and Action constraint pages: Map From/Map To fields, Extrapolate, Mix modes, Min greater than Max rule, rotation wrapping, Action Range Min/Max and Frame Start/End, Evaluation Time, Slot, Object Action, Mix modes. Corrected the reversed-range foot roll and gear-ratio examples, the Mix list, and removed the unconfirmed action-assignment gotcha and Ctrl L shortcut.

Method: documentation only; no commands were run.
