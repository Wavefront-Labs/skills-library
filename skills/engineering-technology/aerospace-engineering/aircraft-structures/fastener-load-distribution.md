---
id: engineering-technology.aerospace-engineering.aircraft-structures.fastener-load-distribution
name: fastener-load-distribution
category: engineering-technology
field: aerospace-engineering
product: aircraft-structures
tags: [fastener-load-distribution, fastener-flexibility, load-transfer, multi-fastener-joints, joints-and-fasteners]
level: practitioner
status: draft
description: "Estimate load share among rows of fasteners using stiffness models with fastener flexibility, so end fasteners are not under-designed."
sources:
  - "Niu, Airframe Structural Design"
  - "Huth (fastener flexibility literature)"
  - "Megson, Aircraft Structures for Engineering Students"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Fastener load distribution

**Goal:** load per fastener in a multi-fastener splice or doubler.

## Model
1. Represent each plate segment between fasteners as an axial spring `k = E A / L`.
2. Represent each fastener as a spring with flexibility `C` (displacement per unit load) that depends on diameter, plate thicknesses, materials, and single vs double shear. Empirical forms (Tate and Rosenfeld, Huth, Swift) exist; check the form and units in the one you use.
3. Assemble a 1D stiffness model; apply the load; solve for fastener forces.
4. Take the bearing-bypass split at each fastener (see bolted-joint-bearing-bypass).

## Results to expect
- Loads are not equal. The end fasteners of a long row take the most, and the middle ones less, for a flexible-plate and stiff-fastener pair.
- Adding fasteners to a long row helps little beyond a point.
- Stiff fasteners and thicker plates give a more peaky distribution.

## Practice
- For final sizing use FE with fastener elements calibrated against coupon data.
- Use test coupon load-deflection data to derive `C` for your fastener system.
- Apply unequal-share knockdowns when handbook equal-share tables are used.

## Gotchas
- Thermal mismatch between dissimilar materials adds fastener loads.
- Hole-clearance slip shifts load before the joint picks it up.

## Verify
- [ ] The sum of fastener loads equals the applied load in the model.
