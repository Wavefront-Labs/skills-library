---
id: creative-arts.film-live-action.film-sound-design.foley-recording-and-performance
name: foley-recording-and-performance
category: creative-arts
field: film-live-action
product: film-sound-design
tags: [film-sound-design, film-live-action, sound-post, post-production-sound, foley, foley-recording, foley-artist, foley-mixer, foley-stage, foley-pits, footsteps, feet, moves, cloth, cloth-pass, props, specifics, foley-cue-sheet, foley-spotting, foley-session, surfaces, shoes, pits, foley-mic, mkh-50, mkh-416, u87, close-mic, perspective, foley-editing, foley-sync, foley-stems, m-and-e, international-version, dubbing-foley, foley-in-the-box, library-foley, pro-tools-foley, perspective-matching, foley-premix, foley-spotting-cue, foley-cue-sheet-use, footsteps-foley, foley-surfaces, cloth-pass-foley, foley-moves, foley-props, foley-specifics, foley-stage-setup, foley-mics, foley-editing-sync]
level: practitioner
status: draft
description: "Spot, record, perform and edit foley: feet, moves and specifics passes, cue sheets, stage and mic setup, performing to picture, sync and perspective, foley stems for the M&E."
sources:
  - "https://www.mpse.org/ (Motion Picture Sound Editors - foley craft)"
  - "Vanessa Theme Ament, The Foley Grail"
  - "https://www.avid.com/pro-tools (Pro Tools - recording to picture and sync workflows)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Foley recording and performance

**Goal:** every footstep, cloth move and prop handled on screen exists as a clean,
sync, perspective-correct recording - because production sound never captures it
usably and the foreign-language version needs it all.

## 1. Spotting and the cue sheet
Watch the locked picture (with the dialogue edit if available). Build a **cue sheet**
per reel with timecode in/out, character, action, surface, and pass type:
- **Feet**: every on-screen (and relevant off-screen) footstep per character; note shoe
  type (heel, trainer, boot), surface (wood, concrete, gravel, carpet, stairs), tempo
  and weight.
- **Moves / cloth**: body movement, sitting, hugs, arm swings - the pass that glues
  dialogue scenes; one pass per character for close shots, one for the group in wides.
- **Specifics / props**: everything handled - doors, keys, cups, paper, guns, bags,
  punches (body hits), kisses, eating. Note what the prop is and what it should sound like
  (not always the real thing).
Group cues by surface/prop so the artist isn't changing shoes every minute. Typical
drama: 150-400 cues per reel; budget stage days accordingly (a good team covers a reel
of feet in a day).

## 2. The stage
- A dead-ish room with **pits**: wood, concrete, gravel, dirt, marble/tile, carpet,
  grass/leaves, water trough; a stair unit; a door frame rig with several doors; a
  prop library (shoes by type, cloth of various weights, bags, glass, metal, "wet"
  props, kitchenware).
- **Mics**: a hypercardioid/shotgun (Sennheiser MKH 50/416, Schoeps) at 0.5-1 m for
  feet and props; a large-diaphragm condenser (U87) for cloth/moves and gentle props;
  often a second mic further back for perspective. Minimal room tone; no reverb (added
  at the mix).
- Picture on a large monitor with timecode/streamers; the foley mixer in Pro Tools
  records to picture with the track armed on a **cue-based layout** (feet tracks per
  character, moves, props A/B/C), using the cue sheet as markers.

## 3. Performing
- **Feet**: the artist watches the walker's weight, rhythm and gait, not the feet;
  heel-toe, scuffs, stops and shifts. Two or three takes; sync performed live rather
  than edited. Match shoe and surface; use "wrong" surfaces when they sound more like
  the picture (a cardboard box for hollow floor).
- **Cloth**: performed with the chest-level mic, the artist mimics the movement in
  cloth of the right weight (denim vs silk); subtle, continuous, keyed to gesture.
- **Props**: creative substitution - celery for bones, leather gloves for bird wings,
  a wet chamois for kisses; punches with a phone book/meat/chest hits; glass handled
  carefully; weight sells reality.
- Record **wild variations** of key props/surfaces for the editor to use elsewhere.
- Perspective: close for CU, more distant/less detail for wides; record both when
  the shot size changes mid-cue.

## 4. Editing and sync
Foley editor tightens sync to the frame (the eye forgives early foot by 1 frame, not
late), cleans breaths/clicks, chooses takes, splits perspective by shot, and fills
missing cues from library foley (Pro Tools + Soundminer) where a stage retake isn't
possible. Keep tracks organised: `FEET A/B`, `MOVES A/B`, `PROPS A-D` per character/
type, with handles; label with cue IDs.

## 5. Delivery
Foley goes to the **premix** as its own stem family (FX premix or a dedicated Foley
premix); it must be **complete for the M&E** (music and effects version) - every sound
a foreign dub needs replaced from production. Deliver conformed to the reel's timecode
with a cue list; at the mix, foley sits under production effects, often lower than the
editor expects.

## Gotchas
- Spotting from the picture alone and missing off-screen footsteps the dialogue editor removed.
- Foley recorded with reverb; can't sit in a different room in the mix.
- Over-detailed, loud foley that fights dialogue ("foley porn").
- Mid-cue shot-size changes recorded at one perspective.
- Feet cues on characters who are dubbed later - still needed; it's the M&E.

## Verify
- [ ] Cue sheet per reel covering feet, moves and specifics, grouped by surface/prop.
- [ ] Stage setup: correct surfaces/shoes, close and perspective mics, dry room.
- [ ] Performed to picture with sync within a frame; wild variants recorded.
- [ ] Foley stems complete for the M&E and delivered conformed with cue lists.
