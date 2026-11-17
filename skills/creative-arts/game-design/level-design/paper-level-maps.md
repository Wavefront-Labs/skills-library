---
id: creative-arts.game-design.level-design.paper-level-maps
name: paper-level-maps
category: creative-arts
field: game-design
product: level-design
tags: [game-design, level-design, paper-map, level-map, top-down-map, level-planning, bubble-diagram]
level: practitioner
status: draft
description: "Plan a level on paper before the editor: bubble diagram, top-down map at scale, legend, critical path, sightlines and annotations a team can review."
sources:
  - https://www.routledge.com/An-Architectural-Approach-to-Level-Design-Second-Edition/Totten/p/book/9780815361367
  - https://www.routledge.com/The-Art-of-Game-Design-A-Book-of-Lenses-Third-Edition/Schell/p/book/9781138632059
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Paper and top-down level maps

**Goal:** catch layout problems in minutes on paper instead of days in the editor.

## Steps
1. **Bubble diagram:** spaces as circles sized by importance, connected by lines for
   paths. Mark gates (keys, abilities) on lines. Check flow: loops, dead ends, hub.
2. **Scale grid:** pick a unit tied to player metrics (e.g. 1 square = 1 m or a
   multiple of the player's width). Note the player's jump and sprint distances in squares.
3. **Top-down map:** walls, openings, height changes (contour or numbers), cover,
   pickups, enemies, spawns, objectives.
4. **Legend:** consistent symbols (arrow = one-way drop, dashed line = gated path,
   star = landmark, eye = key sightline).
5. **Critical path** in one colour, optional paths in another; number the beats.
6. **Side elevations** for vertical spaces.
7. **Review walk:** narrate a playthrough with a colleague, pointing at the map; note
   every "how do I know to go there?".

## Tools
Graph paper, isometric paper for heights; digital: draw.io, Miro, Photoshop/Krita
layers, or the editor's top-down orthographic screenshots for later revisions.

## Gotchas
- Maps without scale produce spaces that feel huge or cramped in engine.
- Forgetting height on paper hides most sightline problems.
- Paper maps rot after blockout; update or mark superseded.

## Verify
- [ ] Bubble diagram with gates.
- [ ] Top-down at stated scale with legend.
- [ ] Critical path and beats numbered.
- [ ] Walkthrough review notes resolved.
