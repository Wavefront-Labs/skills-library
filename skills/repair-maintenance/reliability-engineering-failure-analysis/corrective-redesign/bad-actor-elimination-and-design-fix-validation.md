---
id: repair-maintenance.reliability-engineering-failure-analysis.corrective-redesign.bad-actor-elimination-and-design-fix-validation
name: bad-actor-elimination-and-design-fix-validation
category: repair-maintenance
field: reliability-engineering-failure-analysis
product: corrective-redesign
tags: [corrective-redesign, bad-actors, bad-actor-elimination, pareto, reliability-improvement, design-modification, material-upgrade, component-upgrade, management-of-change, moc, engineering-change, stress-raiser, fillet-radius, seal-upgrade, bearing-upgrade, coatings, cost-benefit, payback, in-service-validation, mtbf-improvement, crow-amsaa, reliability-growth]
level: advanced
status: draft
description: "Find the repeat-failure bad actors, design out the verified root cause with a material, component or geometry change under MOC, and prove the fix in service with before/after reliability data."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Bad-actor elimination and design-fix validation

**Goal:** stop repairing the same failure over and over by changing the design —
material, component, geometry, installation detail — and then prove with data that
the change actually raised reliability.

> Draft: this is the maintenance-engineer scale of redesign (modifications to
> existing equipment), not a new machine design. Anything touching pressure
> boundaries, lifting equipment, safety functions or certified equipment needs the
> relevant code, OEM involvement and qualified sign-off.

## 1. Find the bad actors
- Pull 12–36 months of work orders and downtime from the CMMS.
- **Pareto by cost of failure** (repair labour + parts + lost production), not just
  count: a cheap frequent failure can outrank a rare expensive one, and vice versa.
- Group by asset **and** failure mode. Typical result: ~20 assets/modes drive most of
  the losses.
- Confirm with operations — the CMMS often misses quick fixes nobody logged.

## 2. Prove the cause before changing anything
Run a root cause analysis (see the failed-part examination and cause-tree skill).
You need the **verified physical mechanism**: you can't choose a better material
until you know whether it's fatigue, abrasive wear, corrosion, erosion, heat or
overload. Redesigning on a guess often moves the failure somewhere more expensive.

## 3. Choose the fix — match it to the mechanism
| Mechanism | Typical design fixes |
|---|---|
| Fatigue at a stress raiser | larger fillet radius, remove sharp keyway corners (sled-runner keyway), shot peening, better surface finish, reduce cyclic load (alignment, stiffer support) |
| Abrasive wear | harder/wear-resistant material (hardfacing, ceramic liners, AR steel), better sealing, flow path change |
| Corrosion | material upgrade (e.g. carbon steel → duplex/316, or coatings), remove galvanic couples, drainage |
| Erosion | reduce velocity, longer-radius bends, wear-back plates, harder liners |
| Seal leakage | upgrade seal type/face materials, add flush plan, fix shaft runout |
| Bearing failure | correct bearing type/size for load, sealed-for-life vs relubricated, better lube method, insulated bearings for VFD currents |
| Overheating | improve cooling/ventilation, de-rate, upsize |
| Human/assembly error | error-proof: dowels, asymmetric fixings, torque specs on drawing, alignment jigs |
Generate 2–3 options; evaluate effectiveness, cost, installation downtime, spare
parts impact, side effects (a harder part may wear its mating part faster).

## 4. Cost-benefit
```
annual_loss_now   = failures_per_year * cost_per_failure
annual_loss_after = expected_failures_per_year * cost_per_failure
payback_years     = (one_off_cost) / (annual_loss_now - annual_loss_after - extra_running_cost)
```
Example: 6 failures/yr × 12 000 = 72 000/yr; fix costs 30 000 and is expected to
cut failures to 1/yr → saving 60 000/yr → payback ≈ 0.5 years. Present a range,
not a single optimistic number.

## 5. Implement under management of change (MOC)
- Engineering change request: what, why, drawings/specs updated, risk review
  (does it affect safety, pressure rating, certification, interchangeability?).
- Update CMMS: bill of materials, spare part numbers, PM tasks, drawings.
- Retire old spares or quarantine them so the old part isn't fitted at the next
  breakdown — the most common way a fix gets silently undone.
- Brief the crews: why it changed, any new installation step.

## 6. Validate in service
- Define success up front: e.g. "MTBF from 2 months to > 12 months", "zero seal
  failures in 12 months", "vibration < 2.8 mm/s".
- Monitor actively in the first weeks (inspection, vibration, temperatures) — a fix
  can introduce new modes.
- Compare **before vs after** with the same metric; for repairable systems a
  **Crow-AMSAA (reliability growth) plot** of cumulative failures vs cumulative time on
  log-log axes shows the slope change at the modification date.
- Close the action only when the success criterion is met; otherwise back to RCA.
- Share the fix across identical assets (fleet-wide) once validated.

## Gotchas
- Upgrading material without knowing the mechanism (e.g. harder steel for a fatigue problem).
- Forgetting the storeroom: old spares reintroduce the failure.
- Declaring victory after 4 weeks on a failure that occurred twice a year.
- A design change without updated drawings will be "corrected" back by the next fitter.

## Verify
- [ ] Bad actors ranked by cost of failure from CMMS + operations input.
- [ ] Root cause verified before choosing the fix; fix matched to mechanism.
- [ ] Options compared with cost-benefit and side effects.
- [ ] MOC done: drawings, BOM, spares and PMs updated; old spares quarantined.
- [ ] Success criterion defined and met with before/after data.
