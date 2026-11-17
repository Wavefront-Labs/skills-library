---
id: creative-arts.animation.blender.empty-controllers
name: empty-controllers
category: creative-arts
field: animation
product: blender
tags: [blender, empties, empty-controller, empty-target, empty-helper, constraints, drivers, hooks]
level: practitioner
status: docs-checked
description: "Use Blender empties as rig-free controllers: constraint targets (Track To, Damped Track), hook controllers, driver inputs, texture coordinates and modifier offsets."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/empties.html
  - https://docs.blender.org/manual/en/latest/animation/constraints/tracking/track_to.html
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/deform/hooks.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/vertex/hooks.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# empty-controllers

Goal: control props, cameras, modifiers and shaders with lightweight empties instead of full armatures.

## Patterns

- **Look-at target**: camera or eye with *Track To* (or *Damped Track*) targeting an empty; animate the empty. Pick the *Track Axis* (the owner's local axis that points at the target; a negative axis points away) and a different *Up* axis.
- **Hook controls**: Edit mode, select verts, `Ctrl H` (*Vertex → Hooks → Hook to New Object*) creates an empty at the average position of the selected vertices and a Hook modifier; animate it to deform curves/meshes (cables, flag corners).
- **Modifier origins**: Array *Object Offset* and Mirror *Mirror Object* can use an empty, so moving one object controls the effect.
- **Texture space**: the Texture Coordinate node's *Object* output with an empty as the object (the manual notes this is often used with an empty) — move and rotate projections.
- **Driver inputs**: a driver variable of type *Transform Channel* reading an empty's location or rotation (for example a slider empty limited by *Limit Location*).
- **Booleans/lattice parent**: parent cutters or a lattice to an empty for one-handle animation.

## Making them animator-friendly

- *Limit Location/Rotation* constraints with *Affect Transform* to clamp ranges.
- Lock unused channels (padlock icons in N panel).
- Custom properties on the empty for switches (visibility, colour index).
- Circle/Arrows display, sized and coloured (see empty-display-types).

## Gotchas

- Hook modifier (Edit Mode): *Reset* recalculates and clears the hook's offset transform, and *Recenter* sets the hook centre to the 3D cursor.

## Verify

Animate only empties; the dependent objects follow correctly through the full frame range with no dependency cycle warnings in the console.

## Checked

2026-10-27, Blender manual 5.2 (blender-v5.2-release RST: Empties, Track To, Hooks, Limit Location, Texture Coordinate, Drivers and Array pages). Confirmed: Track To Track Axis and Up semantics (negative axis points away); Hook to New Object on Ctrl H; Hook Reset and Recenter; Limit Location Affect Transform; Texture Coordinate Object output often used with an empty; driver variable type Transform Channel; empties as Array offset and constraint targets; Mirror Object. Removed as unconfirmed: the camera axis recommendation, the Warp, Cast and Simple Deform claims, force-field placement and the engine-export bake claim.

Method: documentation only; no commands were run.
