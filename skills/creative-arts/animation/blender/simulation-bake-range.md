---
id: creative-arts.animation.blender.simulation-bake-range
name: simulation-bake-range
category: creative-arts
field: animation
product: blender
tags: [blender, simulation-bake-range, simulation-frame-range, simulation-nodes, bake, geometry-nodes]
level: practitioner
status: docs-checked
description: "Cache and bake geometry node simulations: scene versus custom frame ranges, bake and delete bake per modifier or zone, disk versus packed targets, and cache invalidation."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/simulation/simulation_zone.html
  - https://docs.blender.org/manual/en/latest/physics/simulation_nodes.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/baking.html
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/geometry_nodes.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# simulation-bake-range

Goal: a simulation that plays back reliably and renders identically on a farm.

## Cache vs bake

- **Cache**: the simulation is cached automatically during playback; the valid cache shows as a strong purple line in the timeline. The *Cache* option on the object can be turned off to save memory when only the current frame matters.
- **Bake**: explicit; saves the result to disk or packs it into the .blend so it can be sent to a render farm and rendered in a non-sequential order. The .blend must be saved first.

## Where to bake

- Physics Properties, Simulation Nodes panel: *Calculate to Frame* (simulate from the start to the current frame), *Bake*, *Delete Cached Simulation*. Baking bakes every simulation in all modifiers of the selected objects.
- Geometry Nodes modifier, *Manage* panel, *Bake* subpanel: *Bake Target* and *Bake Path* for the simulation zones and Bake nodes of that modifier (a bake can override the target). Simulation zones and Bake nodes share the path.

## Frame range

The Bake node in *Animation* mode uses the scene frame range unless *Custom Range* (*Start*, *End*) is set. Check the simulation zone and modifier UI of your Blender version for how the range is chosen for simulation zones; the manual does not describe a per-zone range.

## Target

- *Disk*: baked data goes to a separate directory (*Bake Path*, set per modifier); useful for big caches and farm sharing.
- *Packed*: stored inside the .blend, so no separate file is needed.

## Invalidation

When data is baked the number of baked frames shows above the simulation zone node. Data written by one Blender version may not be readable by another, and the baked format is not an import/export format. Delete the cached simulation and bake again after changing the setup.

## Gotchas

- A simulation is only evaluated while the animation frame changes, so jumping to a frame without a cache does not compute the frames in between; use *Calculate to Frame*.
- Render farms must see the bake folder or bake packed.
- Delta Time is the inverse of the frame rate; re-bake after changing fps.

## Verify

Bake, save, close and reopen the file: the baked frame count shows above the node and frames scrub from the bake.

## Checked

2026-10-27, against the Blender 5.3 manual (branch blender-v5.3-release). Confirmed on the Simulation Nodes (physics), Simulation Zone, Baking, Bake Node and Geometry Nodes modifier pages: Physics panel buttons, cache colour and Cache option, Bake Target and Bake Path, saved-file requirement, version portability warning, Bake node Custom Range. Removed unconfirmed claims: version gates, default bake path, per-zone range and pre-roll, cache-versus-bake invalidation behaviour, command-line render test.

Method: documentation only; no commands were run.
