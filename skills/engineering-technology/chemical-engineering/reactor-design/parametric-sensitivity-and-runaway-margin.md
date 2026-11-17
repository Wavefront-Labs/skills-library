---
id: engineering-technology.chemical-engineering.reactor-design.parametric-sensitivity-and-runaway-margin
name: parametric-sensitivity-and-runaway-margin
category: engineering-technology
field: chemical-engineering
product: reactor-design
tags: [chemical-engineering, reactor-design, rx-heat-effects-and-stability, parametric-sensitivity-and-runaway-margin, parametric-sensitivity, thermal-runaway, semenov, runaway-margin, hot-spot, wall-cooled-reactor, tubular-reactor, safety-margin]
level: advanced
status: draft
description: "Assess parametric sensitivity and thermal runaway margin for exothermic reactors with Semenov and RT^2/E rules, wall-cooled tube checks and when to hand off to calorimetry."
sources:
  - "Fogler Elements of Chemical Reaction Engineering, Levenspiel Chemical Reaction Engineering, Froment Bischoff and De Wilde Chemical Reactor Analysis and Design"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Parametric sensitivity and runaway margin

**Goal:** screen how close an exothermic reactor is to runaway and what operating margin to demand. This is a screening method; actual safe design requires reaction calorimetry, a hazard study and qualified engineers.

## Concepts
- **Parametric sensitivity**: a small change in inlet temperature, coolant temperature or composition causes a large change in the hot-spot temperature, typically in wall-cooled tubular reactors.
- **Semenov (thermal explosion) criterion**: for a vessel with heat loss, ignition happens when the heat generation curve is tangent to the heat-loss line; the critical rise of the reaction temperature above the surroundings is of order R T^2 / E.
 Example: E/R = 10,000 K and T = 400 K gives R T^2/E = 400^2/10,000 = 16 K. A reactor operating with more than about this much temperature rise above the coolant is near the sensitive region.

## Screening procedure
1. Compute E/R from kinetics and the operating temperature; compute R T^2/E.
2. Compute the temperature difference between the process and coolant at the hot spot; compare.
3. Run the simulation of the tube (see the energy balance skill) at coolant temperature plus 1, 2, 5 K and inlet concentration plus 5%: record hot spot peak temperature; plot peak T versus the parameter; a steep rise defines the sensitive region.
4. Apply a margin: operate well below the point where the slope of peak T versus coolant T is above a few K per K.
5. Define protective measures: limits on feed concentration, interlocks on coolant flow and temperature, quench or dump systems; document in the hazard review.

## Gotchas
- A hot spot in the first part of a tube can exceed catalyst limits long before outlet temperature shows a problem.
- Two-dimensional models (radial profiles) can show hotter centre temperatures than one-dimensional models.
- Aging catalyst shifts the hot spot downstream; operating margin changes with time.

## Verify
- [ ] Sensitivity plot produced and operating point sits on the safe side.
- [ ] Hand-off to calorimetry and the formal hazard study noted.
