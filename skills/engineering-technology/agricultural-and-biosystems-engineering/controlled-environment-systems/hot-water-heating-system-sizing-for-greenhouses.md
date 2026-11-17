---
id: engineering-technology.agricultural-and-biosystems-engineering.controlled-environment-systems.hot-water-heating-system-sizing-for-greenhouses
name: hot-water-heating-system-sizing-for-greenhouses
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: controlled-environment-systems
tags: [agricultural-and-biosystems-engineering, controlled-environment-systems, hot-water-heating, greenhouse-heating, greenhouse-cooling, boiler-sizing, heating-pipes, condensing-boiler, zone-control]
level: practitioner
status: draft
description: "Size a hot-water greenhouse heating system: boiler capacity from design load, pipe length and output, flow and return temperatures, pumps, mixing and zoning."
sources:
  - "Nelson, Greenhouse Operation and Management"
  - "von Zabeltitz, Integrated Greenhouse Systems for Mild Climates"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Hot-water heating system sizing for greenhouses

**Goal:** a distribution system that holds temperature at the design heating load.

## Steps
1. **Design heat load** `Q` (see the envelope skill) including infiltration; add a margin for boiler cycling, pipe losses and future expansion (often 10-25 percent).
2. **Boiler**: choose capacity at or above Q with turndown; multiple boilers staged for efficiency and redundancy. Condensing boilers need low return temperature (return below about 55 C for natural gas) to achieve efficiency gains.
3. **Distribution pipes**: bare steel, plastic or aluminium finned tubes; mounting positions (rail pipes along gutters or crop rows, bench heating, floor heating, perimeter). Pipe output (W/m) depends on pipe diameter and the temperature difference between pipe surface and air; use the supplier's tables.
4. **Flow and return temperatures**: common design flow temperatures 60-80 C with a 10-20 K drop; the pipe length required is `L = Q / (q per metre)`.
5. **Flow rate**: `m = Q / (c_p x deltaT)` (water c_p 4.18 kJ/kg K); choose pipe diameters for velocity of about 0.5-1.5 m/s and pump head from friction losses; balance branches with valves.
6. **Control**: mixing valves for flow temperature, zone valves for compartments, weather compensation, and safeties (high-limit, low water cut-off, expansion vessel, pressure relief).
7. Boiler installation and gas or oil connections must meet local codes and be done by licensed installers.

## Gotchas
- Insufficient pipe length at the design day leads to underheating.
- Water treatment (corrosion inhibitors) and air removal.

## Verify
- [ ] Commissioning test heats the house at the design outdoor temperature (or scaled) to the set-point.
