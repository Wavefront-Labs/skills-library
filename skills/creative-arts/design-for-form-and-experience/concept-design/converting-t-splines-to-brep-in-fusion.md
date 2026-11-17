---
id: creative-arts.design-for-form-and-experience.concept-design.converting-t-splines-to-brep-in-fusion
name: converting-t-splines-to-brep-in-fusion
category: creative-arts
field: design-for-form-and-experience
product: concept-design
tags: [t-spline-to-brep, finish-form, brep-conversion, fusion-form, form-modeling, convert-form]
level: practitioner
status: draft
description: "Convert a Fusion T-spline body to BRep with Finish Form, and know what changes: cage control lost, history, conversion issues and when to stay in Form."
sources:
  - "Autodesk Fusion help (help.autodesk.com/view/fusion360)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Converting T-splines to BRep

In Fusion a Form (T-spline) body is a smooth subdivision-style surface. To use shell, fillet, hole, CAM or simulation you need a BRep (boundary representation) body. Menu placement differs by release; verify in your build.

## What to know
- **Finish Form** (button in the Form environment) ends the form session and yields a BRep body for the Design features. In a parametric design the Form feature stays in the timeline and can be re-edited while you are still working in that history.
- The BRep has no cage: you cannot push cage points on it. To change shape, edit the Form feature in the timeline, or start a new Form.
- Closed forms can become solids; open forms become surface bodies.
- Direct-modelling designs have no history to return to; save a version before converting.

## Preparing for clean conversion
1. Remove creases you do not want and check that every edge is intended; tiny unwanted faces cause bad fillets later.
2. Keep cage faces quad where possible; extraordinary vertices (3 or 5 edges) belong in flat or low-curvature areas.
3. Close gaps; weld vertices at seams.
4. Check zebra and curvature before converting.

## After
Add shell, fillets and features on the BRep; inspect for sliver faces; compare with the intended section lines.

## Verify
- [ ] Body type is a solid if intended.
- [ ] Zebra stripes continue smoothly across converted faces.
- [ ] A pre-conversion version was saved.
