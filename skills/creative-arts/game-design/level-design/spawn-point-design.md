---
id: creative-arts.game-design.level-design.spawn-point-design
name: spawn-point-design
category: creative-arts
field: game-design
product: level-design
tags: [game-design, level-design, spawn-points, spawn-camping, spawn-protection, multiplayer-maps, respawn-logic, deathmatch, competitive-maps]
level: advanced
status: draft
description: "Design multiplayer spawn points and respawn logic: spawn selection scoring, protection from spawn camping, safe exits from team spawns, and testing spawn kills."
sources:
  - https://www.gdcvault.com/
  - https://www.routledge.com/The-Art-of-Game-Design-A-Book-of-Lenses-Third-Edition/Schell/p/book/9781138632059
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Spawn point design

**Goal:** players respawn into the match quickly, safely and fairly, without being
killed on arrival or giving the enemy a predictable farm.

## Team-based fixed spawns (objective modes)
- Spawn rooms with **multiple exits** so one team cannot lock them down.
- Exits should not have direct sightlines from enemy-controllable positions.
- Optional **spawn protection** (brief invulnerability, damage barrier at spawn
  door) - cancel protection when the player attacks.
- Forward spawns that move with objective progress keep travel time reasonable.

## Dynamic spawns (deathmatch / free-for-all)
Score each candidate spawn point at respawn time; pick the best (often with some
randomness among top candidates):
```
score = + distance to nearest enemy (capped)
        - number of enemies with line of sight to the point
        - recent deaths near the point
        + distance from where the player died
        + teammates nearby (team modes)
```
Weights are tuning values; log them and adjust from data.

## Procedure
1. Place many candidate spawns spread across the map (dynamic modes) or design spawn
   rooms (team modes).
2. Implement scoring/selection; expose weights.
3. Test with bots and players; log **spawn kills** (deaths within a few seconds of
   spawning) and spawn-to-first-engagement time.
4. Fix hotspots: remove/move bad spawn points, add cover, adjust weights.

## Gotchas
- Spawning behind enemies is as bad as spawning in front of them (free kills for the
  respawning player).
- Small maps with many players make safe spawns impossible; scale player counts or map
  size.
- Spawn-killing in team modes is also a griefing behaviour; see
  `creative-arts.game-design.systems-and-mechanics.griefing-and-toxicity-mitigation`.

## Verify
- [ ] Spawn rooms have multiple protected exits (team modes).
- [ ] Dynamic spawn scoring implemented with logged weights.
- [ ] Spawn-kill rate measured and under the target threshold.
