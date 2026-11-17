---
id: creative-arts.game-design.systems-and-mechanics.attack-telegraphing
name: attack-telegraphing
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, telegraphing, combat-design, anticipation, wind-up, attack-tells, readability, frame-data, audio-cues, fairness]
level: practitioner
status: draft
description: "Telegraph enemy attacks so players can read and react: anticipation poses, audio and VFX tells, ground indicators, timing windows, and tuning tell length to difficulty."
sources:
  - https://www.gdcvault.com/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Attack telegraphing

**Goal:** every dangerous attack gives the player enough information and time to
respond, so taking damage feels like the player's mistake, not the game's trick.

## Tell channels
| Channel | Examples | Notes |
|---|---|---|
| Animation anticipation | wind-up pose, weapon raise | the principle of anticipation from animation |
| VFX | glint, glow, charge particles | colour-code danger types |
| Ground/area indicators | red circles, cones | strong clarity, less diegetic |
| Audio | distinct sound per attack | works off-screen; add subtitles/visual sound cues for deaf players |
| Camera/UI | indicator arrows for off-screen | needed for flankers |

## Timing
- **Tell duration** (startup frames) is the main difficulty knob: longer = easier.
  Reaction time for humans to a visual stimulus is commonly cited around 200-250 ms;
  tells near that are hard reactions, longer ones are comfortable.
- **Delayed attacks** (pause mid-wind-up) punish button mashing but should still be
  learnable; use sparingly.
- **Consistency:** the same tell always means the same attack.

## Procedure
1. List attacks; for each write: tell (channel), tell duration, answer (dodge
   direction, block, distance), punish window after.
2. Make **dangerous attacks have the most distinct tells**.
3. Test **in combination**: with several enemies, tells overlap. Stagger attack timing
   (attack tokens/"one attacker at a time" systems are common in melee action games).
4. Check tells **at a distance, in clutter and in low light**.
5. Tune tell length by difficulty setting rather than damage alone.

## Gotchas
- Tells hidden by camera angle or other effects are effectively absent.
- Too many ground indicators turn combat into reading floor decals; reserve for big
  area attacks.
- Audio-only tells fail for players with sound off; pair with visuals.

## Verify
- [ ] Each attack has a documented tell, duration and answer.
- [ ] Hardest attacks have the most distinct tells.
- [ ] Multi-enemy encounters tested for overlapping tells.
- [ ] Playtesters can name what hit them in most deaths.
