---
id: creative-arts.game-design.systems-and-mechanics.hud-design
name: hud-design
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, hud-design, game-ux, game-interface, diegetic-ui, information-hierarchy, ui-design, readability, safe-area, schell]
level: practitioner
status: draft
description: "Design a game HUD: decide what information is needed when, choose diegetic/non-diegetic/spatial/meta forms, set hierarchy and placement, and test readability."
sources:
  - https://www.routledge.com/The-Art-of-Game-Design-A-Book-of-Lenses-Third-Edition/Schell/p/book/9781138632059
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# HUD design

**Goal:** the player sees the information they need for their next decision at a
glance, and nothing that distracts from play.

Schell (2nd ed.) ch15 (interface) asks what information the player needs and when, and which
channels carry it. A widely used framework (Fagerholt and Lorentzon's thesis, 2009)
classifies UI as **diegetic** (in the world and fiction), **non-diegetic** (overlay),
**spatial** (in the world but not the fiction, e.g. outlines) and **meta** (in the
fiction but not the space, e.g. blood on screen for damage).

## Procedure
1. **Information inventory:** list every piece of information the player might need.
   For each: how often needed, how urgent, during what activity.
2. **Prioritise:**
   | Priority | Treatment |
   |---|---|
   | critical + constant (health in combat) | always visible, prime location |
   | critical + occasional (low ammo) | appears on change or threshold |
   | useful (minimap, objectives) | persistent but subdued, or on demand |
   | rare (stats) | menus |
3. **Choose forms:** diegetic for immersion where readable (ammo counter on the gun);
   non-diegetic when clarity matters more.
4. **Placement:** keep critical info near where the eyes are during play (near the
   crosshair/character); corners for low-frequency info. Respect TV/console safe areas.
5. **Contextual HUD:** fade elements when not relevant (full health bar hidden).
6. **Accessibility:** scalable text and HUD, colour-blind-safe status colours, icons +
   numbers, contrast backgrounds.

## Testing
- **Glance test:** show a screenshot for 1-2 seconds; ask what the player's health,
  objective and threat were.
- Watch eye movement if possible (eye tracking) or ask players to think aloud about
  what they look at.

## Gotchas
- Diegetic-only UI that players cannot read in the heat of play fails clarity.
- HUD clutter grows feature by feature; re-run the inventory each milestone.
- Animated HUD elements pull attention; reserve motion for alerts.

## Verify
- [ ] Information inventory with priority and form per item.
- [ ] Glance test passed by most fresh testers.
- [ ] Safe-area, scaling and colour-blind checks done.
