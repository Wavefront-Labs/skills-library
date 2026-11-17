---
id: engineering-technology.chemical-engineering.process-design.pressure-vessel-preliminary-sizing
name: pressure-vessel-preliminary-sizing
category: engineering-technology
field: chemical-engineering
product: process-design
tags: [chemical-engineering, process-design, pd-equipment-sizing, pressure-vessel-preliminary-sizing, pressure-vessel, design-pressure, design-temperature, shell-thickness, asme-viii, corrosion-allowance, vessel-datasheet, preliminary-sizing]
level: practitioner
status: gated
description: "Do a preliminary pressure vessel sizing: design pressure and temperature margins, shell thickness estimate, heads, corrosion allowance, with a hand-off to code design."
sources:
  - "Towler and Sinnott Chemical Engineering Design, Turton et al. Analysis Synthesis and Design of Chemical Processes, Peters Timmerhaus and West Plant Design and Economics, Douglas Conceptual Design of Chemical Processes, NCEES FE and PE Chemical exam specifications"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Preliminary pressure vessel sizing

**Goal:** vessel dimensions and an estimated wall thickness for cost and weight, handed to a qualified vessel designer for code design.

## Design conditions
- **Design pressure**: the maximum operating pressure plus margin; a common rule of thumb is the larger of 10% above the maximum operating pressure or roughly 1.7 bar (25 psi) above it (gated: unconfirmed, source is paywalled or blocked), and never below the relief set pressure; also consider full vacuum. Follow your company standard and the code.
- **Design temperature**: maximum operating temperature plus a margin (for example 15 to 30 C (gated: unconfirmed, source is paywalled or blocked)), and minimum design metal temperature for brittle fracture.

## Thickness estimate (cylindrical shell, internal pressure, thin wall)
t = P x R / (S x E - 0.6 x P) + corrosion allowance (the ASME VIII-1 UG-27 circumferential-stress form (gated: unconfirmed, source is paywalled or blocked)), where R is the inside radius, S the allowable stress at the design temperature from the code table, E the weld joint efficiency (for example 0.85 to 1.0 (gated: unconfirmed, source is paywalled or blocked)). Heads: 2:1 elliptical heads need about the same thickness as the shell for the same material; hemispherical about half.

## Procedure
1. Fix the diameter and tangent-to-tangent length from process sizing.
2. Choose the material and look up S from the applicable code for your temperature.
3. Compute the shell and head thickness; add corrosion allowance (for example 1.5 to 3 mm for carbon steel (gated: unconfirmed, source is paywalled or blocked); set by corrosion data).
4. Add the weight to the equipment list and cost.
5. Provide the vessel data sheet: nozzles, internals, loadings, codes, inspection class.

## Gotchas
- Final design to the pressure vessel code (ASME Section VIII, EN 13445, or the local code) must be done and stamped by qualified engineers; this skill is for estimating only.
- Vacuum duty and wind or seismic loads often govern thickness for tall columns.

## Verify
- [ ] Hand calculation with a recorded stress value and source of the table.
- [ ] Design basis states codes, edition and jurisdiction.
