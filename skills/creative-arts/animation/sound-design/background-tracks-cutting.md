---
id: creative-arts.animation.sound-design.background-tracks-cutting
name: background-tracks-cutting
category: creative-arts
field: animation
product: sound-design
tags: [background-cutting, backgrounds, ambience, crossfades, looping, scene-transitions, checkerboarding, room-tone]
level: practitioner
status: draft
description: "Cut background (ambience) tracks across an animated scene: one continuous bed per location, crossfades at cuts, looping without audible seams, and prelaps into new scenes."
sources:
  - https://www.reaper.fm/userguide.php
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cutting and crossfading background tracks

**Goal:** each location has a continuous, believable ambience that carries across picture cuts within the scene
and changes cleanly at scene changes.

## Structure

- Backgrounds (BGs) run **under the scene, not the shots**: cutting the BG at every picture cut sounds jumpy. Change
  only when the location or perspective really changes (interior to exterior).
- Two to four layers per location: base tone (air, room), a characterful layer (traffic, birds, machines), a
  detail layer (distant dog, occasional car). Checkerboard them across BG tracks (BG1-BG4) so transitions overlap.

## Transitions

- Crossfade between locations over 4-12 frames at a hard cut, or longer with a dissolve.
- **Prelap:** start the next scene's BG a few frames to a second before the picture cut to pull the audience
  forward; **postlap** the previous scene's tail for a softer exit.
- A hard cut to silence or to a very different BG is a strong storytelling choice; use it on purpose.

## Looping

Library ambiences are often shorter than scenes:
- Loop with a long equal-power crossfade (2-5 s) at a section with no distinctive events.
- Avoid repeating identifiable events (a bird call every 30 s gives the loop away); delete them from the loop and
  place a few manually.
- Better: chain different sections of a long recording instead of looping one short piece.

## Animation specifics

Animation has no production sound; BGs carry all the space. Match the BG to the art direction (a stylised clean world
can have sparse, clean BGs). The stylized pipeline's generated beds are covered in
`creative-arts.animation.sound-design.ambience-beds`.

## Verify

Listen to the scene with only BGs: no level jumps at picture cuts within the scene, no audible loop seams or
repeated events, and scene changes are deliberate (crossfade or prelap) rather than accidental.
