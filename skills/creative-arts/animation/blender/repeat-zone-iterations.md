---
id: creative-arts.animation.blender.repeat-zone-iterations
name: repeat-zone-iterations
category: creative-arts
field: animation
product: blender
tags: [blender, repeat-zone-iterations, repeat-zone, iterations, geometry-nodes, procedural]
level: advanced
status: verified
description: "Use the Repeat Zone in geometry nodes for iterative algorithms: iteration count, repeat items, accumulation patterns like growth and erosion, and performance limits."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/utilities/repeat_zone.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# repeat-zone-iterations

Goal: loops inside one evaluation (not over time): repeated extrusion, relaxation, diffusion, recursive subdivision.

## Basics

The Repeat Zone is in the Utilities section of the node menu. Its input node has an **Iterations** integer; the zone body runs that many times, each iteration's output feeding the next iteration's input, and the output after the last iteration is the result. The *Iteration* socket gives the current iteration index, starting from 0. Add items by dragging a link into the blank socket or with the *Repeat Items* list (sidebar Node tab, Properties); rename with `Ctrl-LMB`.

Nodes inside can take values from outside the zone (the same in every iteration), but nothing inside can link to nodes outside.

## Patterns

- **Growth**: geometry item → Extrude Mesh (top faces) → Scale Elements → back to output: 10 iterations = 10 segments.
- **Relaxation / smoothing**: Set Position to the average of neighbour positions (the Blur Attribute node has its own *Iterations* and *Weight* inputs and may do the job without a zone).
- **Accumulation**: a Float item `sum` += value per iteration; use the *Iteration* socket for the index.
- **Erosion/diffusion on a grid**: store height as attribute, update from neighbours via Sample Index / Evaluate at Index each iteration.

## Iterations from data

*Iterations* is an input, so it can come from a group input or a computed integer.

## Performance

- The body runs once per iteration, so cost grows with the iteration count.
- Operations that do not change per iteration go outside the zone; their values reach the zone unchanged.
- Prefer built-in nodes that already iterate (Blur Attribute *Iterations*) when they fit.

## Gotchas

- Repeat zones are not time: for frame-to-frame state use the Simulation Zone.
- Fields are evaluated in the context of the node they feed, so capture a value (Capture Attribute) if later iterations must see the original (see `gn-fields-attributes`).

## Verify

Drive iterations from a slider: geometry or values change step by step per added iteration. Set the zone's *Inspection Index* to view a given iteration in socket inspection and the Viewer; the Node Timings overlay (node editor overlays popover) shows how long the nodes took.

## Checked

2026-10-27, against the Blender 5.3 manual (branch blender-v5.3-release). Confirmed on the Repeat Zone, Blur Attribute and Inspection pages: Iterations and Iteration sockets (index from 0), Repeat Items list, Inspection Index, outside links allowed but not outward, Node Timings overlay location. Removed unconfirmed claims: version note, performance figures and Iterations 0 behaviour.

Run check, 2026-11-01, Blender 4.5.14 LTS headless (bpy, factory settings): Repeat Input has Iterations (default 1) and an Iteration output; a repeat_items list; a Float item summing the Iteration socket over 5 iterations gave 10 (0+1+2+3+4), confirming the index starts at 0 and each output feeds the next input. Blur Attribute has Value, Iterations and Weight inputs. Not run (confirmed from the manual only): menu location, rule that nothing inside links outside, the growth and erosion patterns, performance remarks.

Method: manual text confirmed from documentation; the listed behaviour run headless in Blender 4.5.14.
