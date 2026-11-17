---
id: engineering-technology.chemical-engineering.process-safety.relief-scenario-identification
name: relief-scenario-identification
category: engineering-technology
field: chemical-engineering
product: process-safety
tags: [chemical-engineering, process-safety, ps-relief-sizing, relief-scenario-identification, relief-scenarios, overpressure-scenario, api-521, governing-case, blocked-outlet, fire-case, tube-rupture, loss-of-cooling, pressure-relief]
level: advanced
status: gated
description: "Identify overpressure scenarios (blocked outlet, fire, control failure, cooling loss, tube rupture, runaway) per API 521 and find the governing relief case."
sources:
  - "CCPS Guidelines for Hazard Evaluation Procedures, CCPS Layer of Protection Analysis, API Standards 520 521 526 and 2000, IEC 61511, OSHA 29 CFR 1910.119, EU Seveso III Directive 2012/18/EU, Crowl and Louvar Chemical Process Safety, Lees Loss Prevention in the Process Industries"
  - "https://www.aiche.org"
  - "https://www.osha.gov"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Relief scenario identification

**Goal:** a complete list of credible overpressure causes for each protected system, and the governing case that sets the relief device size. Relief design is safety-critical: it must be performed or reviewed by qualified engineers under the applicable code (for example ASME Boiler and Pressure Vessel Code Section VIII, API 520/521/526, or local equivalents; confirm edition and jurisdiction).

## Typical scenarios (as considered in API 521; confirm the list in the current edition (gated: unconfirmed, source is paywalled or blocked))
1. **Blocked outlet** (closed manual or control valve, pump or compressor discharge blocked in): relief rate is the maximum inflow at relieving conditions.
2. **Control valve failure** (open or closed): maximum flow through a failed-open valve into a lower pressure system (gas breakthrough).
3. **Loss of cooling or reflux**: vapour generation without condensation in a column.
4. **Fire (external)**: heat input to wetted surface; vapour or thermal expansion of liquid.
5. **Power or utility failure** (electric power, steam, instrument air, cooling water).
6. **Heat exchanger tube rupture**: high-pressure side leaks into the low-pressure side.
7. **Thermal expansion of trapped liquid** in blocked-in piping or exchangers.
8. **Reverse flow** (check valve failure).
9. **Runaway chemical reaction** or abnormal heat input (needs calorimetry data and often two-phase relief; see `runaway-relief-design-considerations`).
10. **Absorbent loss, abnormal process heat input, operator error, vacuum conditions.**

## Procedure
1. For each equipment item and header, list scenarios with causes (from the HAZOP and P&IDs).
2. Decide credibility using the organisation's rules (single-failure basis; some scenarios are double jeopardy and not considered together).
3. Compute the relief load (mass flow, properties, relieving temperature and pressure) for each credible scenario; see `relief-valve-sizing-vapour-and-liquid` and `two-phase-relief-sizing`.
4. The governing case is the one requiring the largest relief area; keep all cases in the relief design documentation with the basis.
5. Verify that the set pressure is at or below MAWP, with allowable accumulation (commonly 10% for a single device in non-fire cases, 16% for supplemental devices, 21% for fire; confirm in ASME Section VIII and API 520/521 (gated: unconfirmed, source is paywalled or blocked)).

## Gotchas
- Credit for control valves, trips or instrumented functions to reduce relief load is subject to strict rules (see the code and API 521); credit is not taken lightly.
- Isolation valves upstream or downstream of a relief device must be locked or car-sealed open per the rules.

## Verify
- [ ] A scenario table for each system exists with loads and the governing case.
- [ ] A qualified relief systems engineer reviewed the basis.
