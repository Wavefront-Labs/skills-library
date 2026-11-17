---
id: creative-arts.animation.blender.particle-render-objects
name: particle-render-objects
category: creative-arts
field: animation
product: blender
tags: [blender, particles, particle-render-objects, render-as-collection, render-as-object, instancing]
level: practitioner
status: docs-checked
description: "Render Blender particles as objects or collections: Render As None/Halo/Path/Object/Collection, Whole Collection, Pick Random, Use Count and Make Instances Real."
sources:
  - https://docs.blender.org/manual/en/5.2/physics/particles/emitter/render.html
  - https://docs.blender.org/manual/en/5.2/scene_layout/object/editing/apply.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# particle-render-objects

## Render As (Particle System > Render)

- **None**: particles are not rendered (useful when particles only duplicate objects). **Halo**: glowing dots, not real lights. **Path**: needs a Hair particle system or Keyed particles; options B-Spline, Steps (a power of 2: 0 gives 1 subdivision, 3 gives 8), and Timing for hair. **Object** and **Collection** instance geometry.
- Cycles supports only the Object and Collection render types.
- Common: **Material** (which of the object's materials shades the particles), **Coordinate System** (use another object's coordinates for the birth of particles), **Show Emitter** (when off the emitter mesh is not rendered).

## Object

- **Instance Object**: the object instanced in place of each particle.
- **Global Coordinates** (use the object's global coordinates), **Object Rotation**, **Object Scale** (use the object's rotation and size).

## Collection

- **Instance Collection**; **Whole Collection** (the whole collection at once in place of each particle), **Pick Random** (one random object per particle), with Global Coordinates, Object Rotation and Object Scale as above.
- **Use Count**: use objects several times in the same collection; the list view sets the order and number of repeats (add and remove entries with the plus and minus buttons).
- To face instances along their direction of travel, use the Rotation panel: Orientation Axis Velocity / Hair (see particle-velocity).

## Extra

**Parents** renders parent particles too when children are used (by default parents are not rendered). **Unborn** and **Dead** render particles before birth or after death.

## Gotchas

- Scale and Scale Randomness are listed in the manual without a description; test their effect on your instances.

## Make instances real

Object > Apply > **Make Instances Real** creates a new object for each instance.

## Verify

Render shows instances with the expected variety and orientation.

## Checked

Date: 2026-10-27. Documentation: Blender 5.2 manual (Particle Render panel, Object > Apply). Confirmed: Render As list and per-type options, Cycles support note, Use Count, Extra options, Make Instances Real menu entry. Corrected: Halo is described only as a glowing-dot render type, and Cycles supports Object and Collection only (the EEVEE claim was removed); Scale/Scale Randomness are undocumented. Removed as unconfirmed: hair-plus-collection scatter recipe, Advanced > Rotation, origin-and-rotation advice, memory-sharing note, and instance-source visibility advice.
Method: documentation only; no commands were run.
