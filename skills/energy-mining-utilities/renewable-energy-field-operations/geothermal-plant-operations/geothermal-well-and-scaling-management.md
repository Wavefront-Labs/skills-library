---
id: energy-mining-utilities.renewable-energy-field-operations.geothermal-plant-operations.geothermal-well-and-scaling-management
name: geothermal-well-and-scaling-management
category: energy-mining-utilities
field: renewable-energy-field-operations
product: geothermal-plant-operations
tags: [renewable-energy-field-operations, geothermal-plant-operations, geothermal, production-well, injection-well, reinjection, wellhead-pressure, whp, enthalpy, mass-flow, steamfield, separator, steam-gathering, brine, silica-scaling, calcite-scaling, scale-inhibitor, ph-modification, wellbore-scaling, workover, ncg, non-condensable-gas, h2s, binary-plant, orc, flash-plant, geothermal-operator]
level: advanced
status: draft
description: "Operate geothermal production and reinjection wells: wellhead pressure and enthalpy tracking, silica and calcite scaling control, brine handling and NCG venting."
sources:
  - "DiPippo, Geothermal Power Plants (principles of steamfield and scaling), paraphrased"
  - "IGA / geothermal operator training material on scaling and reinjection, paraphrased"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Geothermal well and scaling management

**Goal:** keep production wells delivering steady steam/brine and reinjection wells
accepting fluid, while preventing the scaling that slowly chokes both.

## 1. What to watch on each well
- **Wellhead pressure (WHP)** and temperature.
- **Mass flow** (steam and brine, via separator or tracer dilution testing).
- **Enthalpy** (kJ/kg) — rising enthalpy can mean boiling in the reservoir/drawdown;
  falling enthalpy can mean cooler reinjected water breaking through.
- **Chemistry**: silica, chloride, pH, gas content, calcium/carbonate; tracer returns.
Plot output curves (WHP vs mass flow); a well producing less flow at the same WHP than its
curve says is likely scaling or damage.

## 2. Calcite scaling (production wells)
Calcite deposits where CO2 flashes out of the brine — the **flash point in the wellbore**.
Signs: declining flow at constant WHP, calipers/go-devil runs showing restrictions.
Controls:
- Downhole **scale inhibitor** injection via capillary tubing below the flash point
  (continuous, dose checked by residual inhibitor tests).
- Operate WHP to move the flash point (with care for overall output).
- Mechanical or acid workover when restrictions reach the planned limit.

## 3. Silica scaling (surface plant and reinjection)
Amorphous silica precipitates as brine cools and concentrates after flashing.
- Keep brine above the **silica saturation temperature** (or saturation index below the
  plant's limit) until reinjection — this sets the minimum separator pressure/outlet temp.
- **pH modification** (acid dosing) slows polymerisation in some plants; needs tight
  control (corrosion if overdosed).
- Retention time matters: brine standing in ponds/tanks deposits silica; keep reinjection
  lines full and flowing.
- Binary (ORC) plants cool brine further; check heat exchanger fouling, approach temps.

## 4. Reinjection wells
Track injectivity index (flow per unit pressure). A falling index = scaling, particulates
or formation damage. Avoid injecting oxygenated or particulate-laden brine; filter if
required. Shut-ins and restarts cause particulate slugs.

## 5. Gas and safety
Non-condensable gases (mainly CO2, with H2S) are extracted at the condenser and vented or
abated. H2S monitoring across the site, alarm points, escape sets; low areas (cellars,
pits) can accumulate CO2/H2S — confined-space rules. Wellhead and steam line work under
permits; high pressure steam and silencer discharges are hazards.

## 6. Steam quality to the turbine
Separator and scrubber performance: carryover of brine/silica to the turbine erodes and
scales blades. Check steam purity (sodium, silica, conductivity) and drain pots.

## Gotchas
- Sudden plant trips cause rapid pressure/temperature swings in wells — thermal cycling
  can damage casing and mobilise scale.
- Changing separator pressure to gain megawatts can cross the silica saturation limit.
- Tracer returns from injection to production wells are the early warning of cooling —
  review them every quarter.

## Verify
- [ ] Output curves and enthalpy trended per well; deviations investigated.
- [ ] Scale inhibitor residual confirmed in produced fluid.
- [ ] Brine temperature/SI kept within silica limit to reinjection.
- [ ] Injectivity index trended; actions triggered at agreed decline.
- [ ] H2S/CO2 monitoring and confined-space controls in place.

*Uncertain:* scaling limits and inhibitor choices are field-specific; these are general
principles, not settings.
