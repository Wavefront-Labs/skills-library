---
id: creative-arts.animation.motion-graphics.ae-graph-editor
name: ae-graph-editor
category: creative-arts
field: animation
product: motion-graphics
tags: [graph-editor, keyframe-interpolation, after-effects, speed-graph, value-graph, separate-dimensions, bezier-handles, motion-design, easing]
level: practitioner
status: draft
description: "Shape motion in the After Effects Graph Editor: value vs speed graphs, separate dimensions, handle pulling for snappy ease-outs, and reading curves for problems."
sources:
  - https://helpx.adobe.com/after-effects/using/speed.html
  - https://helpx.adobe.com/after-effects/using/keyframe-interpolation.html
  - https://helpx.adobe.com/after-effects/using/editing-moving-copying-keyframes.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# The After Effects Graph Editor

**Goal:** motion with intent: fast starts, long settles, overshoots, instead of default linear or
symmetrical eases. The graph editor (Shift+F3 in the timeline) shows keyframes as curves.

## Two graphs

| Graph | Y axis | Use |
|---|---|---|
| Value graph | the property value | positions per axis (with separate dimensions), rotation, opacity: see overshoot and settle |
| Speed graph | rate of change | the default for combined properties (Position, Scale): shape acceleration |

Switch with the graph type menu (bottom of graph editor). Speed graph area under the curve equals
distance travelled; handles stretch speed in time.

## Classic motion-design curve

"Ease in hard, settle long" (a UI element flying in):
1. Keyframe start and end positions. Select both, F9 (Easy Ease).
2. Speed graph: pull the outgoing handle of the first keyframe short (fast start) and the incoming
   handle of the last keyframe long (to ~70-90% influence). Result: a sharp acceleration and long
   deceleration.
3. Or right-click - Keyframe Velocity and type influence values (e.g. out 15%, in 85%).

## Separate dimensions

Right-click Position - Separate Dimensions: X and Y get their own curves in the value graph. Needed
for bounces (Y bounces while X eases), arcs with different timing per axis, and expressions driving
one axis. Caveat: separated position cannot use spatial bezier handles the same way and some
plug-ins expect combined position.

## Reading curves for problems

- Flat plateaus in the speed graph = holds you did not intend (a stop in a motion path).
- Spikes = a keyframe with mismatched in/out speeds (a hitch); make it continuous (Ctrl-click
  keyframe for auto bezier or align the handles).
- Value graph overshoot past the end value = bounce; intended or not.

## Gotchas

- Copying keyframes between layers copies eases as absolute speeds; if distances differ the curve
  shape changes. Re-check the graph after pasting.
- The graph editor shows only selected properties (or those set to show in the graph); toggle "Show
  Selected Properties" to avoid editing the wrong curve.

## Verify

Play at full speed and frame-step the first 6 frames: the element should cover most of its distance
early and creep into the final position, with no hitch at intermediate keys.
