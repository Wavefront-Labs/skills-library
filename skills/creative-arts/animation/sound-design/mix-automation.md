---
id: creative-arts.animation.sound-design.mix-automation
name: mix-automation
category: creative-arts
field: animation
product: sound-design
tags: [mix-automation, automation-modes, touch, latch, write, read, trim-automation, re-recording-mix, pro-tools, reaper]
level: practitioner
status: draft
description: "Use mix automation modes (read, touch, latch, write, trim) to ride dialogue, music and effects through an episode, with VCAs and snapshot moves for fast changes."
sources:
  - https://www.avid.com/pro-tools
  - https://www.reaper.fm/userguide.php
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mix automation

**Goal:** level and processing changes recorded against time so the mix plays back the same every pass and can be
revised scene by scene.

## Modes

| Mode | Behaviour | Use |
|---|---|---|
| Read | plays automation, ignores moves | playback |
| Touch | writes while you hold a control, returns to existing automation on release | most riding |
| Latch | writes while you hold and keeps the last value after release until stop | setting a new level for the rest of a scene |
| Write | overwrites everything from play to stop | first pass only, dangerous |
| Trim (Pro Tools) / Trim/Read (Reaper) | moves are relative offsets on top of existing automation | "everything here 2 dB down" without destroying rides |

Pro Tools: automation modes per track; *Write to All/Start/End/Punch* commands extend a value across a selection.
Reaper: track automation mode button; envelopes per parameter; *Automation items* for reusable moves.

## Workflow for an episode

1. Static balance first: faders set for the most common scene state.
2. Dialogue rides in touch: ride each line for intelligibility after clip gain
   (`creative-arts.animation.sound-design.clip-gain-levelling`).
3. Music and BG under dialogue: either side-chain ducking or manual rides; manual is more musical
   (see ducking in `creative-arts.animation.sound-design.final-mix`).
4. Use **VCAs** (or Reaper VCA groups) for stems; ride the VCA for broad moves and keep detailed rides on tracks.
5. Revisions: trim mode over the scene, not rewriting.

## Gotchas

- Write mode left armed wipes a scene's work; default to touch.
- Automation follows clips only if "automation follows edits" is enabled; recuts after mix start need it on (Reaper:
  *Envelope points move with media items*; Pro Tools: Automation Follows Edit).
- Plug-in parameters automated on many tracks slow sessions; render where possible.

## Verify

Play an automated scene three times: identical levels each pass (meters/loudness within 0.1 LU), and a trim pass of
-2 dB lowers the scene's dialogue by exactly 2 dB without flattening rides.
