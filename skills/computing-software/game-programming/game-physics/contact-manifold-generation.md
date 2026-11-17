---
id: computing-software.game-programming.game-physics.contact-manifold-generation
name: contact-manifold-generation
category: computing-software
field: game-programming
product: game-physics
tags: [game-physics, narrow-phase, contact-manifold, sutherland-hodgman, clipping, reference-face, incident-face, contact-points, persistent-manifold, contact-caching, box-box, game-programming]
level: advanced
status: verified
description: "Generate stable multi-point contact manifolds for box stacks: SAT axis choice, reference/incident face clipping, point reduction, and persistent manifolds with feature ids."
sources: ["https://box2d.org/files/ErinCatto_ContactManifolds_GDC2007.pdf", "https://realtimecollisiondetection.net/books/rtcd/", "https://www.gdcvault.com/play/1017646/Physics-for-Game-Programmers-The"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Contact manifold generation

**Goal:** turn "these two shapes overlap" into a small set of contact points (position, normal,
penetration) that lets the solver rest a box flat on the ground without rocking.

## Why one point is not enough
A box resting on a plane with a single deepest-point contact rotates around that point each step,
then the contact jumps to another corner: visible jitter. Faces in contact need 2 points (2D) or up
to 4 points (3D) spanning the contact area.

## Box-box (and convex polyhedra) by clipping
1. **SAT** gives the axis of minimum penetration and whether it came from a face of A, a face of B,
   or an edge-edge pair. Bias toward face axes (e.g. accept a face axis if its penetration is within
   ~5% + small absolute tolerance of the best edge axis, as Box2D-Lite does with `relativeTol = 0.95`, `absoluteTol = 0.01`)
   to avoid flip-flopping between features.
2. **Edge-edge case:** one contact point at the closest points between the two edges.
3. **Face case:** the face of the axis owner is the **reference face**. On the other body pick the
   **incident face**: the face whose normal is most anti-parallel to the reference normal.
4. **Clip** the incident face polygon against the side planes of the reference face
   (Sutherland-Hodgman), one plane at a time.
5. Keep only clipped points below the reference face (`separation = dot(n, p) - d <= 0`); store each
   point's penetration and project onto the reference face if desired.
6. **Reduce** to at most 4 points: keep the deepest, then the farthest from it, then points
   maximizing the contact area.

## Feature ids and persistence
Tag each point with ids of the features that produced it (reference face index, incident vertex or
clip edge). Next frame, match new points to old by id and copy accumulated impulses (warm starting).
Stable ids are what make stacks of 10+ boxes settle.

GJK-based engines (Bullet style) instead build a **persistent manifold** incrementally: add one point
per frame from GJK/EPA, keep up to 4 cached points (`MANIFOLD_CACHE_SIZE 4` in Bullet's `btPersistentManifold`), refresh them using stored local-space positions,
and discard points that drift apart tangentially beyond a threshold or separate along the normal.

## Normal conventions
Pick one convention (e.g. normal points from A to B) and keep it everywhere: SAT, clipping, solver.
A flipped normal shows up as objects being pulled into each other.

## Debugging
Debug-draw every contact point with its normal and penetration each frame; freeze-step the
simulation. Typical bugs: points from the wrong side plane, incident face picked by the wrong sign,
reduction discarding corners.

## Verify
- [ ] Box resting on ground: 4 contact points, stable ids over 1000 frames, no rotation drift.
- [ ] Stack of 10 boxes sleeps within a few seconds with warm starting on.
- [ ] Rotated box edge-on-edge produces 1 point with a sensible normal.
