---
id: engineering-technology.agricultural-and-biosystems-engineering.irrigation-design.application-and-project-efficiency-definitions
name: application-and-project-efficiency-definitions
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: irrigation-design
tags: [agricultural-and-biosystems-engineering, irrigation-design, application-efficiency, irrigation-efficiency, distribution-uniformity, project-efficiency, consumptive-use-fraction, performance-indicators]
level: practitioner
status: gated
description: "Define and compute irrigation efficiency terms consistently: application efficiency, distribution uniformity, conveyance and project efficiency, and consumptive use."
sources:
  - "USDA NRCS National Engineering Handbook, Part 623 Irrigation (https://www.nrcs.usda.gov)"
  - "Allen, Pereira, Raes & Smith, FAO Irrigation and Drainage Paper 56: Crop Evapotranspiration (https://www.fao.org/4/x0490e/x0490e00.htm)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Application and project efficiency definitions

**Goal:** report efficiency in a way that others can compare and that does not confuse reuse with loss.

## Definitions (field level)
- Application efficiency (Ea) = volume of water stored in the root zone and used beneficially / volume applied to the field. Beneficial uses include crop ET, leaching requirement and cooling or frost control if relevant.
- Distribution uniformity (DU) = average depth in the low quarter / average depth overall (for surface and microirrigation, also an emission uniformity measure). DU is a measure of the system's evenness, not a measure of loss.
- Requirement efficiency or adequacy: the fraction of the field receiving at least the required depth.
- Conveyance efficiency = water delivered to the field / water diverted to the canal or pipe.
- Project (or overall) efficiency = Ec x Ea (and a field-to-field combination); a low project efficiency may not be a loss at basin scale if drainage and seepage are reused downstream.

## Consumptive use fraction
Consumptive fraction compares ET to net inflow at basin level and identifies real water consumption versus recoverable flows. Hydrologists prefer it to classical efficiency.

## Pitfalls
Quoting "efficiency" without saying which; losing track of leaching needs when calculating Ea; comparing a design value with a measured one; using wind-free test conditions.

## Verify
- [ ] Each efficiency labelled with its definition and the volume basis.
- [ ] Measured data (not just catalogue figures) back any reported value.
- Definitions follow common NRCS and ASCE usage (gated: unconfirmed, source is paywalled or blocked); classical numeric targets differ between texts and are not given here.
