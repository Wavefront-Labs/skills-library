---
id: creative-arts.game-design.level-design.traversal-design
name: traversal-design
category: creative-arts
field: game-design
product: level-design
tags: [game-design, level-design, traversal-design, movement-design, open-world, mounts-and-vehicles, fast-travel]
level: practitioner
status: draft
description: "Design traversal for large worlds: movement verbs and speeds, terrain affordances, mounts/vehicles, fast travel rules, and travel-time budgets between points."
sources:
  - https://www.gdcvault.com/play/1024562/Change-and-Constant-Breaking-Conventions
  - https://www.routledge.com/An-Architectural-Approach-to-Level-Design-Second-Edition/Totten/p/book/9780815361367
  - https://www.routledge.com/The-Art-of-Game-Design-A-Book-of-Lenses-Third-Edition/Schell/p/book/9781138632059
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Traversal design

**Goal:** moving through the world is fun in itself and the time between interesting
moments stays within budget.

## Steps
1. **List movement verbs** with speeds: walk, run, sprint, climb, glide, swim, mount,
   vehicle, grapple. Record m/s and stamina cost.
2. **Travel-time budget:** target seconds between points of interest at the default
   speed (often 30-90 s in open worlds); place POIs to meet it.
3. **Terrain affordances:** which surfaces each verb can use (climbable cliffs, glide
   from heights, roads for vehicles). Build terrain to reward the verbs.
4. **Speed tiers unlock over time** (mount, glider, grapple) and the world should
   contain spaces built for the faster tiers.
5. **Fast travel rules:** unlock by discovery; from anywhere or only from nodes; cost.
   Fast travel reduces the value of traversal, so make traversal fun first.
6. **Navigation aids:** roads, landmarks, compass; avoid forcing map checks every few seconds.

## Gotchas
- Speed raises streaming and world-density cost; the content must keep up.
- Stamina gating feels bad if regeneration is slow; tune with playtests.
- Vehicles that cannot reach POIs make players dismount constantly; give parking/approach.
- Movement abilities can break level gating; decide what sequence breaks are allowed.

## Verify
- [ ] Verb table with speeds and costs.
- [ ] POI spacing meets travel-time budget per tier.
- [ ] Fast-travel rules written.
- [ ] Sequence-break review done for each new movement tier.
