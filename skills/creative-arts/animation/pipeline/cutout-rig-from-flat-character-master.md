---
id: creative-arts.animation.pipeline.cutout-rig-from-flat-character-master
name: cutout-rig-from-flat-character-master
category: creative-arts
field: animation
product: pipeline
tags: [2d, cutout, rig, puppet, pivots, joints, acting, gesture, breathing, overlap, on-ones, pillow, numpy, scipy, anime, cel, character-animation]
level: advanced
status: draft
description: "Turn one flat line+cel full-figure drawing into a cut-out rig: arms and head on pivots with round joints, re-inked parts, hole fill, and automatic gesture acting on ones."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Cut-out rig from a flat character master

**Goal:** stop the "cardboard standee" read, where a whole character drawing slides,
sways or tilts as one piece. Viewers describe it as "the whole character moves rather
than the mouth or a limb". Split the one master drawing into parts on pivots and move
the parts while the body holds still.

Works on a generated or hand-drawn full figure in anime line + flat colour, when the
arms hang beside the torso with the torso's own side line drawn.

## Measure on the image the renderer actually uses

Measure arm polygons, shoulder and elbow pivots on the processed body the pipeline
composites, at master scale. Don't measure on the source drawing. On one cast member
the hi-res pass was not aligned with the base master, so coordinates measured on the
base produced empty arm masks.

Use a grid crop with coordinate labels drawn by value, and read the labels, not
screen pixels. Reading screen pixels on a 2x crop put every point in the wrong place.
Verify with an overlay of the polygons and pivots on the processed body before
animating anything.

Cut each arm polygon just outside the torso's own side ink, so the torso keeps its
outline when the arm lifts.

## Build the parts

1. **Arm mask** = polygon ∪ a shoulder disc (radius about half the arm width), ∩ alpha.
2. **Split at the elbow** by the sign of the projection on the shoulder-to-elbow axis.
   Give both pieces an elbow disc. Round caps turn in place, so a bent elbow or raised
   arm never opens a gap. Hard straight cuts read as folded paper.
3. **Re-ink every part.** Dilate the part's alpha by about 3 px at master scale, fill
   with ink colour, and composite the part over it. Without this, cut edges show as
   torn paper with no line.
4. **Refill torso holes.** A hand drawn over a skirt or hip leaves a hole when the arm
   lifts. Refill only removed pixels that have torso both above and below them in
   their column, within about 90 master px, from the nearest torso pixel. Flat cel
   colours make nearest-neighbour fill read as drawn. A morphological close fills real
   gaps too, such as the space between the legs, so don't use it.
5. **Head** stays a separate layer and rotates about the chin. If the head was cut
   straight across below the jaw, drop head pixels below the lowest jaw ink in each
   column, then paint a shadowed neck behind the collar. Dilate cloth pixels so the
   collar stays in front, and recolour skin flecks on the collar edge from the
   nearest cloth pixel.
6. **Pre-scale the parts once per shot size**, not per frame.

Rotation directions with PIL (counter-clockwise for positive angles): a screen-left
arm swings outward with a negative angle, a screen-right arm with a positive one.

## Acting that reads as fluid

- **On ones.** Rigged motion on twos steps; render rigged shots on every frame.
- **Breathing:** shoulders and head rise about 3 master px on a 3.6 s sine. The torso
  holds.
- **Speaker gestures** come from lip-sync phrase accents at least 0.9 s apart, with
  alternating arms. Ease in over 6 frames, hold until the next accent or 1.4 s, ease
  out over 9 frames. Shoulder 12 to 24 degrees, elbow 25 to 45 degrees, scaled by
  emotion energy (0.35 hollow to 1.6 frantic).
- **Overlap:** the elbow lags the shoulder by 2 frames.
- **Head:** a nod of about 1 % of head height and a 1.2 to 1.6 degree tilt on each
  stressed syllable, alternating direction.
- **Keep shoulder angles under about 45 degrees** on a front-view master. Bigger
  angles expose the flat drawing.

## Frame the shot so the acting is visible

Medium shots must be waist-up and wide shots full-figure. A medium shot framed at the
chest put every gesture below the frame, so the rig looked unchanged.

## Verify

A sheet of six poses per character (rest, both arms out, one forearm raised, wide
reach, breath, high gesture) on a flat background, checked at full size for gaps,
missing outlines and holes. Then a talking medium shot with its voice line, played
back as video.

See `2d-cutout-lipsync-puppet` for mouths, blinks and plates, and
`methods.anime-dialogue-2d-tier` for where this sits in a dialogue shot.
