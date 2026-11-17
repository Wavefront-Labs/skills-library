---
id: computing-software.game-programming.game-physics.triangle-mesh-internal-edges
name: triangle-mesh-internal-edges
category: computing-software
field: game-programming
product: game-physics
tags: [game-physics, internal-edges, triangle-mesh-collision, ghost-collisions, game-programming]
level: practitioner
status: verified
description: "Fix ghost collisions on triangle meshes and tile chains: internal edge detection, adjacency info, chain shapes and contact normal correction."
sources: ["https://box2d.org/posts/2020/06/ghost-collisions/", "https://github.com/jrouwe/JoltPhysics", "https://github.com/bulletphysics/bullet3"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Triangle mesh collision and internal edges

**Goal:** stop objects bumping or snagging when sliding across the seam between two coplanar
triangles or tiles (ghost collisions).

## Why it happens
A box sliding over triangle A collides with the shared edge of triangle B. The narrow phase returns
B's *edge* normal (pointing partly against motion) instead of the face normal, so the body hops. Example: a circle of radius 0.5 whose centre is 0.3 m before the
shared vertex of two collinear segments (penetrating 0.01 m) gets a vertex contact normal of (-0.52, 0.85), tilted 31.5 degrees from the true face normal (0, 1); at 0.1 m before it the tilt is 11.5 degrees.

## Fixes
- **Chain/edge shapes with ghost vertices (2D):** Box2D's `b2ChainSegment` stores the adjacent *ghost* vertices and Box2D uses them to prevent internal
  collisions. The algorithm is one-sided (the front is to the right of the first-to-second vertex direction), chains are for static bodies, and an open chain
  needs leading and trailing ghost points. Use a chain for tile-based ground, not separate boxes.
- **Adjacency + edge flags (3D):** precompute per triangle which edges are convex, concave or flat
  (compare adjacent face normals). Reject or correct contact normals that hit a flat/concave edge:
  replace with the triangle face normal. Bullet's `btGenerateInternalEdgeInfo` + `btAdjustInternalEdgeContacts` and Jolt's
  "active edges" (`MeshShapeSettings::mActiveEdgeCosThresholdAngle`, default cos 5 degrees; a concave edge is always inactive; bodies opt in to
  `BodyCreationSettings::mEnhancedInternalEdgeRemoval`, default false) implement this. Jolt notes a threshold that is too small causes ghost collisions with edges
  and one that is too big causes slow depenetration.
- **Voronoi region check:** only accept an edge normal if it lies within the edge's Voronoi region
  of the adjacent faces.

## Content-side mitigations
- Weld vertices so adjacency can be found (unwelded meshes have no shared edges).
- Avoid many tiny triangles on walkable surfaces; merge coplanar tiles into one shape.
- Character controllers: use a capsule, not a box, plus collide-and-slide that projects out the
  ground normal.

## Verify
- Slide a box across a tiled floor at speed in a debug scene with contact normals drawn; no vertical
  impulse spikes at seams.

## Checked (2026-10-22)
- Box2D main `docs/collision.md` ('Ghost collisions', 'Chain segment': ghost vertices, one-sided, counter-clockwise winding) and `types.h` chain comments (static bodies, open chains need leading/trailing ghost points); the `ghost-collisions` post URL answers 200.
- Jolt master `MeshShape.h` (`mActiveEdgeCosThresholdAngle` = cos 5 degrees with the too-small/too-big note, concave edges always inactive, triangles single sided) and `BodyCreationSettings.h` (`mEnhancedInternalEdgeRemoval = false`). Bullet `btInternalEdgeUtility.h` (`btGenerateInternalEdgeInfo`, `btAdjustInternalEdgeContacts`).
- Computed the vertex-normal tilt in Python (circle radius 0.5, centre height 0.49, offsets 0.05/0.1/0.3 m give 5.8/11.5/31.5 degrees).
- The Voronoi-region description and content advice (weld vertices, avoid tiny triangles) are standard technique descriptions and not run; the sliding test in the Verify section is a suggestion.
