---
id: creative-arts.game-design.level-design.enemy-wave-and-spawn-design
name: enemy-wave-and-spawn-design
category: creative-arts
field: game-design
product: level-design
tags: [game-design, level-design, wave-design, spawn-design, encounter-design, horde-mode, ai-director]
level: practitioner
status: draft
description: "Design enemy spawns and waves for encounters: spawn locations out of sight, wave composition and timing, escalation curves, triggers and anti-camping rules."
sources:
  - https://www.routledge.com/An-Architectural-Approach-to-Level-Design-Second-Edition/Totten/p/book/9780815361367
  - https://www.routledge.com/The-Art-of-Game-Design-A-Book-of-Lenses-Third-Edition/Schell/p/book/9781138632059
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enemy wave and spawn design

**Goal:** encounters whose enemies arrive believably, in readable groups, with rising pressure.

## Spawn placement
- Spawn out of the player's view (behind doors, vents, around corners) and at a
  distance that allows reaction time.
- Prefer **closets/entry points** with a visible arrival (doors burst, dropship) over
  popping into existence.
- Never spawn behind the player without an audio cue; avoid spawning in cleared areas
  unless it is the design (pursuit).
- Valve's Left 4 Dead director spawns around the survivors' flow distance, out of sight,
  based on an estimated intensity per player.

## Wave structure
1. **Composition table:** per wave, enemy types and counts; introduce one new type or
   combination per wave.
2. **Escalation:** count and toughness rise; insert a lighter wave after a hard one.
3. **Timing:** start next wave on a kill threshold (e.g. 70% of the wave dead) or a timer,
   whichever comes first; kill-threshold rewards skill, timers create pressure.
4. **Concurrency cap:** max active enemies to keep readability and performance.
5. **Breathers:** pickup or shop windows between waves (horde modes).

## Triggers
Volumes on the path, objective events, or a director with intensity tracking.
Make each trigger fire once and handle players who skip it.

## Gotchas
- Infinite spawns without a cue feel unfair; signal them (alarm, "they keep coming").
- Players camp chokepoints; vary entry points or flank waves.
- Co-op scaling: scale counts or health with player count.

## Verify
- [ ] Spawn points out of sight with arrival cues.
- [ ] Wave table with escalation and breathers.
- [ ] Concurrency cap and co-op scaling set.
- [ ] Skip/sequence-break cases tested.
