---
id: engineering-technology.automotive-vehicle-engineering.ev-battery-systems.battery-warranty-capacity-modelling
name: battery-warranty-capacity-modelling
category: engineering-technology
field: automotive-vehicle-engineering
product: ev-battery-systems
tags: [battery-warranty, warranty, capacity-warranty, state-of-health, monte-carlo, usage-profile, battery-lifetime, soh-buffer, battery-ageing]
level: practitioner
status: draft
description: "Model battery capacity warranty risk: define SoH, build customer usage distributions, run Monte Carlo ageing, and set pack buffers and thresholds for the target percentile."
sources:
  - "Plett, Battery Management Systems Vols 1 and 2"
  - "Warner, Lithium-Ion Battery Chemistries and Pack Design (chapter list)"
  - "Ehsani et al., Modern Electric Hybrid Electric and Fuel Cell Vehicles (chapter list)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Battery warranty capacity modelling

## 1. Define the promise precisely
Battery warranties typically state a minimum retained capacity (SoH) after a number of years or kilometres, whichever comes first; the numbers differ by manufacturer and market, so take them from the programme requirement. Define SoH measurement: which test, temperature, discharge rate, how the vehicle reports it, and what counts as failure (capacity, energy or power).

## 2. Inputs
- **Usage distribution:** annual distance, trip length, charging habits (AC vs DC fast share), SoC window, parking temperature, climate region. Use fleet telematics or market studies; represent severe users (high percentiles).
- **Ageing model:** calendar and cycle models (see calendar vs cycle ageing) validated on cells and packs, with parameter uncertainty and cell-to-cell spread.
- **Pack effects:** series string limited by the worst cell, thermal gradient, balancing quality.

## 3. Simulation
Monte Carlo: sample usage and parameter sets, run the ageing model over the warranty period, and obtain the distribution of SoH at warranty end. Report the percentage of vehicles below the threshold, not just the mean.

## 4. Design actions
- **Buffers:** hold back usable capacity at beginning of life (hidden top and bottom) and release it with ageing so displayed capacity falls less; the trade-off is cost and initial range.
- **Charge and thermal management:** limit dwell at high SoC, precondition, protect fast charging.
- **Reporting accuracy:** make the SoH estimator accurate (see SoH estimation) so warranty decisions are not driven by estimation error.
- **Financial view:** replacement cost times predicted failure rate guides cell choice and buffer size.

## 5. Validate
Compare early-field data with the prediction; update the model with fleet data; monitor outlier packs. Claim criteria wording belongs to the legal and commercial owners.

## Verify
- [ ] SoH definition and test method specified and consistent with BMS reporting.
- [ ] Usage distribution sourced and tail users represented.
- [ ] Monte Carlo includes parameter uncertainty.
- [ ] Buffer strategy and its range cost quantified.
