---
id: engineering-technology.agricultural-and-biosystems-engineering.food-process-engineering.tray-and-tunnel-dryer-sizing
name: tray-and-tunnel-dryer-sizing
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: food-process-engineering
tags: [agricultural-and-biosystems-engineering, food-process-engineering, dryer-sizing, food-drying, dehydration, tray-dryer, tunnel-dryer, cabinet-dryer, dryer-efficiency, air-velocity]
level: practitioner
status: draft
description: "Size a tray, cabinet or tunnel dryer: product load, water removal, airflow and velocity, heat input, efficiency and counter or co-current choice."
sources:
  - "Toledo, Fundamentals of Food Process Engineering"
  - "Earle, Unit Operations in Food Processing"
  - "Chakraverty & Singh, Postharvest Technology and Food Process Engineering"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Tray and tunnel dryer sizing

**Goal:** dryer volume, airflow and heat to meet the daily throughput.

## Steps
1. **Throughput and drying time**: from the drying curve (see that skill) choose conditions; batch throughput = load per tray x number of trays / cycle time (including loading, unloading and cleaning).
2. **Water to remove** per batch from the moisture change.
3. **Airflow**: from the psychrometric balance (see psychrometrics skill) and from velocity: tray dryers typically run about 1-5 m/s across trays, with uniform distribution plenum and baffles; check the pressure drop and fan power.
4. **Heat**: `Q = m_air c_humid (T_in - T_amb)` plus product heating and losses, divided by heater efficiency. Specific energy (kJ per kg water evaporated) of 4,000-6,000 for convective dryers is a typical order; use measured values.
5. **Configuration**: co-current gives gentler final drying for heat-sensitive products; counter-current gives higher efficiency and drier product.
6. **Recirculation** fraction and exhaust humidity set energy use; heat recovery from exhaust is an option.
7. **Uniformity**: tray position effects; reverse airflow or rotate trays; target moisture spread within specification.

## Gotchas
- Overloaded trays or poor spacing block airflow.
- Condensation on cold walls and ducts leads to mould and corrosion.
- Hygienic design: washable plenum surfaces and drainage.

## Verify
- [ ] Moisture variation across trays within specification and the measured energy per kg water within 20 percent of design.
