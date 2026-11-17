---
id: creative-arts.game-design.level-design.verticality-in-level-design
name: verticality-in-level-design
category: creative-arts
field: game-design
product: level-design
tags: [game-design, level-design, verticality, level-layout, height-advantage, sightlines, 3d-navigation]
level: practitioner
status: draft
description: "Use height in level layouts: high-ground advantage and counterplay, readable vertical routes, falls and drops, sightlines, and metrics for climbing and ledges."
sources:
  - https://www.routledge.com/An-Architectural-Approach-to-Level-Design-Second-Edition/Totten/p/book/9780815361367
  - https://www.gamedeveloper.com/design/the-importance-of-verticality-in-level-design
  - https://www.routledge.com/The-Art-of-Game-Design-A-Book-of-Lenses-Third-Edition/Schell/p/book/9781138632059
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Verticality in level design

**Goal:** height that adds tactical choice and spatial interest without confusing navigation.

## Uses of height
- **Tactical advantage:** high ground sees more and is harder to hit; balance with
  longer exposure on approach and limited exits.
- **Overview and orientation:** a vantage point that shows the next goal (prospect).
- **Pacing:** descent reads as progress into danger; ascent as climax.
- **Shortcuts:** drop-downs that are one-way back to earlier areas.

## Design rules
1. **Readable connections:** every height level has at least two obvious ways up or
   down (stairs, ramps, ladders, climb edges) marked with consistent visual language.
2. **Counterplay for high ground:** routes to flank, cover from below, or vertical
   abilities for the low side.
3. **Metrics:** step height, max climb, safe fall height, fall damage threshold;
   document them and build to them.
4. **Sightline control:** check views both down and up; a sniper perch that sees every
   spawn is a balance bug.
5. **Layer separation:** distinct materials or lighting per floor so players know where they are.
6. **Camera:** third-person cameras struggle under low ceilings and at ledges; test framing.

## Gotchas
- Players rarely look up; place goals and threats above only with cues (sound, light, motion).
- Multi-floor maps confuse minimaps; show floor indicators.
- AI navigation across heights needs nav links and jump points.

## Verify
- [ ] Each height level has two readable connections.
- [ ] High-ground positions have listed counterplay.
- [ ] Vertical metrics documented and respected.
- [ ] Minimap/floor indicator tested.
