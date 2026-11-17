---
id: engineering-technology.chemical-engineering.piping-instrumentation.flow-meter-selection
name: flow-meter-selection
category: engineering-technology
field: chemical-engineering
product: piping-instrumentation
tags: [chemical-engineering, piping-instrumentation, pi-instrument-selection, flow-meter-selection, flow-meter, orifice-plate, coriolis, magnetic-flowmeter]
level: practitioner
status: gated
description: "Select a flow meter from the fluid, range, accuracy and installation constraints: orifice, vortex, Coriolis, magnetic, ultrasonic."
sources:
  - "Crane Technical Paper 410, Perry Chemical Engineers Handbook, ASME B31.3, ISA-5.1, Darby Chemical Engineering Fluid Mechanics, Karassik Pump Handbook"
  - "https://www.isa.org"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Flow meter selection

**Goal:** Select a flow meter from the fluid, range, accuracy and installation constraints: orifice, vortex, Coriolis, magnetic, ultrasonic.

## Steps
1. List the fluid properties, range, turndown, accuracy needed (and whether it is for custody transfer), pressure drop limit and line size.
2. Differential pressure (orifice) is robust and common but has limited turndown and a pressure loss; vortex fits clean steam and gas; Coriolis gives mass flow and density with high accuracy; magnetic needs a conductive liquid; ultrasonic can be clamp-on for retrofit.
3. Check the straight pipe run requirement, which depends on the meter and upstream fittings (use the manufacturer figures).
4. Check the two-phase and solids content.
5. Specify the materials, the ratings and the calibration.

## Gotchas
- Wrong meter type for the fluid is the common error, such as a magnetic meter on hydrocarbons.
- Orifice sizing is covered by the ISO 5167 series; confirm the edition (gated: unconfirmed, source is paywalled or blocked).

## Verify
- [ ] Range and accuracy meet the need across the operating range.
- [ ] Installation requirements are met.
