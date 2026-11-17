---
id: computing-software.game-programming.godot.navigation-layers-and-agent-sizes
name: navigation-layers-and-agent-sizes
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, navigation-layers, navigation-maps, agent-radius, navigation, game-programming]
level: practitioner
status: docs-checked
description: "Support different agent sizes and movement types in Godot navigation with separate navigation meshes and maps, navigation layers bitmasks, and per-agent filtering."
sources: ["https://docs.godotengine.org/en/stable/tutorials/navigation/navigation_different_actor_types.html", "https://docs.godotengine.org/en/stable/tutorials/navigation/navigation_using_navigationlayers.html", "https://docs.godotengine.org/en/stable/tutorials/navigation/navigation_using_navigationmaps.html", "https://docs.godotengine.org/en/stable/classes/class_navigationserver3d.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Navigation layers and agent sizes

**Goal:** small goblins fit through gaps that ogres cannot, and boats stay on water.

## Agent size needs separate navmeshes
A navmesh is baked for one `agent_radius`/`agent_height`/`agent_max_climb`/`agent_max_slope`. For
several sizes, bake one NavigationMesh per size and put each on its own **navigation map**:
```gdscript
var map_small := NavigationServer3D.map_create()
var map_large := NavigationServer3D.map_create()
for m in [map_small, map_large]:
    NavigationServer3D.map_set_cell_size(m, 0.25)
    NavigationServer3D.map_set_active(m, true)
$NavRegionSmall.set_navigation_map(map_small)
$NavRegionLarge.set_navigation_map(map_large)
$Ogre/NavigationAgent3D.set_navigation_map(map_large)
```
The default world map serves the most common agent; extra maps for others. Cell size of each map must
match its navmeshes.

## Navigation layers (movement types on one map)
NavigationRegion `navigation_layers` bitmask marks what a region is (bit 1 ground, bit 2 water, bit 3
restricted). NavigationAgent `navigation_layers` says what it may use; paths only cross regions
whose layers intersect the agent's mask.
```gdscript
$Boat/NavigationAgent3D.navigation_layers = 0b010     # water only
$Amphibian/NavigationAgent3D.set_navigation_layer_value(1, true)
$Amphibian/NavigationAgent3D.set_navigation_layer_value(2, true)
```
Name layers in Project Settings > Layer Names > 3D Navigation. Change a region's layers at runtime (for example with `set_navigation_layer_value`) to
open or close areas such as a gate. Query with `NavigationServer3D.map_get_path(map, from,
to, optimize, layers)`.

## Costs
Region `enter_cost` and `travel_cost` bias routes (avoid mud, prefer roads) instead of forbidding.

## Gotchas
- Layers filter, they do not change size; a large agent on a small-agent navmesh still clips walls.
- Navigation links have their own layers; set them for the agents that may use them.
- Avoidance layers (`avoidance_layers`/`avoidance_mask`) are a separate system from navigation layers.

## Verify
- [ ] Debug navigation view shows each map; large agents never path through narrow gaps; boats stay on water.

## Checked

2026-10-25, against godot-docs master ("latest" docs, last commit 2026-10-24). Confirmed in the different-actor-types tutorial and class pages: one navigation map and navmesh per agent size, map_set_cell_size must match the navmesh cell size, NavigationServer3D.map_get_path(map, origin, destination, optimize, navigation_layers = 1), region and link navigation_layers bitfields, set_navigation_layer_value, Project Settings layer_names/3d_navigation, region enter_cost and travel_cost, and the NavigationMesh agent_* parameters.

Method: documentation only; no commands were run.
