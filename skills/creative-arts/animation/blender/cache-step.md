---
id: creative-arts.animation.blender.cache-step
name: cache-step
category: creative-arts
field: animation
product: blender
tags: [blender, physics-bake, point-cache, cache-step, cache-frame-range]
level: practitioner
status: docs-checked
description: "Set Blender point cache Start/End frames and Cache Step for lighter bakes, with notes on positive frames, interpolated in-between frames and which systems show the options."
sources:
  - https://docs.blender.org/manual/en/latest/physics/baking.html
  - https://docs.blender.org/manual/en/latest/physics/particles/emitter/cache.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# cache-step

## Settings (Cache panel of the physics system)

- **Start / End** (labelled Simulation Start and End in some panels): frames to simulate and cache. The manual says the simulation is only calculated for positive frames between Start and End, whether you bake or not, so a simulation longer than the default range needs a later End frame.
- **Cache Step**: interval for storing simulation data. Per the manual, some systems (such as particles) store positions only every nth frame and interpolate the in-between frames; a step above one gives a smaller cache, but the result may differ from the original simulation.
- In the UI source, the Cache Step field is hidden for Cloth, Dynamic Paint and Rigid Body caches, and the Simulation Start field is hidden for particle systems and Dynamic Paint.

## Hints from the manual

- To fill the cache, start playback on or before the frame the simulation starts.
- Each physics system writes each frame to the cache when the animation plays.
- The cache is cleared automatically on many (not all) changes; delete it manually if needed, for example after changing a force field.
- After baking, the cache is protected from changes. Delete Bake marks the baked cache as temporary.
- Bake from Object Mode. Calculate to Frame bakes only up to the current frame, limited by the End frame.

## Gotchas

- Interpolated in-between frames differ from the true simulation, so keep Cache Step at 1 for fast or colliding particles and compare a fast particle's path against step 1 (practical advice).
- The simulation does not run for negative frames, so a pre-roll that starts before frame 0 is not possible with these settings.
- If you cannot write to the cache folder (for example a very long path) caching does not take place.

## Verify

The cache info line shows the expected frame range, and with a step above 1 a fast-moving particle path matches the step 1 result closely enough for the shot.

## Checked

Date 2026-10-27. Blender manual 5.2 (blender-v5.2-release RST) and properties_physics_common.py on main.
Confirmed: positive-frames-only rule, Start/End, Cache Step meaning and interpolation, hints list, Delete Bake and Calculate to Frame meanings; which cache types hide Cache Step and Simulation Start.
Removed as unconfirmed: the negative start-frame pre-roll pattern (it contradicts the manual), the claim that cloth quality is set per frame via Quality Steps instead, "step 2 to 5 saves disk" figures, and the claim that the sim freezes when the scene runs past cache end.
Method: documentation only; no commands were run.
