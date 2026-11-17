---
id: engineering-technology.mining-geological-engineering.mine-design-planning.open-pit-optimisation-and-scheduling
name: open-pit-optimisation-and-scheduling
category: engineering-technology
field: mining-geological-engineering
product: mine-design-planning
tags: [mining-geological-engineering, mine-design-planning, open-pit, open-cut, pit-optimisation, pit-optimization, lerchs-grossmann, pseudoflow, nested-shells, revenue-factor, block-model, block-value, cut-off-grade, cutoff-grade, lane-cut-off-theory, pushbacks, phase-design, life-of-mine, lom-schedule, mine-scheduling, npv, mixed-integer-programming, whittle, deswik, datamine, vulcan, jorc, ni-43-101, ore-reserves, dilution]
level: practitioner
status: draft
description: "Optimise an open-pit shell and schedule it: block model, block values, Lerchs-Grossmann/pseudoflow nested shells, pushbacks, cut-off grade and life-of-mine scheduling."
sources:
  - "Hustrulid, Kuchta and Martin, Open Pit Mine Planning and Design"
  - "Lerchs and Grossmann (1965), Optimum design of open-pit mines, CIM Transactions"
  - "Hochbaum (2008), The pseudoflow algorithm, Operations Research"
  - "Lane, The Economic Definition of Ore: Cut-off Grades in Theory and Practice"
  - "SME Mining Engineering Handbook (3rd ed.)"
  - "JORC Code (2012) and CIM Definition Standards / NI 43-101"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Open-pit optimisation and scheduling — from block model to life-of-mine plan

**Goal:** turn a resource block model into an economically optimal ultimate pit,
practical pushbacks and a period-by-period schedule that maximises NPV under real
mining and plant constraints, in a form that survives a reserve audit.

## 1. Prepare the block model
- Regularise to the **selective mining unit (SMU)** your equipment can actually dig
  (often 5×5×bench height up to 25×25×15 m) so dilution and ore loss are built in.
- Carry: density, grades, **resource category**, rock type, recovery domain, slope
  sector. Only Measured/Indicated may become reserves under JORC, NI 43-101 / CIM or
  SME codes; set Inferred to zero grade (waste) for reserve work.
- Get **overall slope angles by sector** from geotechnical design. Optimisers need
  the overall angle *including* ramps and berms, not the inter-ramp angle — a ramp
  on a wall can flatten it by several degrees.

## 2. Value every block
For each block, compute both destinations and keep the better:
```
Process value = t × g × R × (P − S) − t × (Cm + Cp + G&A)
Waste value   = − t × Cm
```
t tonnes, g grade, R metallurgical recovery, P price, S selling/refining cost per unit
metal, Cm mining cost (add an increment per bench below the reference level — haul
cost rises with depth), Cp processing cost per tonne. The **marginal (internal)
cut-off grade** at the pit-shell stage is

`g_cut = (Cp + G&A) / ((P − S) × R)`

Mining cost is already sunk for any block inside the pit, so it is left out of the
mill/waste decision but included in the shell decision.

## 3. Generate nested shells
- **Lerchs-Grossmann** (graph closure) and **pseudoflow** (max-flow) give the same
  mathematically optimal undiscounted pit; pseudoflow is much faster on large models
  and is now the default in most packages (Whittle, Deswik, Datamine, Vulcan,
  Hexagon and others — names and menus differ, the maths does not).
- Run with **revenue factors** (price multipliers) from about 0.3 to 1.3 in small
  steps. Each RF gives a shell; the series of nested shells shows where value
  accrues.
- Plot the **pit-by-pit graph**: discounted cash flow for a best case (shell-by-shell
  mining) and worst case (bench-by-bench). The practical choice is usually *inside*
  the RF 1.0 shell — often around RF 0.7–0.9 — because the outermost shells add tonnes
  for almost no discounted value and raise risk.

## 4. Design pushbacks (phases)
- Pick 3–7 intermediate shells as phase guides, chosen where the tonnage step and
  value step are balanced.
- Enforce **minimum mining width** between phases (commonly 40–80 m for large
  trucks and shovels; size to your fleet turning circles) and a ramp access in
  every phase.
- Convert shells to engineered designs (benches, berms, ramps at ~8–10% grade,
  switchbacks) and re-report tonnes — the designed pit typically differs from the
  shell by a few percent; investigate if it is more than about 5%.

## 5. Schedule the life of mine
- Constraints: total material movement per period, plant throughput (t/h × hours ×
  availability), vertical advance per phase (often 6–12 benches per year), phase
  lag, blending limits on deleterious elements, stockpile capacity.
- Methods: heuristic bench sequencing, or mixed-integer programming that chooses
  block/period and destination to maximise NPV. Use **dynamic cut-off grades**
  (Lane's theory): when the mill is the bottleneck, raise the cut-off early and
  stockpile low grade for the end of mine life.
- Check the stripping ratio profile: front-loaded waste is normal but must be
  fundable and within fleet capacity.

## Gotchas
- An RF 1.0 shell is the maximum *undiscounted* pit, not the maximum-NPV pit.
- Block size and the slope precedence pattern both introduce slope error; test the
  optimiser's achieved slope on a section.
- Recovery that varies with grade or ore type must be modelled per block, not as a
  site average, or low-grade margins are overstated.
- Processing cost expressed per hour (throughput-limited hard ore) is not the same
  as cost per tonne — treat hardness domains separately.
- Re-optimising every quarter with a new price chases noise; use a long-term
  consensus price and run price sensitivities instead.
- Reserve reporting requires sign-off by a Competent/Qualified Person under the
  applicable code.

## Verify
- [ ] Block model regularised to SMU and Inferred blocks carried as waste.
- [ ] Slope angles are overall (with ramps) per geotechnical sector.
- [ ] Pit-by-pit graph produced and the selected shell justified on discounted value.
- [ ] Designed pit reconciles to the selected shell within about 5% of tonnes and metal.
- [ ] Schedule respects mining, milling, vertical-advance and blending limits every period.
- [ ] Sensitivities run on price, recovery, cost and slope angle.
