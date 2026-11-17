---
id: engineering-technology.agricultural-and-biosystems-engineering.controlled-environment-systems.sensible-and-latent-heat-and-moisture-balance
name: sensible-and-latent-heat-and-moisture-balance
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: controlled-environment-systems
tags: [agricultural-and-biosystems-engineering, controlled-environment-systems, moisture-balance, enclosure-heat-balance, ce-psychrometrics, sensible-heat, latent-heat, ventilation-rate, humidity-ratio]
level: practitioner
status: verified
description: "Set up steady-state sensible heat and moisture balances for a greenhouse or livestock house to find the ventilation rate that holds temperature and humidity targets."
sources:
  - "ASHRAE Handbook (Fundamentals) (https://www.ashrae.org)"
  - "Albright, Environmental Control for Animals and Plants (ASAE)"
  - "MWPS Midwest Plan Service, Structures and Environment Handbook"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Sensible and latent heat and moisture balance

**Goal:** the ventilation rate that removes heat and moisture produced inside an enclosure.

## Balances
- **Sensible**: `Q_s,produced + Q_solar + Q_heater = U A (T_in - T_out) + rho c_p V (T_in - T_out)` where V is the ventilation airflow (m3/s), rho about 1.2 kg/m3, c_p about 1006 J/kg K. The ventilation term simplifies to about `1200 V (T_in - T_out)` in W.
- **Moisture**: `m_w,produced = rho V (w_in - w_out)` where w is the humidity ratio (kg/kg dry air). Moisture sources: animals (latent heat share), crop transpiration, wet floors, evaporative cooling, humidifiers. Latent heat of vaporisation is about 2.45 MJ/kg.
- Solve for V from each balance and use the larger as the design ventilation rate for that season.

## Heat and moisture production data
Use published production values for animals (for example the CIGR heat and moisture production reports, which give sensible and latent heat per animal by species, weight and temperature) and for crops (transpiration as a fraction of absorbed solar energy; a large share of absorbed solar energy in summer, lower in winter (the fraction depends on crop and canopy; use measured data)).

## Use by season
- **Winter**: minimum ventilation controls moisture, ammonia and CO2; heat must be provided if the sensible balance is negative at that rate.
- **Summer**: maximum ventilation controls the temperature rise above outdoors (design rises are set by the handbook or code for the species or crop; they are small, a few kelvin).

## Gotchas
- Humidity ratio at outdoors in cold weather is much lower than at 20 C, so the moisture balance often sets minimum ventilation.
- Use a psychrometric chart or function to convert RH to w; do not average RH.

Check (computed): rho c_p = 1.2 x 1006 = 1207 J/m3 K, so the 1200 V rule holds; latent heat of vaporisation at 20 C = 2501 - 2.361 x 20 = 2454 kJ/kg, so 2.45 MJ/kg holds.

## Verify
- [ ] Measured indoor temperature and RH match the calculation within a few percent after commissioning.
