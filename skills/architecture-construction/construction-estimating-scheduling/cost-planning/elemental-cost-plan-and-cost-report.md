---
id: architecture-construction.construction-estimating-scheduling.cost-planning.elemental-cost-plan-and-cost-report
name: elemental-cost-plan-and-cost-report
category: architecture-construction
field: construction-estimating-scheduling
product: cost-planning
tags: [construction-estimating-scheduling, cost-planning, cost-plan, elemental-cost-plan, nrm1, uniformat, bcis, benchmarking, cost-per-m2, gross-internal-floor-area, gifa, gfa, cost-control, cost-report, forecast-final-cost, estimate-at-completion, eac, forecast-to-complete, committed-cost, variations, change-orders, contingency, value-engineering, cost-management, quantity-surveyor]
level: practitioner
status: draft
description: "Build an elemental cost plan from benchmarks, then run monthly cost reports: committed vs forecast, change/variation tracking, contingency drawdown and forecast final cost."
sources: ["RICS NRM1: Order of cost estimating and cost planning for capital building works", "ASTM E1557 UNIFORMAT II classification", "BCIS elemental cost analysis"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Elemental cost plan and monthly cost report

**Goal:** set a budget the design can be held to, element by element, and then report
each month a forecast final cost that the client or project director can trust.

## 1. Pick the structure
- Use a standard element breakdown so you can benchmark: **NRM1** groups (UK/RICS,
  e.g. 1 Substructure, 2 Superstructure, 3 Internal finishes, 4 Fittings, 5 Services,
  8 External works) or **UNIFORMAT II** (A Substructure, B Shell, C Interiors,
  D Services, E Equipment, G Sitework) in North America.
- Keep **on-costs** separate: preliminaries, overheads and profit, design fees, risk,
  inflation. Mixing them into elements ruins benchmarking.

## 2. Build the plan
1. Measure the key drivers: **GIFA/GFA**, external wall area, roof area, storeys,
   number of units/beds/keys. Wall-to-floor ratio (often ~0.4–0.7 for buildings,
   unverified range) tells you how expensive the envelope will be.
2. For each element: `element unit quantity × element unit rate`, rates from
   rebased past projects (adjust for location, date, specification).
3. **Rebase benchmarks**: apply a tender price index for time and a location factor.
   Never compare raw £/m² or $/SF from different years or regions.
4. Add on-costs in order: prelims %, OH&P %, **design development risk** (higher at
   early stages, e.g. 10–15% at concept falling to ~5% at technical design — rule of
   thumb), construction risk, then **inflation** to the mid-point of construction.
5. Express total as cost/m² GIFA and compare to 3+ benchmarks. Explain any gap.

## 3. Value engineering (when the plan exceeds budget)
List options per element with saving, impact on function/programme/maintenance, and
who decides. Favour high-value elements (envelope, frame, services typically dominate).
Record accepted options and update the plan; a VE list that never reaches the plan
is just a wish list.

## 4. Monthly cost report (construction stage)
Columns per package/line:
| Column | Meaning |
|---|---|
| Budget | contract sum or cost plan allowance |
| Committed | orders/subcontracts let |
| Approved changes | agreed variations / change orders |
| Pending/anticipated | notified, not agreed (priced at best estimate) |
| Forecast final cost | committed + approved + pending + cost to complete |
| Variance | forecast − budget |
- Track **contingency drawdown** separately: start, used, remaining vs % complete.
  If 60% of contingency is gone at 30% progress, say so.
- Include **early warnings / risks** not yet changes, with a probability-weighted figure.
- State the **basis date** and what's excluded (e.g. client direct costs, fees).
- For earned-value control: EAC = AC + (BAC − EV)/CPI is a common formula; CPI =
  EV/AC.

## Gotchas
- Benchmarks that include/exclude prelims or external works inconsistently.
- Forecasts that only add approved variations — pending changes are where overruns hide.
- Double counting a change as both a variation and a contingency draw.
- Inflation applied to start date rather than the construction mid-point.
- Forgetting GIFA changes as the design evolves — recompute every stage.

## Verify
- [ ] Plan follows a standard element structure; on-costs separate.
- [ ] Benchmarks rebased for time and location; ≥3 comparators.
- [ ] Risk and inflation shown as explicit lines with stated basis.
- [ ] Cost report reconciles: forecast = committed + changes + pending + to-complete.
- [ ] Contingency drawdown compared to progress.
- [ ] Report dated, with exclusions and key risks listed.
