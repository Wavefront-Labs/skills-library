---
id: engineering-technology.chemical-engineering.piping-instrumentation.temperature-and-pressure-instrument-selection
name: temperature-and-pressure-instrument-selection
category: engineering-technology
field: chemical-engineering
product: piping-instrumentation
tags: [chemical-engineering, piping-instrumentation, pi-instrument-selection, temperature-and-pressure-instrument-selection, temperature-instrument, pressure-transmitter, thermowell, rtd]
level: practitioner
status: gated
description: "Choose temperature and pressure instruments: thermocouples vs RTDs, thermowell design, gauge vs absolute pressure transmitters and seals."
sources:
  - "Crane Technical Paper 410, Perry Chemical Engineers Handbook, ASME B31.3, ISA-5.1, Darby Chemical Engineering Fluid Mechanics, Karassik Pump Handbook"
  - "https://www.isa.org"
  - "https://www.asme.org/codes-standards/find-codes-standards/ptc-19-3-tw-thermowells-performance-test-code"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Temperature and pressure instrument selection

**Goal:** Choose temperature and pressure instruments: thermocouples vs RTDs, thermowell design, gauge vs absolute pressure transmitters and seals.

## Steps
1. RTDs (such as Pt100) are accurate and stable up to a few hundred degrees C; thermocouples cover higher ranges and respond faster; pick the type for the range (gated: unconfirmed, source is paywalled or blocked).
2. Design thermowells for the process pressure and the flow-induced vibration (ASME PTC 19.3 TW, "Thermowells", is the method; confirm the current edition), and the response time.
3. Pressure: choose gauge, absolute or differential, the range with margin (the operating point usually in the middle of the range), and the over-range protection.
4. Use diaphragm seals for corrosive, viscous or clogging fluids and account for the fill fluid effect.
5. Locate instruments for access and with correct impulse line slopes.

## Gotchas
- Thermowell failure by vortex shedding is a known hazard at high velocities.
- Seal systems add error and response time.

## Verify
- [ ] Range covers the normal and the upset values.
- [ ] Thermowell calculation is documented.
