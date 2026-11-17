---
id: creative-arts.animation.scripting.ae-loopout-cycles
name: ae-loopout-cycles
category: creative-arts
field: animation
product: scripting
tags: [loopout, ae-expressions, expressions, after-effects, loopin, cycle, pingpong, offset, continue, walk-cycle, looping-animation]
level: practitioner
status: docs-checked
description: "Loop keyframed animation with loopOut/loopIn in After Effects: cycle, pingpong, offset and continue types, partial loops by keyframe count or duration."
sources:
  - https://raw.githubusercontent.com/docsforadobe/after-effects-expression-reference/master/docs/objects/property.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# loopOut and loopIn

**Goal:** animate one cycle (a spin, a bob, a blink, a float) and repeat it without copying keyframes.

## Methods

- `loopOut([type="cycle"][, numKeyframes=0])`: loops a segment measured backward from the last keyframe; the loop plays until the layer Out point.
- `loopIn([type="cycle"][, numKeyframes=0])`: loops a segment measured forward from the first keyframe; plays from the layer In point.
- `loopOutDuration([type][, duration=0])` and `loopInDuration(...)`: same but the segment length is given in composition seconds. With 0, the segment starts at the layer In point (Out version) or ends at the Out point (In version).
- `numKeyframes` 0 (or unspecified) loops all keyframes. `loopIn("cycle", 3)` loops the segment bounded by the first and fourth keyframes; `loopOut("cycle", 1)` loops between the last and second-to-last keyframes; `loopOutDuration("cycle", 1)` loops the last second.
- Values that are too large are clipped to the maximum; too small gives a constant loop.

## Loop types

| Type | Behaviour |
|---|---|
| `"cycle"` | Default. Repeats the segment |
| `"pingpong"` | Repeats, alternating forward and backward |
| `"offset"` | Repeats, offsetting each cycle by the start-to-end value difference times the number of loops so far |
| `"continue"` | No repeat; keeps animating from the velocity at the first or last keyframe. Takes no keyframes or duration argument |

To continue in both directions: `loopIn("continue") + loopOut("continue") - value`. Subtract `value` because both calls include the current value.

## Limits

Keyframe-looping works on most properties, but not on properties that cannot be expressed as simple numeric values in the Timeline panel: Source Text, path shape properties, and the Histogram property of the Levels effect.

## Practical notes (craft, not from the reference)

- For a seamless `cycle`, make the first and last keyframe values match and check the seam at full speed for a hitch or held frame.
- Use `offset` for motion that accumulates, such as travel or rotation that should keep going.

## Verify

Watch several seams at playback speed; with `offset`, check the value after several cycles has accumulated as expected.

## Checked

Method: 2026-11-09 read the property object page of the After Effects expression reference (loopIn, loopOut, the Duration variants, Loop Types). Removed unstated claims: path loops (the reference lists path properties as an exception), Time Remap recipe, seam-frame and tangent advice labelled as craft only.
