---
id: creative-arts.animation.blender.instance-on-vertices
name: instance-on-vertices
category: creative-arts
field: animation
product: blender
tags: [blender, instancing, instance-on-vertices, verts-instancing, dupliverts, object-instancing, align-to-normal]
level: practitioner
status: docs-checked
description: "Instance child objects on a parent mesh's vertices in Blender (Instancing > Vertices): parenting setup, Align to Vertex Normal, hiding the source, and when to use Geometry Nodes instead."
sources:
  - https://docs.blender.org/manual/en/latest/scene_layout/object/properties/instancing/verts.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/instances/instance_on_points.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# instance-on-vertices

Goal: a copy of an object on every vertex of a mesh — rivets on a panel, lights on a dome — without real geometry.

## Setup

1. Make the parent ("emitter") mesh; its vertices set the positions.
2. Select the object to instance, then the emitter (order matters, emitter active), and parent with `Ctrl-P` > Object.
3. With only the emitter selected: Properties > Object Properties > **Instancing** > *Vertices*.
4. Option **Align to Vertex Normal** rotates every instance by the parent's vertex normals; change the instanced objects' direction axis with the child's *Tracking Axis*.
5. The relative object origin position of parent and child offsets the instanced geometry from each vertex; if placement or rotation looks odd, clear the child's rotation (`Alt-R`), scale (`Alt-S`), location (`Alt-G`) and origin.

## Visibility

- The original child and the parent mesh remain visible in the 3D Viewport, but neither is rendered.
- Several children parented to the emitter are all instanced on each vertex.
- Editing the base object changes every instance. Object Mode scaling of the parent also scales the instances, while scaling it in Edit Mode only changes the distances between them.

## When to switch to Geometry Nodes

*Instance on Points* gives rotation and scale inputs per point, a *Selection* input, *Pick Instances* for choosing among a collection's children, and carries point attributes onto the instance domain. Use vertex instancing for quick arrangements; use Geometry Nodes for art-directed work.

## Gotchas

- Turn the instances into real objects with *Make Instances Real* (`duplicates_make_real`); `Ctrl-J` joins the result into one object if wanted.

## Verify

The viewport shows one copy per vertex; *Make Instances Real* yields one object per vertex.

## Checked

2026-10-27, against the Blender 5.3 manual (branch blender-v5.3-release). Confirmed on the Instancing Vertices page and the Instance on Points node page: parenting order, Align to Vertex Normal and Tracking Axis, origin offset, template display with only render exclusion, Edit versus Object Mode scaling, Make Instances Real, Pick Instances and Selection inputs. Removed unconfirmed claims: Up Axis in Relations, Show Instancer toggles, hidden child, exporter behaviour and Statistics overlay.

Method: documentation only; no commands were run.
