---
id: creative-arts.game-design.level-design.blockout-to-art-handoff
name: blockout-to-art-handoff
category: creative-arts
field: game-design
product: level-design
tags: [game-design, level-design, art-pass-handoff, blockout, greybox, environment-art, level-pipeline, metrics]
level: practitioner
status: draft
description: "Hand a locked greybox level to environment art without breaking gameplay: lock criteria, metric and collision contracts, handoff package and art-pass review."
sources:
  - https://www.routledge.com/An-Architectural-Approach-to-Level-Design-Second-Edition/Totten/p/book/9780815361367
  - https://dev.epicgames.com/documentation/en-us/unreal-engine
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Blockout-to-art handoff

**Goal:** environment art dresses the level without changing what made it play well.

## Lock criteria (before handoff)
- Critical path and main encounters playtested with target players; no open layout bugs.
- Metrics validated (jump distances, cover heights, door widths, sightlines).
- Lighting intent pass done (key landmarks and guidance lights blocked in).
- Sign-off from design lead; the blockout is tagged in version control.

## Handoff package
1. **Annotated top-down map** with zones, critical path, sightlines that must stay open,
   cover objects that must keep height, and "do not touch" volumes.
2. **Metrics sheet:** player capsule size, step height, max jump gap, cover heights (e.g.
   half and full), corridor minimum widths.
3. **Collision contract:** art meshes keep simple collision matching the greybox; ornate
   detail gets no collision or is placed outside the play space.
4. **Reference board** per zone (mood, era, materials) and landmark list.
5. **Gameplay layer** kept separate (triggers, spawns, nav modifiers) on its own sublevel
   or layer so art passes do not move them.

## Art pass review
- Replay the critical path after each art drop; compare times and death heatmaps to the greybox.
- Check readability: interactables and climbable edges still visually distinct; colour
  language preserved.
- Run navmesh rebuild and AI tests; art props often block nav.
- Profile performance in the densest view.

## Gotchas
- Kitbashed props with complex collision snag players on edges; use blocking volumes.
- Raising floor detail (rubble) changes jump metrics and cover heights.
- Lighting art can kill guidance lighting; agree which lights are gameplay lights.

## Verify
- [ ] Lock checklist signed.
- [ ] Map, metrics sheet and collision contract delivered.
- [ ] Gameplay layer separated.
- [ ] Post-art playtest matches greybox times within tolerance.
