---
id: creative-arts.game-design.level-design.stealth-level-design
name: stealth-level-design
category: creative-arts
field: game-design
product: level-design
tags: [game-design, level-design, stealth-design, ai-perception, patrol-routes, light-and-shadow]
level: practitioner
status: draft
description: "Lay out stealth spaces: multiple routes, patrol loops and timing, light/shadow and sound surfaces, readable AI perception states and failure recovery."
sources:
  - https://www.gdcvault.com/play/1020004/The-Stealth-Level-Design-of
  - https://www.gamedeveloper.com/design/stealth-level-design-the-basics
  - https://www.routledge.com/An-Architectural-Approach-to-Level-Design-Second-Edition/Totten/p/book/9780815361367
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Stealth level design

**Goal:** a space where observing, planning and choosing a route is the core play, and
getting spotted escalates instead of ending the game.

## Layout
- **Three routes minimum** through each stealth area (e.g. loud direct, quiet flank,
  vertical vents/rooftops).
- **Observation point** at the entry: a safe vantage to read patrols.
- **Cover rhythm:** hiding spots spaced within sprint distance along each route.
- **Light and sound surfaces:** shadows, noisy floors (gravel, metal), distractions
  (bottles, switches) placed deliberately.

## AI patrols
1. Loops with predictable timing; overlapping patrols create windows, not walls.
2. Stationary guards with view cones covering chokepoints, counterable by a route.
3. Document perception: vision cone angle and distance, light modifier, hearing radius
   per surface.

## Readable states
Unaware - suspicious - searching - alerted - returning to patrol. Each needs a clear
audio-visual cue (meter, bark, music). Suspicion should build over time, not trip instantly.

## Failure recovery
Detection should escalate (search, combat, reinforcements) with ways to escape and
re-hide. Instant fail only for explicit "ghost" challenges.

## Gotchas
- Players cannot judge cone length without feedback; show detection meters or barks.
- Too many guards turns stealth into trial and error.
- Inconsistent light rules (bright prop does not count) erode trust.

## Verify
- [ ] Three routes and an observation point.
- [ ] Patrol timings documented with windows.
- [ ] Perception values documented and readable.
- [ ] Detection escalates with escape options.
