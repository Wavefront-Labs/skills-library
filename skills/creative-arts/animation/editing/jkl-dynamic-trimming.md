---
id: creative-arts.animation.editing.jkl-dynamic-trimming
name: jkl-dynamic-trimming
category: creative-arts
field: animation
product: editing
tags: [jkl-trimming, dynamic-trim, jkl, trimming, trim-mode, shuttle, premiere-pro, resolve, avid, keyboard-editing]
level: practitioner
status: draft
description: "Trim cuts by feel with JKL shuttle in trim mode in Avid, Premiere and Resolve: play through the edit, stop on the beat, and the cut point lands there."
sources:
  - https://helpx.adobe.com/premiere-pro/using/trimming-clips.html
  - https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_19_Reference_Manual.pdf
  - https://kb.avid.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# JKL dynamic trimming

**Goal:** set a cut point in real time, by rhythm, instead of nudging frames and replaying.

## JKL basics (all three NLEs)

| Keys | Action |
|---|---|
| L / J | play forward / reverse; tap again for 2x, 4x, 8x |
| K | stop |
| K+L / K+J held | slow forward / reverse (about 1/4 speed) |
| hold K, tap L / J | step one frame |

## Dynamic trim

- **Avid:** enter Trim mode (U), choose A, B or both sides, then play with J/K/L. The trim follows playback and
  commits when you press K (or space). This is the original and still the most fluid implementation.
- **Premiere:** select an edit point, open Trim mode (Shift+T) so the Program monitor becomes the Trim monitor;
  J/K/L shuttle the selected side and the trim is applied when you stop. Ripple vs roll depends on the trim type
  selected (Shift+T cycles in recent versions, or Ctrl/Cmd-click the edit).
- **Resolve:** enable *Dynamic Trim* mode (W) in Trim mode (T); J/K/L then ripple or roll the selected edit as the
  playhead moves, and *Slip/Slide* is used the same way when a clip is selected.

## How editors actually use it

1. Select the outgoing side, play from a second before the cut with L, and hit K on the beat where the action
   should end (an eye-blink, a line's last syllable plus 2-4 frames of breath).
2. Review with a play-around-edit loop (Premiere Shift+K, Avid's loop in trim mode) and repeat. Three passes by feel
   beat ten passes by nudging.
3. On animatics, trim board holds to the scratch VO rhythm; on animation, trim within handles only
   (see `creative-arts.animation.editing.ripple-roll-trims`).

## Gotchas

- Reaction latency: most people stop 2-4 frames late. Calibrate by trimming to a known click track, then
  compensate or set a trim offset where the NLE offers one.
- Sync locks must be on, or a ripple from a dynamic trim pulls later dialogue out of sync.

## Verify

Loop the edit five times: the cut lands on the same musical/dialogue beat each pass and downstream sync is intact.
