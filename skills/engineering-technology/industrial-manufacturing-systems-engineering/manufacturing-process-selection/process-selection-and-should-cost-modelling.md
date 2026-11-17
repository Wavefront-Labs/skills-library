---
id: engineering-technology.industrial-manufacturing-systems-engineering.manufacturing-process-selection.process-selection-and-should-cost-modelling
name: process-selection-and-should-cost-modelling
category: engineering-technology
field: industrial-manufacturing-systems-engineering
product: manufacturing-process-selection
tags: [process-selection, manufacturing-process, should-cost, cost-model, cost-estimating, make-route, routing, dfm, dfma, process-capability, tolerance, break-even, crossover-volume, tooling-amortisation, machine-hour-rate, injection-moulding, die-casting, cnc-machining, sheet-metal, investment-casting, additive-manufacturing, ashby, prima, boothroyd-dewhurst, cost-per-part]
level: practitioner
status: draft
description: "Pick a make-route by screening processes on geometry, tolerance and volume, then compare them with a should-cost model (material, cycle-time rate, tooling amortisation, scrap)."
sources:
  - "Swift & Booker, Manufacturing Process Selection Handbook (PRIMA selection matrices)"
  - "Ashby, Materials Selection in Mechanical Design"
  - "Boothroyd, Dewhurst & Knight, Product Design for Manufacture and Assembly"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Process selection and should-cost modelling

**Goal:** choose how a part will be made by eliminating processes that cannot meet
the design, then ranking the survivors on a transparent cost-per-part model at the
real volume.

## 1. Collect the requirement card
Material (or material family), envelope size and mass, wall thickness range, critical
tolerances and surface finish, annual volume and lifetime volume, ramp profile, and
any special properties (pressure tightness, fatigue, cosmetic class). A process cannot
be selected from a drawing alone; **volume is half the answer**.

## 2. Screen: eliminate, don't rank
Run each candidate through hard filters, in this order:
1. **Material compatibility** (you cannot die-cast steel economically; cannot
   injection-mould a thermoset like a thermoplastic).
2. **Geometry**: undercuts, minimum wall, max size, hollow/closed sections.
3. **Tolerance and finish capability.** Rough orders (verify per supplier): sand casting
   ±0.5-2 mm and Ra 12-25 µm; die casting ±0.1-0.3 mm; investment casting ±0.1-0.25 mm;
   injection moulding ±0.05-0.2 mm (material dependent); CNC milling ±0.01-0.05 mm, Ra 0.8-3.2 µm.
4. **Economic batch range**: injection moulding and die casting usually need 10k+/yr
   to pay for tooling; CNC and additive dominate below ~1k; sheet metal with soft
   tooling spans the middle.
If only one tight feature fails, consider a **hybrid route** (near-net cast + machine
the bore) instead of discarding the cheap primary process.

## 3. Build the should-cost model per surviving route
Cost per part = **material + conversion + tooling amortisation + scrap/yield + secondary ops + overhead/margin**.
- Material = gross mass (part + runner/sprue/chips/skeleton) × €/kg ÷ yield.
- Conversion = cycle time × (machine rate + labour rate × operators per machine).
  Machine rate = (depreciation + floor space + energy + maintenance) ÷ productive hours.
- Tooling = tool cost ÷ parts over the tool's amortisation period (or tool life,
  whichever is shorter); include maintenance and replacement inserts.
- Scrap: divide good-part cost by first-pass yield, don't just add a percentage.

Worked mini-example, 50,000 parts/yr over 3 years, aluminium housing 0.25 kg:
- **Die cast + machine:** material 0.30 kg gross × €3.0 = €0.90; casting 40 s at
  €120/h = €1.33; machining 60 s at €70/h = €1.17; die €90k ÷ 150k = €0.60;
  yield 95% → (0.90+1.33+1.17+0.60) ÷ 0.95 ≈ **€4.21**.
- **Machined from bar:** material 0.9 kg × €3.5 = €3.15; 6 min at €70/h = €7.00;
  fixtures €8k ÷ 150k ≈ €0.05; yield 98% → ≈ **€10.40**.
Crossover volume (fixed tooling F, variable costs v1 < v2): N* = (F1 - F2) ÷ (v2 - v1).
With yield applied, v ≈ €3.58 (cast) and €10.36 (bar), so N* ≈ (90k - 8k) ÷ (10.36 - 3.58) ≈ **12.1k parts** lifetime: below it, machine from bar.
(Rates here are illustrative; use your own plant or regional rates.)

## 4. Score the non-cost factors
Lead time to first parts (die 12-20 weeks vs CNC days), supply-base depth, capital
risk if volumes miss forecast, quality risk (porosity in castings, sink in mouldings),
sustainability (energy/kg, recyclability). Weighted-score them, but keep cost separate
so the trade-off stays visible.

## 5. Define the route
Write the chosen make-route as an operation sequence: primary process → heat treat →
machining datums → finishing → inspection points, with the capability needed at each
step (target Cpk ≥ 1.33 on critical features is a common customer requirement; check
the contract). The route feeds layout, capacity and PFMEA.

## Gotchas
- Cycle time drives conversion cost; for moulding/casting it is dominated by cooling
  time, which scales roughly with wall thickness squared. Thick walls are expensive.
- Quoted tolerances are for a *capable* supplier on a *simple* feature; tight
  tolerances across a parting line or a weld are harder.
- Run the model at 50% and 150% of forecast volume. Tooling-heavy routes are the ones
  that hurt when demand undershoots.
- Ask DFM questions before process: a design change (draft angles, uniform wall)
  often moves the part into a cheaper process.

## Verify
- [ ] Every rejected process has a named hard-filter reason.
- [ ] Each cost line traces to a mass, a cycle time, a rate or a tool quote.
- [ ] Crossover volume is computed and compared with the lifetime forecast.
- [ ] Sensitivity at ±50% volume and ±20% material price shows the choice is stable.
- [ ] The route lists operations, datums and the capability required per critical feature.
