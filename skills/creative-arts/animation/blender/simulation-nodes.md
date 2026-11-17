---
id: creative-arts.animation.blender.simulation-nodes
name: simulation-nodes
category: creative-arts
field: animation
product: blender
tags: [blender, simulation-zone, simulation-nodes, repeat-zone, simulation-zones, geometry-nodes, gn, particles-gn, procedural-sim, delta-time, zones]
level: advanced
status: docs-checked
description: "Simulation and Repeat zones in Blender Geometry Nodes: zone mechanics, Delta Time, Skip, caching and baking, iteration, and state-passing patterns."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/simulation/simulation_zone.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/utilities/repeat_zone.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/geometry/operations/bake.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# simulation-nodes

Goal: build stateful procedural effects (particles, growth, erosion, flocking, springs) in Geometry Nodes, and iterate without time with Repeat zones.

## Simulation zone mechanics

Adding a simulation adds a **Simulation Input** and a **Simulation Output** node, which define the zone between them. Simulation zones let the result of one frame influence the next, so simple rules can build complex behaviour over time.

- Values connected to the Simulation Input from outside are evaluated **once**, at the beginning of the simulation, then passed on as the simulation state and output. Other nodes can be linked into the zone from outside; those are re-evaluated every step from their value at the given frame.
- **No link may go from inside the zone to the outside.** The only way to read the result is the Simulation Output node. This is also what allows sub-frame interpolation for motion blur.
- The zone works only in the **Modifier** context, not the Tool context.
- The simulation is tied to the animation system: it is evaluated only while the frame changes, and is cached like Blender's other physics simulations.
- **Delta Time** is the time in seconds between frames (the inverse of the render frame rate). Multiply rate-based setups (velocity, gravity) by it so playback stays consistent when the frame rate changes.
- **Skip** forwards the Simulation Input directly to the Output and ignores the nodes in the zone (a way to pause the simulation).
- More state items are added by dragging a socket onto the blank socket, or in the *Simulation State* panel. Rename an item with `Ctrl-LMB` on its name or in the node's Properties panel.
- **Anonymous attributes are not propagated** by simulation nodes unless they are explicitly stored in the simulation state. Store per-point state in named attributes or as state items.

## Minimal particle pattern

State geometry holds the live points. Each frame inside the zone: join newly emitted points to the incoming state, move points by their velocity times Delta Time, update velocity (for example add gravity times Delta Time), age points, and delete those past their lifetime; output the result and instance geometry on the points outside the zone. Change the random seed per frame (for example from the current frame) so each emission batch differs.

Other patterns use the same loop: flocking (compare each point with nearby points, for example with the Index of Nearest node, which the manual shows driving sphere-based simulations), growth (extend a curve each frame), and erosion (displace a mesh each frame).

## Repeat zone

A **Repeat Zone** executes a set of nodes multiple times within one evaluation, with no time involved. It has an input node on the left, an output node on the right and an orange area between them.

- The first time the zone executes it evaluates its inputs and forwards them to the inner nodes; those write to the Output node to provide the next iteration's inputs and, after the last iteration, the result.
- Inputs from nodes outside the zone are the same in every iteration. As with simulation zones, inner nodes cannot send outputs to nodes outside the zone.
- **Iterations** is the number of times to execute the zone; the **Iteration** socket gives the current index, starting from 0.
- Extra inputs are added by connecting to the blank input or in the *Repeat Items* list (Sidebar > Node > Properties).
- **Inspection Index** chooses which iteration is shown in socket inspection and the Viewer node.
- The manual's example builds a pyramid with a configurable number of levels: each iteration creates a cube, positions it and joins it with the previous result.
- Repeat zones inside a simulation step suit relaxation-style iteration per frame; heavy bodies times many iterations multiply evaluation time.

## Caching and baking

- The simulation is cached automatically during playback; the valid cache shows as a strong purple line in the Timeline, so earlier frames can be inspected quickly. If only the current frame matters, opt out of caching to save memory.
- To send to a render farm, bake to disk so frames can be rendered in non-sequential order. Baking bakes all simulations in all modifiers of the selected objects. The UI is in Physics > Simulation Nodes.
- The **Bake** node stores intermediate geometry for performance. *Bake Mode* is Animation (scene frame range by default, or a Custom Range with Start and End) or Still (current frame); *Bake Target* is Inherit from Modifier (default), Packed (inside the .blend) or Disk, with an optional Custom Path. That Bake Path is also used for simulation zones. Baked data is not an interchange format and may not be readable by another Blender version.

## Gotchas

- Bake before rendering on a farm or in non-sequential order; the manual says baking is what allows frames to be rendered out of order.
- Anonymous attributes vanish between frames unless stored in the simulation state.

## Verify

- Playing from the start frame: particles emit, fall under gravity scaled by Delta Time, and die at their lifetime; changing fps does not change motion in world time.
- Scrubbing backwards shows cached frames, and the Timeline shows the purple cache line.
- Repeat zone with Iterations 0 passes geometry through unchanged; with N it applies N steps.

## Checked

2026-11-09. Confirmed against the Blender manual Simulation Zone, Repeat Zone and Bake Node pages (raw RST, all read in full): zone semantics, the no-outward-link rule, Modifier-only context, anonymous attribute note, Delta Time, Skip, State panel, cache line, bake-to-disk and bake-all behaviour, Repeat Iterations / Iteration / Repeat Items / Inspection Index, Bake node modes, targets and shared path. Removed: version gates (3.6+, 4.1+, 4.3+), For Each Element zone, Physics-tab Frame Start/End and "Calculate to Frame" details, point-count and performance figures, the Delta Time zero-on-first-frame claim, undo and nested-cache claims, node-level recipe details, the play-every-frame advice and the "state cannot be a field" error wording.
Method: documentation only; no commands were run.
