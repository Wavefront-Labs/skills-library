---
id: engineering-technology.agricultural-and-biosystems-engineering.food-process-engineering.drying-air-psychrometric-calculations
name: drying-air-psychrometric-calculations
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: food-process-engineering
tags: [agricultural-and-biosystems-engineering, food-process-engineering, psychrometrics, food-drying, dehydration, humidity-ratio, wet-bulb, enthalpy, drying-air, adiabatic-saturation]
level: practitioner
status: gated
description: "Use the psychrometric chart and equations for humidity ratio, enthalpy and wet-bulb to design drying air heating, airflow and humidity limits in food dryers."
sources:
  - "Toledo, Fundamentals of Food Process Engineering"
  - "Earle, Unit Operations in Food Processing"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Drying air psychrometric calculations

**Goal:** know the air state, how much air a dryer needs and how much heat.

## Key relations
- Humidity ratio `W = 0.622 p_v / (P - p_v)` (kg water per kg dry air).
- Enthalpy `h = 1.006 T + W (2501 + 1.86 T)` kJ/kg dry air (T in C).
- Relative humidity `RH = p_v / p_sat(T)`.
- Wet-bulb temperature approximately equals the adiabatic saturation temperature for air-water mixtures (gated: unconfirmed, source is paywalled or blocked); used for the surface temperature in the constant-rate drying period.
- Dew point: temperature at which p_v equals p_sat.

## Dryer air balance
1. Water to remove: `m_w = m_dry solids x (X1 - X2)` (dry basis X).
2. Air flow: `m_air = m_w / (W_out - W_in)`; choose W_out from allowed outlet RH (leave a margin so product at the exit is not in condensing conditions).
3. Heating the ambient air at constant W from T_amb to T_in: `Q = m_air x c_humid x (T_in - T_amb)` with `c_humid = 1.006 + 1.86 W` kJ/kg K.
4. Adiabatic drying follows a line of constant enthalpy (approx.) toward saturation.
5. Recirculation raises W_in and cuts energy but slows drying; compute the mix.

## Check
At 25 C, 50% RH, 101,325 Pa: W = 0.00988 kg/kg and h = 50.32 kJ/kg, identical from these equations and from the ASHRAE-based psychrolib library (run this session).

## Gotchas
- Elevation changes pressure P and therefore W at a given p_v.
- Use dry-basis moisture for balances and wet-basis for product spec.
- Over-drying wastes energy; outlet air temperature should be monitored.

## Verify
- [ ] Use a validated psychrometric function (e.g. spreadsheet) and confirm against chart readings.
