---
id: engineering-technology.chemical-engineering.aspen.pump-compressor-turbine-blocks
name: pump-compressor-turbine-blocks
category: engineering-technology
field: chemical-engineering
product: aspen
tags: [chemical-engineering, aspen, aspen-rotating-equipment-and-hydraulics, pump-compressor-turbine-blocks, pump-block, compressor-block, turbine-block]
level: practitioner
status: gated
description: "Use the Aspen Plus Pump, Compr and Turbine blocks: specify pressure and efficiency and check power, NPSH and phase conditions."
sources:
  - "Aspen Plus and Aspen HYSYS user guides and help (AspenTech), Seider et al. Product and Process Design Principles"
  - "https://www.aspentech.com"
  - "AspenTech Aspen Plus certification study guide AT-05198 (learning objectives, aspentech.com)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pump compressor turbine blocks

**Goal:** Use the Aspen Plus Pump, Compr and Turbine blocks: specify pressure and efficiency and check power, NPSH and phase conditions.

## Steps
1. (Block names and options below are Aspen-specific (gated: unconfirmed, source is paywalled or blocked); the study guide confirms design and rating specifications for pumps and compressors and an expander/compressor flowsheet.) Pump: specify discharge pressure (or pressure rise) and an efficiency; the block reports duty and head and NPSH available.
2. Compr: select the isentropic, polytropic or positive-displacement model, set discharge pressure and efficiency; use MCompr for multistage with intercoolers.
3. Turbine (expander option): specify discharge pressure and isentropic efficiency; check the outlet for liquid formation.
4. Use a property method suited to gases (equation of state) so that non-ideality and compressibility are right.
5. Use efficiencies from vendor curves or typical values and confirm them for the machine type.

## Gotchas
- Wet outlet from an expander may signal an unrealistic specification.
- Efficiency definitions (isentropic or polytropic) differ; match to vendor data.

## Verify
- [ ] Power matches a hand calculation with the same efficiency.
- [ ] Outlet phase is physically acceptable.
