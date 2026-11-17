---
id: engineering-technology.agricultural-and-biosystems-engineering.controlled-environment-systems.co2-enrichment-dosing-and-safety
name: co2-enrichment-dosing-and-safety
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: controlled-environment-systems
tags: [agricultural-and-biosystems-engineering, controlled-environment-systems, co2-enrichment, carbon-dioxide-enrichment, co2-dosing, co2-safety, burner-co2, greenhouse-co2, climate-control]
level: practitioner
status: verified
description: "Plan CO2 enrichment for greenhouses: targets, dosing rate from volume and ventilation loss, sources, controls, and safety limits for people and burner contaminants."
sources:
  - "NIOSH Pocket Guide to Chemical Hazards: carbon dioxide (https://www.cdc.gov/niosh/npg/npgd0103.html)"
  - "ASABE Standards, Engineering Practices and Data (https://www.asabe.org)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# CO2 enrichment dosing

**Goal:** raise the CO2 concentration when it pays, using the least gas, and keep people safe.

## When it pays
Ambient CO2 is roughly 400-430 ppm. Photosynthesis benefits from higher concentrations when light and temperature are not limiting, and when the vents are closed enough to hold the gas. Published studies support about 800-1000 ppm with vents closed (a Japanese horticultural study; Dutch tomato work found 400 to 1000 ppm raised net photosynthesis about 51 percent), and grower guidance caps enrichment at roughly 1,000-1,200 ppm when not ventilating and enriches when the house is below ambient. With vents open, holding near ambient (about 400 ppm) is the practical aim because of losses. The exact target depends on crop and economics, so use the crop guide.

## Dosing calculation
- Gas required to raise the concentration by dC in a volume V: mass = V x dC x density factor (at 20 C and 1 atm, 1 ppm of CO2 is 44.01 g/mol / 24.06 L/mol = 1.83 mg per m3; computed).
- Plus replacement of the leakage and ventilation losses: dosing rate must balance ventilation air exchange (air-exchange rate x volume x concentration difference) plus crop uptake.
- Plant uptake is large in bright light; dosing is controlled by light and by ventilation state.

## Sources
- Pure liquid CO2 in a tank with a vaporiser, flow controller and distribution tubes: clean, controlled; bulk delivery.
- Combustion gas from natural gas boilers or burners with a clean combustion and flue gas treatment: low-cost where heat is needed; the flue gas must be free of ethylene, NOx and CO at harmful levels; check combustion tuning.
- Not suitable: unvented kerosene or poorly tuned burners, and exhaust from engines.

## Controls
Controller closes the dosing valve when vents open beyond a threshold, when the CO2 sensor reads above the setpoint, or when it is dark; use sensors in the crop area (`aspirated-sensor-placement-and-calibration`).

## Safety
CO2 is an asphyxiant and toxic at high concentration; occupational limits apply. In the US, OSHA's PEL is 5,000 ppm (8-hour TWA) and NIOSH's REL is 5,000 ppm TWA with a 30,000 ppm short-term limit; NIOSH lists 40,000 ppm as IDLH (NIOSH Pocket Guide, fetched). OSHA sets no short-term PEL. Other jurisdictions differ, so confirm with your workplace safety authority. Install fixed CO2 alarms at head height in enclosed rooms, with ventilation interlock, never enter a room with a gas leak; ventilate dosing rooms and tank enclosures. Liquid CO2 handling needs training and PPE.

## Verify
- [ ] Sensor span-checked against a known gas.
- [ ] Alarm test and ventilation interlock test.
