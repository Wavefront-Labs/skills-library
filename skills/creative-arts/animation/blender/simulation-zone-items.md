---
id: creative-arts.animation.blender.simulation-zone-items
name: simulation-zone-items
category: creative-arts
field: animation
product: blender
tags: [blender, simulation-zone-items, simulation-state, zone-items, simulation-nodes, geometry-nodes]
level: advanced
status: docs-checked
description: "Manage Simulation Zone state items in geometry nodes: adding, typing and ordering items, what persists between frames, delta time, and passing attributes through the state."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/simulation/simulation_zone.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/simulation/index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# simulation-zone-items

Goal: carry exactly the data a simulation needs from one frame to the next.

## What a state item is

Everything connected to the Simulation Output's inputs is stored at the end of a frame and fed back into the Simulation Input on the next frame. Each pair of sockets is a **state item**.

## Add and edit items

- Drag a link into the empty socket on Simulation Output (or Input) to add an item of that type.
- Node editor sidebar → *Node* tab → *Simulation State* panel: items can be renamed (also `Ctrl-LMB` on the socket name), reordered and removed.
- Inputs connected to the Simulation Input node are evaluated only once, at the start, then passed on from state to state. Other nodes can be linked into the zone from outside and are re-evaluated every step; no link may go from inside the zone to outside, so results are only reachable through the Simulation Output node.

## What persists

- Store per-point velocity, age and similar data as named attributes on the geometry item (Store Named Attribute) rather than as separate items. Anonymous attributes (for example from Capture Attribute) are not propagated unless explicitly stored in the simulation state.
- Single values (frame counter, accumulated time) can be items of their own.

## Delta Time

Delta Time is the time in seconds between frames, essentially the inverse of the render frame rate. Connect it to rate-dependent logic so playback stays consistent when the frame rate changes.

## Gotchas

- Links from outside into the zone are re-evaluated each step at the given frame; they are not stored state. Put values that must persist through the Simulation Output.
- Removing an item removes its sockets; check downstream links.
- Large geometry items make caches big; keep only the attributes you need.

## Verify

Play from the start frame: the state accumulates (for example a counter item increases by one per frame).

## Checked

2026-10-27, against the Blender 5.3 manual (branch blender-v5.3-release). Confirmed on the Simulation Zone and Simulation Nodes index pages: Simulation State panel, initial evaluation of inputs, outside-to-inside links re-evaluated every step, Delta Time definition, anonymous attribute rule. Removed unconfirmed claims: list of item types, per-item Attribute Domain, first-frame Delta Time of zero and reset behaviour.

Method: documentation only; no commands were run.
