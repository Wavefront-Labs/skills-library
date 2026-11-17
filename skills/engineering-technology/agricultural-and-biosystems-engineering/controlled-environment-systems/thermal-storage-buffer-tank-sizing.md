---
id: engineering-technology.agricultural-and-biosystems-engineering.controlled-environment-systems.thermal-storage-buffer-tank-sizing
name: thermal-storage-buffer-tank-sizing
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: controlled-environment-systems
tags: [agricultural-and-biosystems-engineering, controlled-environment-systems, thermal-storage-buffer, greenhouse-heating, greenhouse-cooling, buffer-tank, chp, heat-storage, stratification]
level: practitioner
status: draft
description: "Size a hot-water thermal storage buffer for a greenhouse boiler or CHP: stored energy, charge and discharge, temperature limits and stratification, and the economic case."
sources:
  - "Nelson, Greenhouse Operation and Management"
  - "von Zabeltitz, Integrated Greenhouse Systems for Mild Climates"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Thermal storage buffer tank sizing

**Goal:** decouple heat production from demand to cut peak boiler size, run CHP economically or store solar and waste heat.

## Energy stored
`E = rho V c_p deltaT`. For water, 1 m3 with a 40 K usable temperature difference stores about 46 kWh. A 100 m3 buffer with 40 K therefore holds about 4.6 MWh.

## Sizing approach
1. Determine the heat demand profile for the design days (hourly) and the heat source profile (CHP running hours, boiler capacity, solar or waste heat availability).
2. Choose the tank volume to cover the largest mismatch: for example storing CHP heat produced during the day for night heating. Greenhouse CHP installations in horticulture commonly use buffer volumes in the order of tens of cubic metres per hectare; confirm with a simulation.
3. Select temperature range: hot flow set by the heat source, minimum return by the distribution system; a wider delta T gives more storage per volume.
4. **Stratification**: tall tanks with proper inlet diffusers maintain a hot layer at the top and cold at the bottom; avoid mixing.
5. **Insulation**: heat loss `U A (T - T_ambient)` is a significant continuous loss; choose insulation thickness by economics.
6. **Safety**: pressure vessel or atmospheric tank, expansion, relief, and legionella and corrosion considerations.

## Economics
Compare avoided boiler capacity and fuel savings, electricity market values for CHP flexibility, and tank and installation costs.

## Verify
- [ ] Logged tank temperature profiles through a day confirm that the design storage swing is used.
