---
id: creative-arts.game-design.level-design.blockout-and-player-guidance
name: blockout-and-player-guidance
category: creative-arts
field: game-design
product: level-design
tags: [game-design, level-design, blockout, greybox, whitebox, layout, player-guidance, leading-lines, landmarks, sightlines, weenie, pacing, intensity-curve, encounter-design, critical-path, gating, breadcrumbs, metrics, unreal, unity, probuilder, bsp, fps, platformer]
level: practitioner
status: draft
description: "Build a level as a greybox first: lock player metrics, sketch flow and pacing, block out in grey shapes, then guide players with landmarks, light and sightlines instead of arrows."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Blockout and player guidance — a level that plays before it looks

**Goal:** prove a level's flow, pacing and readability in untextured grey geometry,
where changes cost minutes, and make players find the way without a waypoint marker.

## 1. Lock metrics before drawing anything
Measure the player character in-engine and write the numbers down:
- Height, collision width, walk/run speed, jump height and distance, crouch height,
  step height, any mantle/climb reach.
- Derive standard sizes: corridor width (at least ~2–3× collision width; more for
  combat or co-op), door height, cover height (below eye level when crouched, above
  when standing), max gap you expect players to clear (leave margin below max jump).
Build a **metrics gallery** — a test map with each size labelled. Every blockout
piece comes from it. Without this, the art pass will discover your jumps are impossible.

## 2. Paper: flow and pacing
- Draw a top-down bubble diagram: spaces as circles, connections as lines, the
  **critical path** marked, optional areas branching off.
- Draw an **intensity curve** along the path: tension (combat, hazards, puzzles)
  rising in waves with rests between. Peaks need a quiet space before them so the
  player can prepare, and after so they can recover and loot.
- Mark gates (locked door, key, ability check) and where the key is seen *before*
  it is reachable — players remember a locked door they've seen.

## 3. Blockout in engine
- Use simple primitives: Unreal BSP/modeling tools, Unity ProBuilder, Godot CSG.
  Colour-code if helpful (walkable, blocking, interactive, hazard).
- Play it constantly at real speed. Time the critical path with a stopwatch; compare
  against your target length.
- Place encounters with spawn points, cover and enemy sightlines blocked in. Ask for
  each fight: where does the player first see it, and can they choose an approach?

## 4. Guide without arrows
Ordered roughly from subtle to blunt:
1. **Landmarks / "weenies"** — a tall, unique object visible from far away (tower,
   beam of light) that pulls players toward the goal. Keep it in view at decision points.
2. **Light and contrast** — players move toward the brightest, highest-contrast exit.
3. **Leading lines** — pipes, cables, roads, wall trims pointing at the way forward.
4. **Framing** — doorways and arches that frame the next objective.
5. **Movement and sound** — an NPC running ahead, a bird flying off, a distant noise.
6. **Consistent affordance colour** — one colour means climbable/interactive
   everywhere (yellow paint is a common convention). Don't use it decoratively.
7. **Breadcrumbs** — pickups along the path.
8. **Explicit UI** — markers, as a last resort or accessibility option.
At every fork, decide which way most players should go first; make the critical
path the brighter, wider, more open one and the optional path visibly secondary.

## Gotchas
- **Designers can't see their own level** — you know the route. Watch fresh players
  silently; where they stall or backtrack, fix guidance, don't add a sign.
- **Scale drifts in art pass** — props get added and corridors shrink below metrics.
  Re-test collision after art.
- **Backtracking without change is padding.** If players must return, open a
  shortcut or change the space (new enemies, lighting).
- **Vertical spaces confuse.** Players rarely look up; put upward routes in the
  natural view cone or signal them strongly.
- Specific multipliers above are common practice, not verified standards; your
  camera (first vs third person) changes them.

## Verify
- [ ] A metrics gallery exists and every blockout piece matches it.
- [ ] A bubble diagram and intensity curve exist for the level.
- [ ] Critical path time measured against target.
- [ ] Three fresh testers reach the exit without hints; stall points noted and fixed.
- [ ] Every fork has a deliberate primary direction readable from the fork.
