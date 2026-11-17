---
id: engineering-technology.automotive-vehicle-engineering.ev-battery-systems.reading-a-cell-datasheet
name: reading-a-cell-datasheet
category: engineering-technology
field: automotive-vehicle-engineering
product: ev-battery-systems
tags: [cell-datasheet, datasheet, c-rate, internal-resistance, discharge-curve, cell-specification, nominal-capacity]
level: practitioner
status: draft
description: "Read a lithium-ion cell datasheet critically: test conditions, DCIR, C-rate limits, cycle-life definition, temperature windows and what is missing."
sources:
  - "Plett, Battery Management Systems Vol. 1"
  - "Warner, Lithium-Ion Battery Chemistries and Pack Design"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Reading a cell datasheet

1. **Capacity and voltage:** nominal capacity (Ah) at a specified discharge rate and temperature (often 0.2C-0.5C at 25 C); nominal voltage, upper and lower cut-offs; energy = Ah x V nominal. Typical vs minimum capacity: design with minimum.
2. **Resistance:** DCIR at stated SOC, temperature and pulse duration (for example 10 s at 50% SOC, 25 C). Power capability comes from this; resistance rises at low temperature and at low/high SOC.
3. **Current limits:** continuous and peak charge/discharge currents by temperature window; fast-charge limits vs SOC; the datasheet may give a table by temperature.
4. **Cycle life:** the definition matters: capacity retention (70% or 80%), at what C-rate, temperature, depth of discharge. Compare like with like.
5. **Environmental:** storage and operating temperature ranges, calendar life statement, self-discharge.
6. **Mechanical:** swelling, compression, torque for terminals, weight, dimensions with tolerances.
7. **Safety:** abuse test claims, vent pressure, CID presence.
8. Ask the supplier for what is missing: aged DCIR, thermal data (cp, entropy), OCV curve, hysteresis.

**Gotchas:** datasheet values are typical for fresh cells at 25 C; derate for ageing and cold.

## Verify
- [ ] Design values use minimum capacity and end-of-life DCIR.
- [ ] Every claim has its test condition recorded.
