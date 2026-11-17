---
id: creative-arts.design-for-form-and-experience.concept-design.building-lofted-surfaces-with-guide-curves-in-solidworks
name: building-lofted-surfaces-with-guide-curves-in-solidworks
category: creative-arts
field: design-for-form-and-experience
product: concept-design
tags: [surface-loft, loft-surface, guide-curves, solidworks-surfacing, surfacing]
level: practitioner
status: draft
description: "Build lofted surfaces in SOLIDWORKS with matched profiles, guide curves, start and end tangency and centre-line control, and fix twists with connectors."
sources:
  - "SOLIDWORKS Help (help.solidworks.com)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Lofted surfaces and guide curves

A loft blends between two or more profiles. Use Insert > Surface > Loft (the Lofted Surface PropertyManager); menu names can differ slightly by release.

## Prepare
1. Sketch profiles on planes or select faces and edges. Profiles should have a similar segment count and consistent start points.
2. For complex shapes add **guide curves** (sketches or 3D sketches) that touch every profile. A guide curve that does not meet every profile makes the loft fail.
3. Optionally draw a **centre line** to steer the loft path.

## Settings
- **Profiles:** pick near the same corner on each so the loft does not twist; the **connector** handles can be dragged to realign vertices.
- **Start/End constraints:** options include None, Direction Vector, Normal to Profile and Tangency to Face (and Curvature to Face), with tangent-length controls. Use tangency to blend into neighbouring surfaces.
- **Guide curves:** more guides give more control but can over-constrain; add the fewest that hold the shape.

## Troubleshooting
- Twisted result: re-pick profiles near consistent corners or drag connectors.
- Fails with guides: check that each guide has a pierce or coincident relation to every profile.
- Wavy surface: reduce profile count or simplify guides; check with zebra stripes.

## Verify
- [ ] No twisting; connectors align across profiles.
- [ ] Guide curves pierce or touch every profile.
- [ ] Zebra and curvature show smooth continuity with neighbours.
