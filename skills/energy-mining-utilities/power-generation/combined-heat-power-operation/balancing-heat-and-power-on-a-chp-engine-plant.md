---
id: energy-mining-utilities.power-generation.combined-heat-power-operation.balancing-heat-and-power-on-a-chp-engine-plant
name: balancing-heat-and-power-on-a-chp-engine-plant
category: energy-mining-utilities
field: power-generation
product: combined-heat-power-operation
tags: [combined-heat-power-operation, power-generation, chp, cogeneration, cogen, district-heating, district-energy, gas-engine, reciprocating-engine, jenbacher, mwm, heat-recovery, jacket-water, exhaust-heat-exchanger, thermal-store, heat-led, electricity-led, dump-radiator, return-temperature, delta-t, spark-spread, quality-index, chpqa, part-load, engine-derate]
level: practitioner
status: draft
description: "Run a gas-engine CHP plant to balance heat and electricity: heat-led vs power-led dispatch, thermal stores, return temperature, dump radiators and the signs your efficiency is quietly leaking away."
sources: ["CHPQA guidance (UK) — quality index concept (paraphrased)", "Engine OEM heat-recovery manuals (general structure)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Balancing heat and power on a CHP engine plant

**Goal:** run a combined heat and power plant (typically gas engines from 0.5 to
10 MWe each, feeding a district heating loop or a site) so that heat and electricity
are both used, the engines stay healthy and the plant earns its efficiency case.
Electricity is easy to export; **heat that nobody uses is the plant's real enemy.**

## 1. Know where the heat comes from
A gas engine turns roughly 40–45 % of fuel into electricity and 40–50 % into
recoverable heat (figures vary by engine and temperature levels):
- **Jacket water / oil cooler / intercooler HT stage** — low-grade heat, ~80–95 °C.
- **Exhaust heat exchanger** — high-grade, gas in at ~400–500 °C, can make hot water
  or steam.
- **LT intercooler** — low temperature (~40 °C); usually dumped unless there is a
  low-temperature use.
Heat goes to the customer via a plate heat exchanger; anything the loop can't take
goes to the **dump (emergency) radiator** or the engine trips on high jacket
temperature.

## 2. Pick the dispatch mode
- **Heat-led:** engines follow heat demand; electricity is a by-product. Best
  efficiency, the norm for district heating.
- **Electricity-led:** engines follow a power price or site demand; surplus heat
  goes to store or dump. Only worth it when the **spark spread** (power price minus
  gas cost per unit of output) clearly pays for the wasted heat.
- In practice: run on price signals, with the **thermal store** as the buffer that
  lets you generate when power is valuable and supply heat later.

## 3. Use the thermal store properly
- A stratified hot-water tank: hot at the top, cool at the bottom. Charge from the
  top, draw cool water from the bottom to the engines.
- Watch the **thermocline**: if the bottom sensor reads hot, the store is full — the
  engines will soon see high return temperature and either derate or dump heat.
- Plan charging ahead of known demand peaks (morning heating), discharge during
  peaks so engines aren't asked to swing.

## 4. Return temperature is everything
- Engines need cool return water (often below ~70 °C at the heat-recovery inlet;
  check OEM). A high network return temperature means less heat can be taken, so
  the dump radiator runs and efficiency falls.
- Causes of high return: customer substations with poorly set or stuck valves,
  bypasses left open, oversized pumps forcing flow. Fixing customer substations is
  often the biggest efficiency gain in the system.
- Track the network **delta-T** (flow minus return); falling delta-T over weeks is an
  early warning.

## 5. Engine health at part load
- Gas engines prefer high load; repeated starts and long low-load running increase
  wear, oil consumption and emissions. Prefer fewer engines at higher load to many at
  low load.
- Stagger running hours across units to plan overhauls; log oil analysis results.
- Watch for derates from high charge-air temperature or knock — often a cooling
  problem upstream (fouled LT cooler).

## Gotchas
- A dump radiator running continuously is a symptom, not a setting; find why heat
  isn't being taken.
- Low gas pressure or quality changes (biogas, gas-grid blending) cause knock-related
  derates — check gas analysis before blaming the engine.
- Grid export limits (G99 in the UK, utility interconnection agreements elsewhere)
  cap electrical output regardless of heat demand.
- Uncertain: temperature thresholds and efficiencies vary widely by engine model and
  design — confirm against OEM data.

## Verify
- [ ] Dispatch mode (heat-led or electricity-led) chosen and justified for the period.
- [ ] Thermal store charge state known and planned against demand peaks.
- [ ] Return temperature to engines below OEM limit; dump radiator duty logged and explained.
- [ ] Network delta-T trended weekly.
- [ ] Engines run at efficient load with balanced running hours.
