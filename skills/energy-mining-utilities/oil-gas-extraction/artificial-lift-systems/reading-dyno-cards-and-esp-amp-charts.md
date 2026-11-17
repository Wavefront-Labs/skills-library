---
id: energy-mining-utilities.oil-gas-extraction.artificial-lift-systems.reading-dyno-cards-and-esp-amp-charts
name: reading-dyno-cards-and-esp-amp-charts
category: energy-mining-utilities
field: oil-gas-extraction
product: artificial-lift-systems
tags: [artificial-lift-systems, artificial-lift, beam-pump, rod-pump, sucker-rod, pump-jack, dynamometer, dyno-card, downhole-card, fluid-pound, gas-interference, pump-off-controller, poc, fluid-level, echometer, esp, electric-submersible-pump, amp-chart, vsd, gas-lock, underload, overload, gas-lift, gas-lift-valve, unloading, plunger-lift, plunger, well-optimisation, production-engineering]
level: practitioner
status: draft
description: "Troubleshoot artificial lift: read rod-pump dynamometer card shapes, tune pump-off control, interpret ESP amp charts and trips, and check gas lift and plunger lift behaviour."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reading dyno cards and ESP amp charts

**Goal:** diagnose why an artificially lifted well is underperforming or failing, using
the data the lift system already produces, and make the tuning call or the workover
call correctly.

> Status: draft. Card shapes and chart patterns are industry-standard diagnostics, but
> interpretation depends on the well; confirm with fluid levels and production tests.
> Lift selection is in engineering-technology.petroleum-engineering.production-engineering.nodal-analysis-and-artificial-lift-selection.

## 1. Rod pump (beam pump) dynamometer cards
A **downhole card** (computed from the surface card) plots pump load against plunger
position. Shapes to know:
- **Full pump:** roughly rectangular — load picks up quickly at the bottom of the
  stroke and releases quickly at the top.
- **Fluid pound:** the downstroke load stays high, then drops sharply partway through —
  the plunger hits fluid in a partly filled barrel. Causes rod and pump damage. Fix:
  slow the unit, shorten run time, or let the pump-off controller (POC) idle the well.
- **Gas interference:** like fluid pound but the load falls gradually (gas compresses).
  Fix: gas anchor/separator, set the pump below the perforations, vent the casing.
- **Leaking travelling valve or plunger:** load picks up slowly on the upstroke and
  bleeds off before the top. **Leaking standing valve:** the load is released slowly
  and late at the start of the downstroke (rounded corner). Leak signatures are subtle
  and I'm less sure of the exact shapes — confirm with a travelling/standing valve
  check (stop the unit on the upstroke/downstroke and watch the load trend).
- **Tagging** (pump hitting bottom) shows a spike at the bottom of the stroke — re-space.
- **Pump-off control:** set the POC fillage setpoint (often around 70–85% of a full card)
  and idle time so the well runs only when there's fluid. Validate with an **acoustic
  fluid level** shot (Echometer-type) and production tests.

## 2. ESP amp charts and VSD data
- A steady, smooth current near nameplate-adjusted normal is healthy.
- **Gas lock / gas interference:** erratic, fluctuating amps, then underload trip.
- **Pump-off (low fluid level):** amps decline gradually to an **underload** trip;
  repeated restarts and trips. Lower frequency, or set restart delays to allow
  inflow — repeated hot restarts shorten motor life.
- **Overload:** rising amps — heavier fluid, solids, scale, mechanical drag. Check BS&W
  and sand; don't just raise the overload setpoint.
- **Intake pressure and motor temperature** from the downhole gauge are the best
  diagnostics where installed. Rising motor temperature with falling flow → poor
  cooling flow past the motor.
- Before restart after a trip, check insulation resistance (phase-to-ground) if
  procedure requires; a falling megger trend warns of cable or motor failure.

## 3. Gas lift
- Gas is injected into the annulus and enters tubing through valves; unloading
  valves open in sequence to work down to the **operating valve**.
- Check: injection rate and pressure stable; casing pressure "heading" or cycling
  means multi-pointing or an unstable valve. Too much gas costs compression with no
  gain past the optimum — do a step-rate test.

## 4. Plunger lift
- The plunger travels with the well's own gas, carrying a liquid slug. Tune the
  controller's off time (build pressure) and afterflow time (produce gas) to keep
  **arrival times** in the target band: too fast arrivals damage the lubricator;
  no arrival means too little energy (more off time).

## Gotchas
- Surface cards can look normal while downhole has a problem; use the downhole card.
- Units out of balance waste energy and gearbox life — check counterbalance.
- Data first, then workover: many "failed pumps" were inflow or setting problems.

## Verify
- [ ] Card shape identified and confirmed with fluid level/test.
- [ ] POC setpoints match well inflow.
- [ ] ESP trip cause classified before restart; insulation trend checked.
- [ ] Gas lift injection stable and near optimum.
- [ ] Plunger arrivals in target band.
