---
id: engineering-technology.automotive-vehicle-engineering.crash-safety.spot-weld-and-joint-modelling
name: spot-weld-and-joint-modelling
category: engineering-technology
field: automotive-vehicle-engineering
product: crash-safety
tags: [joint-modelling, spot-weld, spot-weld-model, adhesive-model, cohesive-element, mat-100, connection-modelling, coach-peel, lap-shear, weld-failure, crash-cae]
level: practitioner
status: draft
description: "Model body joints for crash: spot weld models, failure by force and moment, adhesive cohesive layers, laser weld and bolts, and the coupon tests that calibrate them."
sources:
  - "LS-DYNA user manual contents (keyword manual volumes I-III; vendor documentation at https://www.ansys.com)"
  - "Huang, Vehicle Crash Mechanics (chapter list)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Spot weld and joint modelling

## 1. Joint types
Resistance spot welds (thousands in a body), structural adhesives, laser and arc seam welds, rivets and flow-drill screws, bolts. Each needs a model that carries stiffness correctly and fails at realistic loads.

## 2. Spot weld models
- **Beam or rigid-link connectors** (simple, fast): a beam between two shell nodes with a spot-weld material (LS-DYNA MAT_100 type); failure from normal force F_n, shear force F_s and moments, typically written as an interaction (F_n/F_n_max)^a + (F_s/F_s_max)^b >= 1.
- **Solid hexahedral weld elements** connected to shells (area contact models) capture local deformation and pull-out better; costlier.
- **Generalised connection elements** in some solvers calibrated from coupon tests.
Mesh must place a node at each weld (or use projection onto the nearest shell), and the weld diameter parameter drives strength (nugget size from the weld schedule).

## 3. Coupon calibration
Test lap shear, cross tension, coach peel and combined mode (angled) coupons for each material and thickness stack, at quasi-static and higher rates. Failure modes are nugget pull-out (plug failure, the desired mode), interfacial failure (low ductility steels) and HAZ cracking in ultra-high strength steel; model them differently. Calibrate failure forces versus plate thickness and strength, including strength reduction in HAZ for hot-stamped steel.

## 4. Adhesive models
Cohesive zone elements or tied contact with failure (LS-DYNA TIEBREAK, cohesive material MAT_240-type mixed-mode law), calibrated from butt-joint, lap-shear and peel tests. Account for rate dependence and for a thickness of the bond line (typically around a millimetre).

## 5. Practical points
Weld count and pitch drive body stiffness; include missing welds only where deliberately missing; model sealed flange adhesives; keep a database of weld schedules (nugget diameter). Check energy absorption of joint failure does not dominate or vanish.

## 6. Validation
Component crush tests with joints (hat section with flanges, B-pillar assembly). Compare weld failure counts and locations with the model.

## Verify
- [ ] Coupon tests cover all material stacks and failure modes.
- [ ] Failure criterion includes normal and shear interaction.
- [ ] Adhesive properties are rate-dependent where relevant.
- [ ] Component test shows matching joint failure locations.
