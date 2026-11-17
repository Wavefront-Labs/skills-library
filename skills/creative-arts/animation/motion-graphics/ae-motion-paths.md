---
id: creative-arts.animation.motion-graphics.ae-motion-paths
name: ae-motion-paths
category: creative-arts
field: animation
product: motion-graphics
tags: [motion-path, keyframe-interpolation, spatial-interpolation, after-effects, auto-orient, bezier-path, arcs, paste-mask-to-position, motion-design]
level: practitioner
status: draft
description: "Control spatial interpolation and motion paths in After Effects: bezier path handles, arcs, auto-orient, pasting a mask path into Position, and the default-spatial preference."
sources:
  - https://helpx.adobe.com/after-effects/using/keyframe-interpolation.html
  - https://helpx.adobe.com/after-effects/using/assorted-animation-tools.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Motion paths and spatial interpolation

**Goal:** objects travel along the path you want (arcs, figure-eights, along a drawn route) rather
than overshooting loops or straight robotic lines. Spatial interpolation shapes the path; temporal
interpolation shapes the timing.

## Editing the path

- Select a layer with Position keyframes: the comp viewer shows the motion path with dots per frame
  (dot spacing = speed).
- Pen tool (G) on the path: drag handles at a keyframe to curve the path; Convert Vertex tool
  (Alt-click a keyframe) toggles linear/bezier.
- Arcs read as natural motion (principle of arcs): curve paths between keys rather than letting them
  run straight.

## Unwanted loops and overshoot

Auto bezier spatial interpolation can create loops when keyframes are close in space but far in
time. Fix: select the keys - Animation - Keyframe Interpolation - Spatial: Linear, or pull handles.
Preference: Edit - Preferences - General - "Default Spatial Interpolation to Linear" stops surprise
curves on new keys (many motion designers enable it).

## Auto-orient

Layer - Transform - Auto-Orient - Orient Along Path: the layer rotates to face its travel direction
(paper plane, car). Add a rotation offset if the artwork faces the wrong way.

## Paths from shapes

Copy a mask or shape path (select the Path property, Ctrl/Cmd+C), select the Position property and
paste: AE creates position keyframes along the path (roving in the middle, 2 s default). Retime by
moving the last key. Good for routes on maps and logo traces.

## Rove across time

Middle keyframes along a path can be set to rove (`creative-arts.animation.motion-graphics.ae-roving-keyframes`)
to get constant speed along a complex path.

## Gotchas

- Separate Dimensions removes spatial bezier handles from Position; arcs then come from per-axis
  value curves.
- 3D layers have Z on the path; check the path in a side view.

## Verify

Look at the dotted motion path: evenly spaced where speed should be constant, bunched into
ease-in/out zones, no loops at keys.
