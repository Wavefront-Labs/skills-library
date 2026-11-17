---
id: creative-arts.animation.blender.simulation-skip
name: simulation-skip
category: creative-arts
field: animation
product: blender
tags: [blender, simulation-skip, skip-input, simulation-nodes, geometry-nodes, simulation-pause]
level: advanced
status: docs-checked
description: "Pause and gate geometry node simulations with the Simulation Output Skip input: holding state, starting late, toggling from properties, and how caching treats skipped frames."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/simulation/simulation_zone.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# simulation-skip

Goal: freeze a simulation for some frames, or start it at frame 50 without moving the scene start.

## Skip input

The simulation zone has a **Skip** input. The manual describes it as forwarding the output of the Simulation Input node directly to the Output node and ignoring the nodes inside the zone.

## Patterns

- **Start late**: `Scene Time.Frame` → Compare (Less Than, B 50) → Skip. Before frame 50 the state stays at its initial value.
- **Pause window**: Skip = frame in [80, 100] (two compares + Boolean AND).
- **User toggle**: expose a Boolean group input "Paused" on the modifier and connect it to Skip; animators key it.
- **Stop when settled**: compute a boolean from the state (e.g. max speed < threshold) in the previous frame and store it as a state item; feed into Skip.

## Caching

The simulation is cached during playback and evaluated only while the frame changes; the manual does not describe how skipped frames are cached, so check a short test.

## Gotchas

- With Skip true the zone forwards its Input directly to its Output, so logic inside (including Delta Time integration) does not run.
- Delta Time is the time in seconds between frames (the inverse of the frame rate); it does not grow to cover skipped frames.

## Verify

With Skip driven by frame < 50, play: nothing moves until 50, then motion starts from the initial state; toggling the Paused input holds the current state.

## Checked

2026-10-27, against the Blender 5.3 manual (branch blender-v5.3-release). Confirmed on the Simulation Zone page: the Skip input forwards the Simulation Input output to the Output node and ignores the zone contents; Delta Time is the time between frames; caching behaviour. Removed unconfirmed claims about cache entries for skipped frames, node placement of Skip, and catch-up behaviour beyond the documented Delta Time definition.

Method: documentation only; no commands were run.
