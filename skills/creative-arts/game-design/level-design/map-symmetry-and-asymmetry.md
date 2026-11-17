---
id: creative-arts.game-design.level-design.map-symmetry-and-asymmetry
name: map-symmetry-and-asymmetry
category: creative-arts
field: game-design
product: level-design
tags: [game-design, level-design, map-symmetry, multiplayer-maps, competitive-balance, rotational-symmetry]
level: practitioner
status: draft
description: "Choose and balance map symmetry for competitive levels: mirror vs rotational symmetry, asymmetric attack/defence maps, side-swaps and win-rate checks."
sources:
  - https://www.gamedeveloper.com/design/the-hows-and-whys-of-level-design
  - https://www.routledge.com/An-Architectural-Approach-to-Level-Design-Second-Edition/Totten/p/book/9780815361367
  - https://developer.valvesoftware.com/wiki/Map_design
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Map symmetry and asymmetry

**Goal:** a competitive map that is fair to both sides and still interesting to learn.

## Options
| Type | Fairness | Notes |
|---|---|---|
| Mirror (reflection) | high | lighting and sightlines also mirror; left-handed angles differ for players (peek-side bias) |
| Rotational (180 degrees) | high | avoids handedness bias; common in RTS and arena maps |
| Asymmetric, side-swap | balanced over halves | attack/defence maps (Counter-Strike); teams swap sides at half |
| Asymmetric, fixed roles | needs tuning | payload, assault; tune with spawn times and timers |

## Steps
1. Pick the type from the mode: symmetric for deathmatch/CTF; asymmetric for
   attack/defence with side swaps.
2. For symmetric maps, build one half and mirror/rotate, then break visual sameness
   (different themes per side) without changing collision.
3. For asymmetric maps, measure equalities that matter: time from spawn to each
   objective, number of routes, sightline lengths, cover counts.
4. Tune with spawn wave times, objective timers, choke widths.
5. Track side win-rates over many matches and skill brackets; target near 50/50 for
   symmetric, and a known stable split for attack/defence that side swaps neutralise.

## Gotchas
- Sun direction and light differ per side even on mirror maps.
- Mirror maps create corner peeks favouring one side (third-person or right-hand
  weapon models); rotational symmetry fixes it.
- Players memorise symmetric maps quickly; asymmetry adds depth at a balance cost.

## Verify
- [ ] Symmetry type chosen and justified.
- [ ] Spawn-to-objective times measured per side.
- [ ] Side win-rates tracked by bracket.
