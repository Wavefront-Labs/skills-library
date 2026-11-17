---
id: engineering-technology.civil-engineering.geotechnical-engineering.pile-axial-capacity
name: pile-axial-capacity
category: engineering-technology
field: civil-engineering
product: geotechnical-engineering
tags: [pile-capacity, deep-foundation, driven-pile, bored-pile, drilled-shaft, alpha-method, beta-method, skin-friction, end-bearing, negative-skin-friction, pile-load-test]
level: advanced
status: draft
description: "Estimate axial capacity of driven or bored piles from soil data: shaft and base resistance, alpha/beta methods, group effects, negative skin friction and load tests."
sources: ["FHWA GEC-10 Drilled Shafts: Construction Procedures and LRFD Design Methods", "FHWA NHI-16-009 Design and Construction of Driven Pile Foundations", "Fleming et al., Piling Engineering", "Tomlinson and Woodward, Pile Design and Construction Practice"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Pile axial capacity

**Goal:** Qu = Qs (shaft) + Qb (base), checked against settlement and verified by testing.

## Static methods
- Clay, undrained (alpha method): fs = alpha * su, alpha commonly 0.3 to 1.0 and falling as su rises; take the curve from FHWA guidance for your pile type. Base qb = Nc*su, Nc about 9.
- Sand and drained clay (beta method): fs = beta * sigma'v, beta commonly 0.2 to 0.5 by soil and pile type. Base qb = Nq * sigma'vb with a limiting value per method.
- CPT or SPT correlation methods are alternatives; never mix factors across methods.
- Sum layer by layer. Neglect shaft friction in the top zone disturbed by construction or seasonal change.
- Bored piles: base needs large movement (roughly 5 to 10% of diameter) to mobilise in sand; reduce for soft debris.

## Other effects
- Negative skin friction (downdrag) from settling fill: treat as additional load, and check structural capacity.
- Groups: block failure can govern in clay; spacing of 2.5 to 3 diameters or more is common; group settlement exceeds single-pile settlement.
- Lateral loads need separate p-y analysis.

## Resistance and testing
Apply LRFD resistance factors or a working-stress FS of about 2 to 3 (higher with few tests). Verify by static load test (ASTM D1143), dynamic test (ASTM D4945), or bi-directional cell. Production piles: driving criteria or integrity tests.

## Verify
Hand-total a layered profile; compare with a CPT-based method; confirm settlement at working load is within structural limits.

> Professional guidance only. Design, sign-off and site decisions belong to a licensed/chartered engineer applying the codes adopted in the project jurisdiction; check edition and local amendments.
