---
id: engineering-technology.automotive-vehicle-engineering.crash-safety.composite-crash-absorbers
name: composite-crash-absorbers
category: engineering-technology
field: automotive-vehicle-engineering
product: crash-safety
tags: [composite-crash, cfrp, crash-absorber, progressive-crush, specific-energy-absorption, sea, trigger, composite-tube, smc, crash-materials, delamination]
level: practitioner
status: gated
description: "Design composite (CFRP/GFRP) crash absorbers: crush mechanism, trigger, specific energy absorption, off-axis sensitivity, modelling, and testing and certification points."
sources:
  - "Kramer, Passive Safety of Vehicles (chapter list)"
  - "Huang, Vehicle Crash Mechanics (chapter list)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Composite crash absorbers

LS-DYNA MAT_54/58/262 names and the SEA comparison are unconfirmed (gated: unconfirmed, source is paywalled or blocked).

## 1. Mechanism
Unlike metals that fold, a well-designed composite tube absorbs energy by progressive crushing: fronds splay outward or inward and fibres and matrix fragment at a stable crush front, giving a near-constant crush force. Brittle failure (global buckling, delamination without fragmentation) gives low energy absorption and a force collapse, which is the main design risk.

## 2. Key parameters
- **Specific energy absorption (SEA)** = energy absorbed / mass of crushed material (kJ/kg). Carbon-epoxy tubes can reach SEA values that are several times those of steel or aluminium sections when they crush progressively; the exact figure depends on layup, section and test speed. Measure on your design.
- **Trigger:** a chamfer, bevel or stepped wall at the loaded end to initiate stable crushing and limit the initial peak force.
- **Fibre architecture:** hoop and axial layers, braided or woven; fibre type (carbon, glass, aramid), resin toughness.
- **Section shape:** round tubes crush most stably; square tubes need corner radii; honeycomb or foam fills can stabilise.
- **Crush efficiency:** crush force efficiency (mean force/peak force) and stroke efficiency (usable stroke/length).

## 3. Application
Composite crash boxes and bumper beams, battery enclosure frames and shields (glass-fibre sheet moulding compounds are common for pack covers), motorsport noses and side structures. Consider off-axis loading (oblique impact) because crush stability falls with load angle; combine with metal support or guides. Compare cost, repair and recycling.

## 4. Modelling
Ply-level shell models (continuum damage material models in explicit solvers such as MAT_54/58/262 in LS-DYNA), cohesive layers for delamination, and calibration against coupon and tube crush tests. Crush predictions are sensitive; correlate carefully (see correlation). Use test-supported empirical force levels for early design.

## 5. Testing and certification
Quasi-static and dynamic tube crush tests with the trigger design and temperature (hot, cold, humid), off-axis tests, post-test inspection. Include environmental ageing, impact damage from stone strike and repair, and the required regulatory crash tests of the whole vehicle.

## Verify
- [ ] Crush mode observed as progressive in tests, SEA measured.
- [ ] Trigger controls the initial peak.
- [ ] Off-axis and temperature extremes tested.
- [ ] Modelling calibrated to the tube tests.
