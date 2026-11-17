---
id: engineering-technology.agricultural-and-biosystems-engineering.food-process-engineering.vapor-compression-cycle-analysis
name: vapor-compression-cycle-analysis
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: food-process-engineering
tags: [agricultural-and-biosystems-engineering, food-process-engineering, vapor-compression-cycle, food-refrigeration, cold-chain, p-h-chart, cop, refrigerant, superheat, subcooling]
level: practitioner
status: gated
description: "Analyse a vapour-compression refrigeration cycle on the pressure-enthalpy chart: evaporator and condenser temperatures, superheat, subcooling, COP and compressor capacity."
sources:
  - "Singh & Heldman, Introduction to Food Engineering"
  - "ASHRAE Handbook (Fundamentals and Refrigeration volumes) (https://www.ashrae.org)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Vapour-compression cycle analysis

**Goal:** capacity and energy of a refrigeration plant for food storage or processing.

## Cycle on the p-h chart
1. State 1: compressor suction (saturated vapour plus superheat); state 2: discharge (isentropic compression, corrected by compressor isentropic efficiency); state 3: condenser outlet (saturated liquid plus subcooling); state 4: after expansion valve (same enthalpy as state 3).
2. **Refrigeration effect** `q_e = h1 - h4`; **compressor work** `w = h2 - h1`; `COP = q_e / w`.
3. Mass flow: `m = Q_evap / q_e`; compressor power `W = m (h2 - h1) / eta_mech`.
4. Evaporating temperature typically 5-10 K below the room temperature required (for a coil rating); condensing temperature 10-15 K above ambient or water supply temperature (gated: unconfirmed, source is paywalled or blocked).

## Rules of thumb
- COP falls as lift (condensing minus evaporating temperature) rises: each reduction of condensing temperature by 1 K improves efficiency of the order of 2-3 percent (CoolProp ideal ammonia cycle: +2.7% for 35 to 34 C condensing at -10 C evaporating; +1.9% for 40 to 39 C at -30 C evaporating).
- Superheat protects the compressor; subcooling raises capacity.
- Two-stage compression with intercooling for low evaporating temperatures (freezers).

## Refrigerant choice
Ammonia (R717), CO2 (R744), HFCs and HFOs; regulation (such as the global HFC phase-down) and safety classification (ASHRAE 34) matter (gated: unconfirmed, source is paywalled or blocked); ammonia and CO2 systems have specific safety and design requirements (see the ammonia skill).

## Verify
- [ ] Plot the cycle with measured pressures and temperatures from the plant; calculated capacity matches the energy balance on the chilled medium within 10 percent.
