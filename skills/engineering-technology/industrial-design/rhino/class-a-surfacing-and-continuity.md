---
id: engineering-technology.industrial-design.rhino.class-a-surfacing-and-continuity
name: class-a-surfacing-and-continuity
category: engineering-technology
field: industrial-design
product: rhino
tags: [industrial-design, rhino, rhino-8, rhinoceros, nurbs, surfacing, product-modelling, g2-continuity, curvature-continuity, blendsrf, matchsrf, zebra, draftangleanalysis, edgecontinuity, class-a]
level: practitioner
status: docs-checked
description: "Rhino 8 NURBS product surfacing: G0/G1/G2 meaning, BlendSrf and MatchSrf options, and checking with Zebra, EdgeContinuity and DraftAngleAnalysis."
sources:
  - https://docs.mcneel.com/rhino/8/help/en-us/commands/zebra.htm
  - https://docs.mcneel.com/rhino/8/help/en-us/commands/matchsrf.htm
  - https://docs.mcneel.com/rhino/8/help/en-us/commands/blendsrf.htm
  - https://docs.mcneel.com/rhino/8/help/en-us/commands/draftangleanalysis.htm
  - https://docs.mcneel.com/rhino/8/help/en-us/commands/edgecontinuity.htm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Class-A-style surfacing in Rhino: continuity and analysis

**Goal:** surfaces whose highlights flow without kinks, checked with Rhino's analysis
tools, and with the draft a toolmaker needs.

## 1. Continuity levels
- G0: position only. G1: position and tangency. G2: position, tangency and curvature.
- Zebra stripes with kinks or sideways jumps at a seam indicate G0; stripes that line up
  but turn sharply indicate G1; stripes that flow smoothly across the seam indicate G2.

## 2. Joining surfaces
- **BlendSrf** sets continuity for each surface end: Position, Tangency, Curvature, G3 or
  G4. Two bulge sliders set each end's distance of influence (a lock icon keeps their
  relationship). Add Shapes adds profile curves for more control; Straighten adds shapes
  automatically to reduce isocurve twist.
- **MatchSrf** continuity options are Position, Tangency and Curvature (default
  Curvature). The edge being modified must be untrimmed. Average surfaces moves both
  surfaces toward an intermediate shape and turns off history recording.

## 3. Analyse after each step
- **Zebra:** the analysis mesh affects accuracy. Increase mesh density through Analysis
  Mesh Options; free-form NURBS surfaces generally need a detailed mesh.
- **EdgeContinuity:** evaluates how well two surface edges meet position (G0), tangency
  (G1) and curvature (G2) tolerances, showing distance, tangent-direction and curvature
  deviations; each has a tolerance, with good and bad colours for hair lines.
- **DraftAngleAnalysis:** false-colour draft evaluation, often used for injection-moulded
  parts. Set the pulling direction (World Z, CPlane Z, view, two points, curve or edge, or
  named CPlane) and the upper and lower angle values. Blue shows draft above the upper
  value, red below the lower value; if both values are equal, every part exceeding the
  draft angle shows red.

## Gotchas
- A surface can look fine at default Zebra mesh density and fail later: refine the
  analysis mesh before trusting it.
- Match a smooth, simple primary rather than forcing a blend onto a poorly built surface.
- Agree tolerances and the minimum draft with the downstream CAD or toolmaker; this page
  does not set them.

## Verify
- [ ] Zebra stripes flow across every blend that is meant to be G2.
- [ ] EdgeContinuity values are within tolerance where the design intends continuity.
- [ ] DraftAngleAnalysis shows no moulded face below the agreed minimum draft.
- [ ] Receiving CAD opens the exported file as a valid solid.

## Checked
2026-11-01. Confirmed on the McNeel Rhino 8 command pages in sources: G0/G1/G2 Zebra
interpretation, mesh density, BlendSrf and MatchSrf options, EdgeContinuity and
DraftAngleAnalysis behaviour. Removed as not on those pages: template and tolerance
values, curve degree and point-count advice, SubD, fillet and G-level tables for other
commands, CurvatureAnalysis, ShowEdges, Check, STEP and mesh export, all Grasshopper
steps, and the textbook source.
Method: documentation only; no commands were run.
