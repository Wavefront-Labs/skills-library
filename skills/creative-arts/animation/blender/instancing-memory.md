---
id: creative-arts.animation.blender.instancing-memory
name: instancing-memory
category: creative-arts
field: animation
product: blender
tags: [blender, render-optimization, instancing-memory, instance-memory, object-instancing, geometry-nodes]
level: practitioner
status: draft
description: "Save render memory with instancing: collection instances, geometry nodes instances vs realized geometry, linked duplicates, and checking that the renderer really instanced."
sources:
  - https://docs.blender.org/manual/en/latest/scene_layout/object/properties/instancing/index.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/instances.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# instancing-memory

Goal: thousands of trees, rocks or crowd members without running out of memory.

## What actually instances

| Method | Memory per copy |
|---|---|
| Geometry Nodes Instance on Points (not realized) | Almost none (a transform) |
| Collection instance (Add > Collection Instance) | Almost none |
| Particle system rendering an object/collection | Almost none |
| Linked duplicate (Alt D) | Shares mesh data, but each is a full object (modifiers evaluated per object) |
| Duplicate (Shift D) / Realize Instances | Full copy |

Cycles and EEVEE render true instances with shared geometry. Cycles builds a BVH per unique mesh and references it.

## Keep instances instanced

- In geometry nodes, do not add **Realize Instances** unless you need to edit the result per copy. Apply variation with instance transforms and attributes instead (instance attributes drive material variation through the Attribute node with Instancer type).
- A modifier after instancing on the same object realizes the geometry. Put modifiers on the source object.
- Object modifiers with random seed per copy (displacement) make each copy unique, so memory grows. Use shader variation instead.

## Check

- Viewport Statistics overlay shows objects and triangles. Compare render Mem/Peak before and after converting duplicates to instances.
- Spreadsheet editor: Instances domain count shows instances not yet realized.

## Gotchas

- Instances of objects with heavy subdivision: the subdivided mesh is stored once per source, so it is fine. Adaptive subdivision may dice per instance, which uses more memory.
- Motion blur on many instances adds per-instance transforms per step. Cheap compared with geometry.

## Verify

Convert a forest from Shift D copies to a geometry nodes scatter. Peak render memory should drop by roughly the per-tree mesh size times the number of trees.
