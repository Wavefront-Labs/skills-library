---
id: creative-arts.animation.pipeline.drawn-props-on-cutout-shots
name: drawn-props-on-cutout-shots
category: creative-arts
field: animation
product: pipeline
tags: [2d, props, cutout, staging, show-dont-tell, physics, timing, sfx-sync, inserts, pillow, anime, continuity]
level: advanced
status: draft
description: "Put the script's objects on screen in a 2D cut-out pipeline: ink+flat prop sprites anchored to the figure, carry poses, falls timed to the SFX, plate props, hand-held inserts."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Drawn props on cut-out shots

**Goal:** when the action line says "the bottom bag splits, groceries drop" or "an
orange bounces off the curb into the drain", the viewer has to see it. A
script-to-picture audit of one episode found none of its objects ever drawn, and the
owner's note was "it talks about a bounce and you never see it". Props are cheap
when they are data on the shot, drawn in the same ink and flat colour as the
characters.

## Style rules

- Draw sprites at 2x with Pillow and downsample: ink outline about 3 % of the sprite
  width, flat fills, one hard shade band on the side away from the key light.
- Add one or two identifying details per prop: a bread loaf and celery in a grocery
  bag, can rims and a label, a stem dimple on an orange so its spin reads.
- Typeset cards over a blurred background read as a different show. Give paper props
  the same ink outline and a hard drop shadow, and keep the text simple.

## Anchor to the figure, not the frame

- Take the figure's bounding box in frame coordinates from the first frame and cache
  it. Place props by head height: the chest is one head below the top of the box.
  This scales the same prop correctly for wide and medium shots.
- **Carry pose:** a character holding something gets forearms bent inward, with
  elbows at -50 degrees on the rig. Draw the props over the figure, then the hands
  last, as skin ellipses at the prop's sides in that character's own skin colour,
  read from the cel master. A fixed skin colour put an older man's hands on a
  teenager.
- Draw props inside the character's lighting pass, so they take the same key tint
  and rim.

## Motion timed to the sound

Use simple physics scaled to the shot: gravity of about 6000 px/s² at a 380 px head,
scaled by head size. Solve release times backwards from the effect beats. With
impacts at 0.7, 1.0 and 1.35 s and a 0.3 s fall to the frame edge, release can, can
and box at about 0.4, 0.65 and 1.0 s, with the tear at 0.25 s on the sting and impact
frame. Spin falling objects in alternating directions.

A plate prop, like an orange on a curb painting, is drawn into the plate before the
camera move, so it moves with the world. Measure its path on a 1920×1080 grid of that
painting: entry, the one bounce as a parabola, a roll that eases out to the target,
then shrink and darken over 0.35 s to drop it into the drain.

## Hand-held inserts

A close-up of paper or a photo makes sense when someone is holding it. Bring the
character's hands up from the bottom of frame, easing in over 0.35 s, with sleeve
cuffs running off the frame edge and thumbs over the front. For a flip, scale the
card horizontally by |cos| over 0.4 s about the card's own centre, not the frame's,
and swap front for back at the midpoint. Keep text clear of the thumbs.

## Data on the shot

```json
"props": {"okafor": "bag_split"}, "props_t": 0.25
"props": {"plate": "orange_roll"}
```

A character prop overrides any gesture-pose variant on that shot, so drop the pose
when you add a prop.

## Verify

Grab frames from the final cut at each prop beat and check the object is visible and
in contact with whoever holds it. Play the shot with sound and check every impact
lands on a visible event.

See `editorial.script-to-picture-audit` for finding the missing props and
`pipeline.cutout-rig-from-flat-character-master` for the rig they attach to.
