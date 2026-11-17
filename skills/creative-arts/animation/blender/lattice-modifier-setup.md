---
id: creative-arts.animation.blender.lattice-modifier-setup
name: lattice-modifier-setup
category: creative-arts
field: animation
product: blender
tags: [blender, lattice, lattice-modifier, modifiers, deform, squash-stretch, lattice-deform]
level: practitioner
status: verified
description: "Deform one or many Blender objects with a Lattice modifier: Lattice Deform parenting, Object/Vertex Group/Strength fields, particle stack order, why lattices help."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/deform/lattice.html
  - https://docs.blender.org/manual/en/latest/animation/lattice.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# lattice-modifier-setup

Goal: a coarse control cage that bends or squashes any number of objects at once, with animatable controls. Lattice object properties (resolution, interpolation): `creative-arts.animation.blender.empties-lattices`.

## What the modifier does

It deforms the base object by the shape of a Lattice object. Targets can be meshes, curves, surfaces, text, lattices and even particles.

- **Object**: the Lattice object to deform with.
- **Vertex Group** (+ Invert): optional, limits the effect to part of the base mesh.
- **Strength**: blends between the original and deformed positions.
- **Quick add**: parent selected objects to the lattice using the *Lattice Deform* option of Object > Parent, which adds the modifier to them.

## Why use a lattice

From the manual:
- It deforms large portions of dense meshes efficiently.
- It gives smooth deformations that are hard to make by hand.
- Several objects can share one lattice and be edited together.
- It is non-destructive, like all modifiers.
- A lattice does not affect the surface's texture coordinates.

## Particles

When deforming particles, order in the stack matters: place the Lattice modifier after the Particle System modifier.

## Animating

Edit lattice points in Edit Mode, or animate through other means (shape keys on the lattice, hooks, parenting the lattice to a bone); these are standard Blender techniques but are not documented on the modifier page, so test them in your own file.

## Verify

With the lattice in its rest state the targets look identical to having no modifier. Moving lattice points deforms all linked targets together.

## Checked

Date: 2026-10-27. Documentation release: Blender manual, 5.2 release branch (Lattice modifier page). Confirmed: fields, Lattice Deform parenting shortcut, supported target types, particle stack-order note, benefits list. Removed unconfirmed fitting steps, resolution figures, keyboard shortcuts, export and stack-order advice.

Run check, 2026-11-01, Blender 4.5.14 LTS headless: Lattice modifier with Python: properties Object, Vertex Group (Invert) and Strength; an undeformed lattice left a 10x10 grid unchanged; moving one lattice point deformed the grid, and Strength 1.0, 0.5 and 0 gave maximum displacements of 0.2397, 0.1198 and 0; Object > Parent > Lattice Deform (parent_set type Lattice) set the lattice as parent and added a Lattice modifier pointing at it. Not run: particle stack order, the texture-coordinate statement and animation techniques (documentation only; the page itself says to test them).

Method: manual text confirmed from documentation; behaviour run headless in Blender 4.5.14.
