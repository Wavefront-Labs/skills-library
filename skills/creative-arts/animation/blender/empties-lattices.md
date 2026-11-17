---
id: creative-arts.animation.blender.empties-lattices
name: empties-lattices
category: creative-arts
field: animation
product: blender
tags: [blender, empties, empty-object, lattice, lattice-modifier, image-empty, reference-images, controllers, null-objects, cage-deform, ffd, hook]
level: practitioner
status: docs-checked
description: "Empties as controllers, references and instance hosts; lattices as deformation cages: display types, image empties, lattice resolution and interpolation, animating."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/empties.html
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/deform/lattice.html
  - https://docs.blender.org/manual/en/latest/modeling/modifiers/deform/hooks.html
licence: Apache-2.0
version: 5
updated: 2026-11-17
aliases: []
---

# empties-lattices

Goal: know the two "non-rendering" object types every rig, layout and FX setup depends on, and use them without the common traps.

## Empties

Add an empty (Add menu, Empty) in one of the display types Plain Axes, Arrows, Single Arrow, Circle, Cube, Sphere, Cone or Image. Object Data tab: *Display As* and *Size* (Size controls how large the empty is displayed and does not change its scale; applying scale with Ctrl A folds the scale into Size).

Uses:
- **Controllers and targets:** IK targets outside an armature, Track To / Damped Track targets for cameras and lights, Copy Location references, driver sources (an empty's location driving a shape key is the simplest slider).
- **Hierarchy roots:** one empty per prop group; animate the root, keep the parts clean (`creative-arts.animation.blender.parenting-relations`).
- **Array offset:** an empty can offset an Array modifier so a single object controls a complex deformation.
- **Other uses listed by the manual:** placeholders, rigging controls, DOF distances and reference images.
- **Collection instances:** empties host collection instances (see `creative-arts.animation.blender.object-instancing`).
- **Texture coordinate objects:** an empty can be used as the Object in a Texture Coordinate node for a movable projection space (practice).
- **Force-field hosts:** force fields are empties with physics (see `creative-arts.animation.blender.particles-fx`).
- **Hooks:** a Hook modifier can be driven by an empty (see the Hook modifier page).

Image empties:
- Image empties display an image regardless of the 3D display mode, for blueprints or character sheets to model from. Properties (Object Data, Empty panel): *Offset* X/Y (1.0 is the image width/height; X=0.5, Y=0.5 puts the origin at the image centre), *Depth* (Default, Front, Back), *Side* (Both, Front, Back), *Show in* Orthographic / Perspective / Only Axis Aligned, and *Opacity*.
- The manual tips: for modelling, set Depth to Front with a low Opacity; disable Show in Perspective so reference images do not get in the way; use *Side* to show front and back photos only from the correct side.
- Set the empty's size so the subject matches real-world scale before modelling (practice).

An empty is a single coordinate point with no geometry and cannot be rendered.

## Lattices

A lattice is a 3D grid of control points; objects inside it deform smoothly when the grid is deformed via a **Lattice modifier** (or *Parent → Lattice Deform*).

Setup:
1. `Shift A → Lattice`. Object Data: *Points* U/V/W (1 to 64 per axis in the Python API; more points give finer control but more to manage), *Interpolation Type* per axis (Linear, Cardinal, Catmull-Rom, B-Spline). *Outside* takes only the vertices on the lattice surface into account. Scale and move the lattice **object** in Object Mode to fit around the target.
2. On the target: Modifier → *Lattice*, pick the lattice, optional *Vertex Group* to limit, *Strength*. Alternatively parent the targets to the lattice with the *Lattice Deform* option, which adds the modifier automatically.
3. `Tab` into the lattice and move points with the usual transform tools and proportional editing. Apply the modifier to bake the result when done.

Uses:
- Squash/stretch and cartoon bulges on props and whole characters (lattice parented to the root bone, points keyframed or driven — "lattice as secondary rig").
- Fixing proportions after rigging (practice).
- Reusable deformation: multiple objects can use the same lattice, so editing it edits them all at once (from the manual).
- A lattice does not affect the texture coordinates of the mesh's surface, and like all modifiers it is non-destructive (from the manual).

Animating a lattice (practice): keyframe the lattice object, or use shape keys or hooks on the lattice; check the manual's shape key and hook pages for the exact steps.

Multiple lattices: stack Lattice modifiers; the stack evaluates top-down, so a lattice after the Armature modifier deforms the posed character. When deforming particles the manual says the Lattice modifier must come after the Particle System modifier.

## Gotchas

- Make the lattice larger than the object with a margin (practice).
- Applying object scale with Ctrl A to an object inside a lattice has the same effect as scaling the lattice in Edit Mode, and deforms the object.
- Exporters may not carry the Lattice modifier; apply it before export (practice, check your exporter).
- Very small empties are easy to lose in big scenes; search the Outliner (practice).
- An opaque image empty with Depth Front hides the model; use a low Opacity (the manual's tip).

## Verify

- Image empty: the reference lines up with a known-size object at the agreed scale.
- Lattice: moving one corner point in Edit mode deforms the nearby part of the target; `Tab` out and apply, and the mesh keeps the shape.
- After applying the modifier, the mesh matches the viewport.

## Checked

2026-10-27, Blender manual, branch blender-v5.2-release (raw RST, projects.blender.org/blender/blender-manual). Confirmed against modeling/empties.rst (display types, Display As, Size, Apply Scale behaviour, image empty properties and tips, uses), animation/lattice.rst and modeling/modifiers/deform/lattice.rst (points, interpolation, Outside, Lattice Deform parenting, particle ordering note, multi-object use). Removed unconfirmed claims: Background/Reference add options, drag-and-drop, FBX empty export, 2 to 4 resolution, default interpolation, 5 percent example, Apply as Shape Key assertions.

Method: documentation only; no commands were run.
