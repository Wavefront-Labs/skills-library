---
id: creative-arts.animation.sound-design.music-edit-to-picture
name: music-edit-to-picture
category: creative-arts
field: animation
product: sound-design
tags: [music-edit, music-editing, temp-music, temp-love, edit-on-the-beat, music-stems, tempo-map, music-post]
level: practitioner
status: draft
description: "Edit score and library music to picture: cutting on the beat, lengthening and shortening cues, hitting sync points, working with stems, and managing temp music."
sources:
  - https://www.routledge.com/Producing-Animation/Winder-Dowlatabadi-Miller-Zarneke/p/book/9781138479937
  - https://www.reaper.fm/userguide.php
  - https://www.avid.com/pro-tools
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Editing music to picture

**Goal:** music that starts, hits and ends where the picture needs it, with edits nobody hears.

## Making edits invisible

- Cut **on the beat**, ideally at a downbeat or phrase start (bar 1 of a 4- or 8-bar phrase), into the same
  harmonic position. Set the DAW's tempo map to the cue's tempo to see bars and beats.
- Crossfade short (5-30 ms) on transients; longer crossfades smear rhythm.
- Watch reverb tails: cutting out of a bar whose tail rings into the next makes a jump. Overlap tails or use the
  cue's stem without reverb at the edit and add reverb after.
- Key and orchestration must match across the edit; a cut from strings to full brass is audible.

## Fitting length

- Remove or repeat whole phrases (2, 4, 8 bars) to shorten or lengthen.
- Time-stretch small amounts (under about 3-4%) with a good algorithm (élastique in Reaper, X-Form in Pro Tools) to
  land an end hit; larger stretches change feel.
- Endings: use the cue's real ending (the "button") and back-time it so the last note lands on the picture moment.

## Hitting sync points

Animation can be timed to music (pre-scored) or music to animation (post-scored). For post-scored shows, spot sync
hits (gag hits, cuts, a door slam) with the composer in spotting
(`creative-arts.animation.editorial.spotting-sessions`); editors move cue sections to hit them.

## Stems

Ask for stems (melody, rhythm, pads, percussion) so dialogue can poke through by lowering only the melodic stem,
and so the M&E has clean music (see `creative-arts.animation.sound-design.m-and-e-mix`).

## Temp music risk

Directors fall in love with the temp track ("temp love"). Keep temp music to genre and tempo references, avoid
famous cues, and note in the cut that it is temp. Replace with score or cleared music before any public screening;
temp music is almost never cleared (see `creative-arts.animation.sound-design.music-licensing-sync-and-master`).

## Verify

Play every music edit five times without picture: no listener can spot the edit point; sync hits land within one
frame. Score creation is in `creative-arts.animation.sound-design.scoring`.
