---
id: creative-arts.animation.blender.gn-sampling-nodes
name: gn-sampling-nodes
category: creative-arts
field: animation
product: blender
tags: [blender, geometry-nodes, gn-raycast, geometry-proximity, sample-nearest, gn-sample-index, sample-index, evaluate-at-index, sample-nearest-surface]
level: practitioner
status: verified
description: "Read data across geometries in Geometry Nodes: Raycast (snap to ground), Geometry Proximity, Sample Nearest/Nearest Surface, Sample Index and Evaluate at Index."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/geometry/sample/raycast.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/geometry/sample/geometry_proximity.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/geometry/sample/sample_index.html
  - https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/utilities/field/evaluate_at_index.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# gn-sampling-nodes

Goal: get values from *another* geometry or another element — the step past "fields on my own geometry" (see `gn-fields-attributes`).

## Raycast

- Inputs: **Target Geometry**, **Attribute** to sample at the hit (with an *Interpolation* of Interpolated or Nearest), **Source Position** (field), **Ray Direction** (field), **Ray Length** (maximum distance before "no hit").
- Outputs: Is Hit, Hit Position, Hit Normal, Hit Distance (the Ray Length if no hit), Attribute.
- Snap scattered points to terrain: Set Position = Switch(Is Hit, Hit Position, Position), casting rays downward from above the surface.

## Geometry Proximity

Closest point on the target (*Target Element*: Points, Edges or Faces; Points is usually fastest and the only mode that works on point clouds) returns Position, Distance and Is Valid. Pair Distance with Map Range for falloffs. *Group ID* and *Sample Group ID* restrict matches to the same group.

## Sample Nearest / Sample Nearest Surface

- **Sample Nearest**: index of the nearest element of the chosen *Domain* (mesh and point cloud only) → feed Sample Index. With Sample Index this replicates the old Transfer Attribute nearest behaviour. For nearest within the same geometry, Index of Nearest is the better node.
- **Sample Nearest Surface**: attribute value at the closest point on a mesh surface, interpolated for non-face attributes; loose points and edges are ignored. Has Group ID, Sample Group ID and Is Valid.
- **Sample UV Surface**: reverse UV lookup returning the value at a *Sample UV* coordinate; the UV map should not overlap, otherwise the default value is returned.

## Sample Index / Evaluate at Index

- **Sample Index**: value of a field at a given index *of another geometry* (*Domain*, *Clamp*). With several components on the Point domain it samples the first non-empty one (Mesh, Point Cloud, Curve).
- **Evaluate at Index**: same idea within the *current* geometry context (no geometry socket needed), with a *Domain* setting, e.g. Index - 1 to read the previous element.
- **Evaluate on Domain**: choose when a field is interpolated to another domain.

## Gotchas

- Sample Index without Clamp outputs a default value for invalid indices.
- Sample Nearest only supports point cloud and mesh inputs.
- Heavy static targets can be cached with the Bake node.

## Verify

Viewer node on Hit Distance/Distance shows a sensible gradient; points sit exactly on the terrain in side view.

## Checked

2026-10-27, against the Blender 5.3 manual (branch blender-v5.3-release). Confirmed on the Raycast, Geometry Proximity, Sample Index, Sample Nearest, Sample Nearest Surface, Sample UV Surface, Evaluate at Index and Evaluate on Domain pages: inputs, outputs, domains and clamp behaviour. Removed unconfirmed claims: Raycast default direction, Group ID version gate, instance handling and complexity remarks, curve-hair use of Sample UV Surface.

Run check, 2026-11-01, Blender 4.5.14 LTS headless (bpy, factory settings): Raycast inputs Target Geometry, Attribute, Source Position, Ray Direction, Ray Length with Interpolated or Nearest mapping and outputs Is Hit, Hit Position, Hit Normal, Hit Distance, Attribute; a downward ray hit a Grid at distance 1.0 and an upward ray missed with Hit Distance equal to the Ray Length (5.0). Geometry Proximity targets Points, Edges, Faces with outputs Position, Distance, Is Valid and Group ID inputs; Sample Nearest domains Point, Edge, Face, Face Corner; Sample Nearest Surface and Sample UV Surface sockets as described; Index of Nearest and Evaluate on Domain exist. Sample Index on a 4-point mesh with index 10 returned the default (zero) without Clamp and the last element with Clamp. Not run (confirmed from the manual only): the terrain-snap recipe, point-cloud-only proximity mode, overlapping-UV behaviour, first-non-empty component rule.

Method: manual text confirmed from documentation; the listed behaviour run headless in Blender 4.5.14.
