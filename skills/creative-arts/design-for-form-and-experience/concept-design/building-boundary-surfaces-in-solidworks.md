---
id: creative-arts.design-for-form-and-experience.concept-design.building-boundary-surfaces-in-solidworks
name: building-boundary-surfaces-in-solidworks
category: creative-arts
field: design-for-form-and-experience
product: concept-design
tags: [solidworks, surface-modeling, boundary-surface, curvature-continuous, tangency-conditions, surfacing, industrial-design, product-design]
level: advanced
status: draft
description: "Build Boundary Surfaces in SOLIDWORKS with the right curves in each direction, tangency and curvature conditions to neighbours, and influence settings for clean highlights."
sources:
  - "SOLIDWORKS Help - Boundary Surface PropertyManager, Surfaces overview (help.solidworks.com)"
  - "SOLIDWORKS Help - Curvature continuous conditions and Zebra Stripes"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Boundary surfaces in SOLIDWORKS

**Goal:** a surface patch that meets its neighbours smoothly (tangent or curvature
continuous) so the product shows unbroken highlights.

## Before you start
- Plan patches as four-sided wherever possible. Three-sided and many-sided patches are the
  usual source of pinches.
- Build clean boundary curves first: 3D sketches or split lines on adjacent faces, with as few
  spline points as possible. Check curvature combs on every spline (right-click spline > Show
  Curvature Combs); combs should change gradually with no flips.

## Steps
1. Insert > Surface > **Boundary Surface**.
2. **Direction 1:** select the two (or more) curves or edges that run one way. Pick them at
   matching ends so the preview does not twist.
3. **Direction 2:** select the cross curves.
4. For each edge that lies on an existing face, set the **Tangent Type**: None, Direction
   Vector, Normal To Profile, **Tangency To Face** (G1) or **Curvature To Face** (G2). Use
   Curvature To Face where highlights must flow.
5. Adjust **tangent influence** (tangent length) per edge; too low and the patch flattens near
   the edge, too high and it bulges.
6. Use **Trim by direction 1** when curves overshoot. Turn on curvature combs and Zebra Stripes
   in the preview.
7. OK, then Knit with neighbours (Insert > Surface > Knit) and check gaps.

## Gotchas
- Curvature To Face needs the neighbour itself to be smooth; a G2 condition on a bad face
  propagates the problem.
- Curves that meet at different parameter speeds cause wobbles; re-fit splines with matching
  point counts.
- Boundary Surface prefers edges to sketch entities for continuity; select model edges where you can.

## Verify
Zebra stripes cross every boundary with no kink (G2) or with aligned but kinked stripes where
G1 was intended; Check (Tools > Evaluate > Check) reports no bad faces; deviation analysis
along the shared edge reads near 0 degrees.
