---
id: engineering-technology.mechanical-engineering.hvac-design.cooling-load-calculation
name: cooling-load-calculation
category: engineering-technology
field: mechanical-engineering
product: hvac-design
tags: [hvac, cooling-load, heat-gain, load-calculation, ashrae, ashrae-fundamentals, ashrae-62-1, radiant-time-series, rts, cltd, ventilation, sensible-heat, latent-heat, shr, supply-airflow, psychrometrics, design-conditions, infiltration, solar-heat-gain, shgc, hap, trace, energyplus, air-conditioning]
level: practitioner
status: gated
description: "Peak cooling load per ASHRAE practice: design conditions, envelope, solar, people, lighting, ventilation per 62.1, sensible/latent split and supply airflow."
sources: ["ASHRAE Handbook—Fundamentals, chapter on Nonresidential Cooling and Heating Load Calculations", "ANSI/ASHRAE Standard 62.1, Ventilation and Acceptable Indoor Air Quality", "ANSI/ASHRAE/IES Standard 90.1", "McQuiston, Parker and Spitler, Heating, Ventilating and Air Conditioning: Analysis and Design (Wiley)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Cooling load calculation — peak loads you can size equipment from

**Goal:** a room-by-room and block peak cooling load, split into sensible and latent,
that sets supply airflow per zone and coil/plant capacity without stacked safety factors.

## 1. Inputs
- **Outdoor design**: ASHRAE climatic data for the site — typically 0.4 % or 1 % cooling
  dry-bulb with mean coincident wet-bulb; check a dehumidification (dew-point) case too
  for humid climates.
- **Indoor design**: e.g. 24 C / 50 % RH (adjust to code or brief).
- Geometry, constructions (U-values), glazing (U, SHGC), shading, orientation.
- Schedules for occupancy, lighting, equipment.

## 2. Load components
Use the **Radiant Time Series (RTS)** method (the current ASHRAE manual method) or a
heat-balance program; CLTD/CLF is legacy. Components:

| Component | How |
|---|---|
| Walls/roof conduction | `U A dT` with time-lag via conduction time series |
| Glazing conduction | `U A (To - Ti)` |
| Glazing solar | area x SHGC x incident solar (with shading), radiant part delayed |
| People | office ~75 W sensible + ~55 W latent per person (ASHRAE table, activity-dependent; (gated: unconfirmed, source is paywalled or blocked)) |
| Lighting | installed W/m2 (LED offices often ~5–9 W/m2 (gated: unconfirmed, source is paywalled or blocked)) x use factor |
| Equipment | measured or ASHRAE plug-load density (light office ~5–10 W/m2 (gated: unconfirmed, source is paywalled or blocked)) |
| Infiltration | small for pressurised buildings; per air-change or crack method otherwise |
| Ventilation (coil load) | outdoor air flow x enthalpy difference |

Radiant gains (solar, lights, people's radiant fraction) become cooling load only after
being absorbed by mass and released — that delay is why the peak hour is often
mid-afternoon and differs per facade. Compute several hours/months (west zones peak late,
south zones may peak in autumn at low sun angles).

## 3. Ventilation per ASHRAE 62.1
Breathing-zone outdoor air `Vbz = Rp Pz + Ra Az`. For offices the commonly cited values
are Rp = 2.5 L/s per person and Ra = 0.3 L/s per m2 (office row of the 62.1-2010 breathing-zone table, seen in secondary reports; the standard is paywalled (gated: unconfirmed, source is paywalled or blocked)) — confirm against the edition your
jurisdiction adopts. Divide by zone air-distribution effectiveness, then apply the
multi-zone system efficiency procedure for VAV systems. Outdoor air is usually the
largest latent load in humid climates.

## 4. Air-side relations (sea level, standard air)
- Sensible: `q_s [W] = 1.2 x V [L/s] x dT [K]`  (IP: `1.08 x cfm x dF` Btu/h; the two forms agree, 1.207 W per L/s per K after unit conversion)
- Latent: `q_l [W] = 3.0 x V [L/s] x dW [g/kg]` (IP: `0.68 x cfm x d grains/lb`; converts to 2.96 W per L/s per g/kg, rounded to 3.0 here)
- Total: `q_t [W] = 1.2 x V [L/s] x dh [kJ/kg]` (IP: `4.5 x cfm x dh Btu/lb`; converts to 1.20)

Correct air density for altitude. Supply airflow per zone = room sensible load /
(1.2 x (T_room - T_supply)); with 13 C supply and 24 C room, dT = 11 K.

## 5. From room loads to equipment
- Room loads set zone airflow; the **block load** (simultaneous peak across zones) sizes
  the AHU/chiller — not the sum of zone peaks.
- Add ventilation load, fan heat (supply fan motor in airstream ~ several % of load),
  duct gains and reheat if used.
- Sensible heat ratio of the room (SHR = qs/qt) drives coil leaving condition; low SHR
  (< ~0.75) may need dedicated dehumidification.
- Next step, ducts: equal-friction sizing around 0.8–1 Pa/m with main-duct velocities
  roughly 5–8 m/s in offices for noise (typical practice (gated: unconfirmed, source is paywalled or blocked)) (check NC targets).

## 6. Gotchas
- Stacked margins (on U, people, lights, plus 20 % at the end) produce oversized,
  short-cycling plant with poor humidity control. Use realistic inputs and one stated margin.
- Rules of thumb (m2 per kW) are for checking, never for sizing.
- Do not use the heating design day for cooling or vice versa; heating loads ignore
  internal gains and solar.

## Verify
- [ ] Climate data, indoor setpoints and code edition recorded.
- [ ] Peak hour/month searched per zone, not assumed.
- [ ] Ventilation rates traceable to 62.1 (or local code) with effectiveness applied.
- [ ] Block load < sum of zone peaks; plant sized on block load plus OA and fan heat.
- [ ] Load density compared with a benchmark for the building type and the difference explained.
