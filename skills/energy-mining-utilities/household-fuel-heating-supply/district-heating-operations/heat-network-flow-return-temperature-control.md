---
id: energy-mining-utilities.household-fuel-heating-supply.district-heating-operations.heat-network-flow-return-temperature-control
name: heat-network-flow-return-temperature-control
category: energy-mining-utilities
field: household-fuel-heating-supply
product: district-heating-operations
tags: [household-fuel-heating-supply, district-heating-operations, district-heating, heat-network, communal-heating, flow-temperature, return-temperature, delta-t, weather-compensation, differential-pressure, dp-control, index-circuit, heat-interface-unit, hiu, substation, heat-exchanger, bypass, heat-meter, network-losses, leak-detection, make-up-water, water-treatment, boiler-scheduling, heat-pump, chp, thermal-store, cp1, district-heating-operator]
level: advanced
status: draft
description: "Run a district heat network for low return temperatures: weather-compensated flow, differential pressure control, finding bad substations, and leak detection."
sources:
  - "CIBSE/ADE CP1 Heat Networks Code of Practice (UK), concepts paraphrased"
  - "Euroheat & Power / Danish district heating operational guidance, paraphrased"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Heat network flow and return temperature control

**Goal:** deliver enough heat to every customer at the lowest practical flow temperature
and the **lowest possible return temperature** — the single best indicator of a
well-run heat network.

## 1. Why return temperature rules
Heat delivered = flow × ΔT. High return temperature (small ΔT) means pumping more water,
higher heat losses, less efficient boilers/CHP/heat pumps and less thermal store capacity.
Many networks aim for returns well below ~40–50 °C at customer substations; modern
4th-generation networks lower still.

## 2. Flow temperature: weather compensation
- Set flow temperature by outdoor temperature (a compensation curve), with a minimum
  set by domestic hot water needs (often ~ 60–65 °C at the HIU primary side for
  instantaneous DHW with legionella-safe storage elsewhere — check your design).
- Review the curve seasonally against complaints and return temperatures. Higher flow is
  not a cure for a poorly balanced network; it often makes returns worse.

## 3. Differential pressure control
- Pumps controlled to hold a **differential pressure at the index (worst-served) point**,
  not at the plant. Too high: valves noisy, bypasses pass more water, returns rise. Too low:
  far customers go cold.
- Check where the index point actually is — new connections move it.

## 4. Finding bad substations/HIUs
Use heat meter data (flow, flow/return temps, energy) per customer:
- Sort by **volume per MWh** delivered (or average return temperature). The worst 10% often
  cause most of the problem.
- Usual culprits: open or faulty **bypasses** (summer bypasses left on, thermostatic
  bypass set high), failed control valves, fouled plate heat exchangers, poorly set
  secondary radiators (high secondary flow rate), DHW keep-warm functions set too warm.
- Visit, measure primary/secondary temperatures across the HIU heat exchanger; fix
  settings, replace valves/actuators, descale heat exchangers.

## 5. Plant scheduling
Run lowest-cost/lowest-carbon heat first: heat pumps/CHP/waste heat as base load, thermal
store to shift, gas boilers for peak/backup. Low return temperatures improve condensing
boiler and heat pump efficiency directly.

## 6. Leaks and water quality
- Track **make-up water** volume daily — a rise means a leak (or someone draining).
- Find leaks with: pressure-zone isolation, thermal imaging/drone surveys in cold weather,
  leak detection wires in pre-insulated pipe (alarm systems), acoustic methods.
- Water treatment: softened/demineralised make-up, oxygen kept low, pH and conductivity per
  spec; poor water quality corrodes and fouls HIUs. Filters/strainers maintained.

## 7. Customer side
Respond to "no heat/hot water" with a checklist: network pressure/temperature at that
building, HIU status, strainer, valve/actuator, then secondary system. Communicate planned
outages in advance.

## Gotchas
- Heat meters that are wrongly installed (sensors swapped, flow sensor on wrong pipe)
  produce nonsense ΔT — validate meters before chasing "bad" customers.
- Raising flow temperature to fix one cold customer raises losses for everyone.
- Bypasses installed "temporarily" during commissioning often stay open forever.

## Verify
- [ ] Flow temperature follows a reviewed compensation curve.
- [ ] DP held at the true index point.
- [ ] Customers ranked by return temp/volume per MWh; worst actioned.
- [ ] Make-up water trended; leaks investigated; water quality within spec.
- [ ] Network return temperature trending down month on month.

*Uncertain:* target temperatures depend on network generation and DHW design; use your
scheme's design values.
