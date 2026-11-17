---
id: creative-arts.design-for-form-and-experience.concept-design.checking-surface-quality-with-zebra-stripes-and-curvature
name: checking-surface-quality-with-zebra-stripes-and-curvature
category: creative-arts
field: design-for-form-and-experience
product: concept-design
tags: [solidworks, surface-modeling, zebra-stripes, curvature-analysis, curvature-comb, deviation-analysis, g2-continuity, fusion-360, surface-quality]
level: practitioner
status: draft
description: "Judge surface quality in SOLIDWORKS or Fusion with zebra stripes, curvature display, curvature combs and deviation analysis, and know what each defect pattern means."
sources:
  - "SOLIDWORKS Help - Zebra Stripes, Curvature, Deviation Analysis (help.solidworks.com)"
  - "Autodesk Fusion help - Inspect - Zebra Analysis, Curvature Map Analysis, Curvature Comb Analysis (help.autodesk.com/view/fusion360/ENU)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Zebra stripes and curvature analysis

**Goal:** see surface faults before a render, a print or a tool reveals them.

## Tools
| Tool | SOLIDWORKS | Fusion |
|---|---|---|
| Zebra stripes | View > Display > Zebra Stripes | Inspect > Zebra Analysis |
| Curvature map | View > Display > Curvature | Inspect > Curvature Map Analysis |
| Curvature comb | Right-click curve/edge > Show Curvature Combs | Inspect > Curvature Comb Analysis |
| Edge continuity | Tools > Evaluate > Deviation Analysis | Inspect > Zebra across edges |

## Reading zebra stripes
- **Stripes break (jump) at an edge:** position only (G0), a visible crease.
- **Stripes meet but kink sharply:** tangent (G1); a highlight changes speed at the edge.
- **Stripes flow smoothly through:** curvature continuous (G2).
- **Wobbly or rippled stripes inside a face:** too many control points or uneven spacing.
- **Stripes bunch or pinch at a corner:** degenerate or three-sided patch.
Rotate the model and change stripe direction and density; one orientation can hide a fault.

## Curvature combs
On curves: comb teeth should change length smoothly; a sudden jump means a curvature
discontinuity, a flip to the other side means an inflection (S-bend), often unintended.

## Deviation analysis (SOLIDWORKS)
Select the two faces' shared edge; set number of sample points; read max angle deviation.
Under about 0.5 degree reads tangent in practice for consumer products; for A-class work teams
set tighter limits.

## Gotchas
- Display quality: turn image quality up, or the faceting creates false wobble.
- Zebra on very small faces is meaningless; judge those by render.
- Fillets from the standard command are G1 unless set curvature continuous; expect kinks.

## Verify
Record screenshots of zebra at two orientations for each key surface at review; every flagged
fault is either fixed or accepted with a reason.
