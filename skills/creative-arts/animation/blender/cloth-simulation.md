---
id: creative-arts.animation.blender.cloth-simulation
name: cloth-simulation
category: creative-arts
field: animation
product: blender
tags: [blender, cloth, cloth-simulation, physics, pinning, vertex-group, collision, bake, cache, jitter, stiffness, quality-steps, collision-margin, cel, on-model]
level: advanced
status: docs-checked
description: "Blender cloth sim for a stylized cel show: when to sim vs hand-key, modifier/collision/pin settings, baking, killing jitter, keeping cloth on-model and outline-friendly."
sources:
  - https://docs.blender.org/manual/en/latest/physics/cloth/introduction.html
  - https://docs.blender.org/manual/en/latest/physics/cloth/settings/index.html
  - https://docs.blender.org/manual/en/latest/physics/cloth/settings/cache.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# SKILL: Cloth simulation for a stylized cel show (Blender)

**Goal:** get a cape, skirt, scarf or coat-tail on a production character to move with believable weight while staying *on-model*: readable, outline-friendly, and not a noisy real-cloth jitter-fest. The simulation is a tool for motion, not realism, and most of this skill is about *restraining* it.

This is the dynamic counterpart to `cloth-garment-modeling.md`, which builds the garment as static geometry. That static garment is the **input** here: sim a well-built, properly weighted garment, never a raw cylinder.

## Decide first: sim, hand-key, or model the folds

Simulation is the expensive option on a reused-asset show. Before baking anything:

- **Model or hand-key it** when the cloth is tight, motion is subtle, or the shot is short. A skirt with a few swing bones (see `hair-simulation.md` for the bone-chain technique) is cheaper, art-directable and repeatable across shots. The manual's own guidance is the same in spirit: Soft Body suits simple fabric and jiggle, while Cloth has a solver designed for fabric.
- **Simulate** when the cloth is loose and large and a bone rig cannot carry the secondary folds.
- **Hybrid:** drive the gross shape with swing bones and sim only a low-poly cloth proxy for the trailing edge. The manual notes that a Cloth modifier on a low-poly mesh can be followed by a Subdivision Surface modifier to improve quality without a big increase in sim time.

## The cloth modifier: settings that matter

Add **Physics > Cloth**; a Cloth modifier appears in the stack and the settings live in the Physics tab.

- **Presets** (top of the Cloth panel): start from the closest fabric preset, then stiffen.
- **Quality Steps**: simulation steps per frame; the first dial to raise when cloth tunnels or explodes (higher is better but slower).
- **Speed Multiplier**: how fast time progresses in the sim.
- **Stiffness** (Physical Properties): **Tension** and **Compression** resist stretching and compression, **Shear** resists shearing, **Bending** is the wrinkle coefficient: higher makes more large folds, which is the key stylization dial for a clean cel line.
- **Damping** (Tension, Compression, Shear, Bending): raise to settle motion fast and kill flutter.
- **Vertex Mass** and **Air Viscosity**: heavier mass for statelier swing; air viscosity slows falling cloth.
- **Internal Springs** (on a closed 3D shape): make the mesh behave more like a Soft Body so a bell shape keeps its volume. **Pressure** is for balloon-like objects (see `cloth-pressure-internal-springs`).

## Pinning via vertex groups

1. Create a vertex group (for example `cloth_pin`) and weight the fixed band (collar, waistband, shoulder seam), fading into the free cloth for a softer drape; weight controls how strongly each vertex is pinned.
2. Physics > Cloth > **Shape > Pin Group** = that group; **Stiffness** is the target-position stiffness.
3. Pinned vertices follow whatever deforms the mesh before Cloth in the stack, so keep the **Armature** modifier above Cloth and weight the pinned band to the body bones (`rigging.md`). Order: Armature, Cloth, then Subdivision Surface, Solidify and outline.
4. **Sewing** (Shape) needs extra loose edges in the mesh; otherwise the pin group carries attachment. **Dynamic Mesh** lets unpinned cloth squash and stretch with the character via shape keys or modifiers above Cloth. Cloth has no Goal setting; use pinning and stiffness to hold it near the modelled shape.

## Collision setup

- **On the body:** Physics > **Collision**. In Soft Body and Cloth: **Thickness Outer** and **Inner** (padding along the face normal), **Damping**, **Friction**. Padding that is too large makes cloth float off the body; too small risks tunnelling. Tune at real character scale.
- Collide against a simplified, smoothed copy of the body rather than the render mesh.
- The Collision modifier must come after shape keys and Armature on the collider.
- **On the cloth:** Physics > Cloth > **Collisions**: **Quality**, **Object Collisions > Distance**, **Impulse Clamping**, **Collision Collection**, and **Self-Collisions** (Friction, Distance, Impulse Clamping) for a skirt that folds on itself. Details in `cloth-collisions`.
- If elbows poke through a cape, the manual's order of attack is: raise Distance (fast but less accurate), raise cloth Quality Steps and collision Quality, then edit the baked result.

## Caching and baking

Cloth results live in the **Physics > Cloth Cache** panel.

- Set **Start** and **End** to cover the shot, with lead-in frames before frame 1 so the cloth settles; jumping far ahead before the earlier frames are computed may show an inaccurate shape.
- Cache settings match other dynamic systems (see Particle Cache). A **Disk Cache** with a per-shot folder avoids losing the sim when the file reloads; if the file is not saved the cache is only in memory.
- **Bake** to compute and **Delete Bake** to clear. Start and End cannot change without clearing the bake.
- Moving or editing the cloth object after simulating requires clearing the cache. The manual notes that editing a cached sim in Edit Mode is currently not working.
- A cache is stored per subdivision level, so use the same level for viewport and render.

## Reducing jitter and keeping it on-model

- **Jitter:** raise damping (Bending and Shear first), then Quality Steps; collision distances that fight each other also cause buzzing.
- **Too many fine wrinkles for a cel line:** raise Bending stiffness and damping and use a lower-poly cloth, smoothing it after the Cloth modifier (the manual says to smooth after Cloth computes its shape).
- **Off-model drift:** raise pin Stiffness, add pinned area, or shorten the free cloth.
- **Outline friendliness:** the inverted-hull or Solidify outline (`cel-shading.md`) sits after Cloth and any smoothing; stress it on the fastest frames.

## Cross-links

- Static garment construction: `cloth-garment-modeling.md`.
- Bone-chain alternative for skirts and scarves: `hair-simulation.md`.
- Body skeleton and swing bones: `rigging.md`.
- Cel outline: `cel-shading.md`.
- Running a bake unattended: `blendercraft-headless.md`.

## Verify

1. Scrub to frame 1 after the lead-in frames: cloth is hanging at rest.
2. Bake a hard whip-turn: no poke-through, no cloth through itself, no explosion; if it fails, raise Quality Steps and collision Quality before changing distances.
3. Hold the character still: the cloth settles and stops.
4. Compare the simulated silhouette against the modelled garment at a quiet pose.
5. With the outline on, scrub the fastest frames for double lines at creases.
6. Free and re-bake with identical settings and compare the result.

## Checked

Date: 2026-10-27. Blender 5.2 manual (blender-v5.2-release branch). Confirmed: Cloth panel names (Presets, Quality Steps, Speed Multiplier, stiffness and damping fields, Internal Springs, Pressure, Shape Pin Group and Stiffness, Sewing, Dynamic Mesh), Collision panel fields, collider modifier order, cache panel (Physics > Cloth Cache, Start and End, Bake, Delete Bake, per-subdivision-level cache, editing currently not working) and the troubleshooting order. Removed the claim that Cloth has a Goal setting (it does not), the "Quality 5" default, preset names and all numeric tuning values, and the Corrective Smooth and applied-scale claims no doc covers.
Method: documentation only; no commands were run.
