---
id: computing-software.game-programming.game-ai-programming.navmesh-generation-and-dynamic-avoidance
name: navmesh-generation-and-dynamic-avoidance
category: computing-software
field: game-programming
product: game-ai-programming
tags: [game-ai-programming, navmesh, recast, detour, navigation-mesh, dynamic-obstacle, off-mesh-link, rvo, local-avoidance, velocity-obstacle, agent-radius, tile-cache, crowd-simulation, unity-navmesh, unreal-navmesh, game-programming, tiled-navmesh]
level: advanced
status: draft
description: "Bake and query navigation meshes correctly (Recast/Detour-based), handle runtime-changing obstacles, and add local avoidance so agents don't collapse into each other."
sources: ["https://github.com/recastnavigation/recastnavigation"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Navmesh generation and dynamic avoidance

**Goal:** get agents walking on a correctly-baked navmesh and avoiding each
other locally — this is the layer below A*/pathfinding
(`computing-software.game-programming.game-ai-programming.astar-pathfinding-and-behaviour-trees`
covers the search itself); this skill is about building the mesh the search runs
on and reacting to a world that changes after baking.

## How Recast builds a navmesh (why settings matter)
Recast (the de facto standard engine under Unity's NavMesh, Unreal's
NavMesh/RecastNavMesh, Godot's NavigationServer) voxelizes level geometry, finds
walkable surfaces by slope/height, then simplifies that into convex polygons.
Three settings decide whether an agent fits where you expect:
- **Agent radius**: the navmesh is eroded inward by this amount from walls — too
  small and agents visually clip corners; too large and tight corridors become
  unwalkable. Match it to the actual collision radius, not a guess.
- **Agent height / max slope / max step**: determine which floor geometry counts
  as walkable (a ramp vs a wall) and whether a ledge is a climbable step or a
  cliff. A ramp just over max slope silently becomes unwalkable with no error —
  check the baked mesh visually, don't assume the settings matched intent.
- **Cell size/height** (voxelization resolution): too coarse loses thin walkways
  and doorways; too fine blows up bake time and memory on large levels. Bake
  time scales roughly with level volume / cell_size³ — profile a bake on your
  actual level size before committing to a resolution.

## Dynamic obstacles
A navmesh baked once goes stale the moment something moveable blocks a path
(a closed door, a destroyed wall opening a shortcut, a player-placed turret).
Three approaches, in order of cost:
1. **NavMeshObstacle / carving** (Unity: `NavMeshObstacle` with Carve on;
   Unreal: `NavModifierComponent` on a dynamic actor) — cuts a hole in the
   navmesh around the object at runtime. Works for a handful of slow-moving or
   static-when-active obstacles; carving every frame for many fast movers is
   expensive (it's a re-triangulation, not free).
2. **Off-mesh links** — explicit designer/runtime-toggled connections (a door
   that's "open" or "closed" toggles a link's enabled state) for known
   chokepoints. Cheap, bounded, but must be authored.
3. **Full re-bake of a region** (TileCache / NavMeshData async rebuild) — for
   structural changes (a building collapses). Expensive; do it async and only
   for the affected tiles, never the whole level, and expect a frame or more of
   latency before agents react — have them treat the obstacle as a temporary
   blocker (local avoidance) in the meantime, not walk through it.

## Local avoidance (RVO / ORCA)
Pathfinding gives a route; it does not stop ten agents converging on one
doorway from interpenetrating. **Reciprocal Velocity Obstacles (RVO)** / ORCA
compute each agent's velocity each tick accounting for nearby agents' current
velocities (not just positions), so agents steer around each other smoothly
without freezing or oscillating — this is what Unity's
`NavMeshAgent.avoidancePriority`, Unreal's `UCrowdFollowingComponent`, and
Godot's `NavigationAgent2D/3D.avoidance_enabled` wrap. Gotchas:
- Avoidance radius ≠ navmesh agent radius necessarily — a tighter avoidance
  radius than the navmesh's baked erosion lets agents visually overlap before
  avoidance kicks in.
- Priority matters: a lower-priority agent yields to a higher one; leaving
  every agent at the same default priority in a dense crowd produces visible
  indecisive jitter as no one yields — assign priority by role (a boss shoves
  through, minions yield).
- Avoidance is local and short-horizon; it does not replace re-planning a
  genuinely blocked path — pair it with periodic path validity checks for
  long-lived obstacles, not just steering around them forever.

## Verify
- [ ] Baked navmesh visually inspected against agent radius/height/slope on
      every ramp, doorway, and ledge that matters — not assumed correct from
      default settings.
- [ ] Dynamic obstacles use the cheapest method that fits (carve for a handful,
      off-mesh links for known chokepoints, async region rebake only for
      structural changes).
- [ ] A crowd of agents converging on one doorway/chokepoint doesn't
      interpenetrate or visibly deadlock, tested with agent count at the actual
      target density, not 2-3 agents.
