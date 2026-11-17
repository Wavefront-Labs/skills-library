---
id: creative-arts.animation.blender.make-instances-real
name: make-instances-real
category: creative-arts
field: animation
product: blender
tags: [blender, instancing, make-instances-real, instances-real, realize-instances, export-prep, collection-instance]
level: practitioner
status: verified
description: "Convert Blender instances to real objects with Make Instances Real: Parent and Keep Hierarchy options, shared data, and Geometry Nodes Realize Instances alternatives."
sources:
  - https://docs.blender.org/manual/en/latest/scene_layout/object/editing/apply.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/instances/realize_instances.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# make-instances-real

Goal: turn collection instances, vertex/face instances or particle instances into editable objects — for export, per-copy edits, or baking.

## Object > Apply > Make Instances Real

- Select the instancer (collection-instance empty, emitter with vertex/face instancing, particle emitter).
- Options (redo panel):
  - **Parent**: if *Keep Hierarchy* is off, parents all generated objects to the former instancer; if on, parents the generated objects that are not already parented to their matching instancer or its new copy.
  - **Keep Hierarchy**: preserve parent-child relations inside the instanced data. By default new objects go into the instancer's collection with no hierarchy. The manual suggests enabling both options to get a hierarchy close to the instancing one.
- If the new objects share mesh data, use `Object > Relations > Make Single User` before editing copies independently.

## Geometry Nodes instances

- The manual describes Make Instances Real for direct (vertices or faces) and indirect (particle system) instancing. For Geometry Nodes, the *Realize Instances* node turns instances into real geometry inside the node tree; `Object > Apply > Visual Geometry to Mesh` freezes the evaluated result into a mesh; `Object > Apply > Visual Geometry to Objects` creates new objects from the evaluated geometry while preserving shared data and instancing hierarchies.

## Gotchas

- Tens of thousands of instances (from particles, for example) can slow Blender down significantly; realise only what you must.
- Recursive instancing is only supported to some extent when preserving relationships.

## Verify

Outliner shows the new objects (with hierarchy if kept); Statistics object count rises accordingly; renders match pre-conversion.

## Checked

2026-10-27, Blender manual 5.2 (blender-v5.2-release RST, Apply page, and the Realize Instances node page). Confirmed: Object > Apply > Make Instances Real, its Parent and Keep Hierarchy options and their meanings, the slowdown warning for tens of thousands of instances, Visual Geometry to Mesh and Visual Geometry to Objects, and the Realize Instances node. Removed as unconfirmed: the Shift Ctrl A shortcut, linked-library behaviour, and the animation and particle-frame claims. The description no longer states the shortcut.

Run check, 2026-11-01, Blender 4.5.14 LTS headless (bpy, factory settings): Operator object.duplicates_make_real has use_base_parent and use_hierarchy (Parent and Keep Hierarchy); object.make_dupli_face, object.convert (targets include Mesh) and object.visual_geometry_to_objects exist; Instance on Points of a cube on 3 points then Realize Instances gave 24 vertices and 18 faces; Realize Instances has Selection, Realize All and Depth inputs. Not run (confirmed from the manual only): the option semantics, naming and collection placement of the new objects, performance and recursion remarks.

Method: manual text confirmed from documentation; the listed behaviour run headless in Blender 4.5.14.
