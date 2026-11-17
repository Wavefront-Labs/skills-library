---
id: creative-arts.game-design.level-design.multiplayer-map-lane-design
name: multiplayer-map-lane-design
category: creative-arts
field: game-design
product: level-design
tags: [game-design, level-design, multiplayer-maps, lane-design, three-lane-map, competitive-maps, map-flow, chokepoints, rotations, fps-maps, moba]
level: advanced
status: draft
description: "Lay out competitive multiplayer maps around lanes: three-lane structure, connectors and rotations, chokepoints, timing to objectives, and testing with heatmaps."
sources:
  - https://www.gdcvault.com/
  - https://www.routledge.com/An-Architectural-Approach-to-Level-Design-Second-edition/Totten/p/book/9780815361367
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Multiplayer map lane design

**Goal:** a competitive map where routes, timings and engagement points create varied
fights and strategic choices, with no route or position that dominates.

## The three-lane baseline
Many competitive shooter and MOBA maps use three main lanes between team bases or
objectives, with connectors between them:
- **Each lane has a character** (long-range open lane, close-quarters interior lane,
  mid-range mixed lane) so team composition and playstyle choose routes.
- **Connectors** let teams rotate between lanes; rotation time is a key tuning number.
- **Mid control** usually offers fastest rotations; make it contestable, not
  permanently holdable.

## Procedure
1. **Define the mode's needs:** objective locations, team size, respawn rules, match
   length.
2. **Draw the lane graph:** spawns, lanes, connectors, objectives. Annotate travel times
   (measure with player run speed from metrics).
3. **Timing parity:** both teams reach equivalent contested points at the same time
   (symmetric maps make this automatic; asymmetric maps need careful measurement).
4. **Engagement design:** each lane has defined engagement distances, cover and at least
   one flank or alternate approach to every strong position.
5. **Sightlines:** cap the longest sightlines to what the weapon sandbox supports; break
   long lines with geometry.
6. **Blockout and test early** with real players; competitive maps are found in
   playtest, not on paper.
7. **Heatmaps** of deaths and positions show dominant spots and dead lanes.

## Gotchas
- Lanes that are always strictly worse become dead space; give each a reason.
- Too many routes dilute fights; players never meet.
- Vertical advantage (high ground) needs counters (routes up, cover from below).

## Verify
- [ ] Lane graph with measured travel and rotation times.
- [ ] Timing parity for contested points.
- [ ] Every strong position has a counter route.
- [ ] Heatmaps show fights distributed across lanes.
