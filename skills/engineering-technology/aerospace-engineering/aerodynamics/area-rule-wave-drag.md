---
id: engineering-technology.aerospace-engineering.aerodynamics.area-rule-wave-drag
name: area-rule-wave-drag
category: engineering-technology
field: aerospace-engineering
product: aerodynamics
tags: [aerodynamics, transonic, supersonic, area-rule, wave-drag, sears-haack, whitcomb, cross-section-area-distribution, fuselage-contouring]
level: advanced
status: verified
description: "Apply the transonic and supersonic area rule: smooth the cross-sectional area distribution of the whole aircraft to reduce wave drag, and check it from CAD."
sources:
  - "Whitcomb, NACA Report 1273"
  - "Raymer, Aircraft Design"
  - "Anderson, Modern Compressible Flow"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Area rule

**Goal:** lower transonic and supersonic wave drag by shaping the vehicle's longitudinal cross-sectional area distribution.

## Principle
At transonic speeds the wave drag of a slender configuration is similar to that of an equivalent body of revolution with the same area distribution. The area distribution should therefore be smooth, avoiding sudden growth where wing and tail add area. Whitcomb's work (early 1950s) formalised the transonic rule (gated: unconfirmed, source is paywalled or blocked); the supersonic extension uses Mach-plane cuts (Jones; Ward). The minimum wave drag for a given length and volume is the Sears-Haack body.

## Procedure
1. From the CAD model, cut cross-section areas at stations along the axis (transonic: planes normal to the axis; supersonic: planes inclined at the Mach angle, giving a family of distributions).
2. Plot `S(x)` for the whole aircraft: fuselage plus wing, tail, nacelles, stores.
3. Look for humps at wing and tail stations. Reduce the fuselage area (waisting) where the wing adds area and fair the bulges.
4. Compare to a Sears-Haack or Von Karman ogive shape of the same length and volume to gauge how far you are from the ideal.
5. Confirm with Euler or RANS drag-rise predictions at the cruise Mach.

## Gotchas
- Waisting costs internal volume; accept anti-shock bodies or fairings only if volume is not critical.
- The rule is first-order: sweep and local thickness effects matter and CFD must be the final check.

## Verify
- [ ] A smooth `S(x)` plot is part of the design record.
- [ ] CFD shows lower wave drag after modifications at the same CL.
