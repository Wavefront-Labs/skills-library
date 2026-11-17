---
id: engineering-technology.aerospace-engineering.spacecraft-systems-design.thermal-vacuum-testing
name: thermal-vacuum-testing
category: engineering-technology
field: aerospace-engineering
product: spacecraft-systems-design
tags: [thermal-vacuum, tvac, thermal-balance, thermal-cycling, environmental-testing, gevs]
level: practitioner
status: verified
description: "Plan a spacecraft thermal vacuum test: thermal balance and cycling phases, temperature margins, vacuum level, monitoring and success criteria."
sources:
  - "NASA GSFC-STD-7000 (GEVS)"
  - "Gilmore, Spacecraft Thermal Control Handbook"
  - "NASA GSFC-STD-7000B (GEVS), thermal vacuum section: https://standards.nasa.gov/standard/gsfc/gsfc-std-7000"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Thermal vacuum test

**Goal:** verify the thermal design and workmanship in a space-like environment.

## Phases
- **Thermal cycling / thermal vacuum**: hot and cold plateaus with dwells at temperatures beyond the predicted flight range (a margin is added for qualification and protoflight; the margin and number of cycles come from the programme standard such as GEVS and the project plan; GEVS describes 12 thermal vacuum cycles before flight for flight hardware) with functional tests at each plateau and transitions.
- **Thermal balance**: steady-state hot and cold cases with simulated solar, albedo and infrared inputs (lamps, infrared plates, or heater simulators) to correlate the thermal model.
- **Vacuum**: GEVS gives 1.33e-3 Pa (1e-5 torr) as the pressure below which the vacuum environment is usually sufficiently low; confirm the level specified.

## Procedure
1. Define the test plan from the thermal analysis hot and cold cases, the unit allowable ranges, and test margins.
2. Instrument with thermocouples and the flight thermistors; set pass and fail limits; define abort criteria.
3. Contamination control: bakeout, cold surfaces and a residual gas analyser.
4. Run: pump down, cold and hot plateaus with functional tests, thermal balance, return to ambient with the unit warm to avoid condensation.
5. Correlate the thermal model to the balance data: aim for agreement within the programme's tolerance (a few degrees) and update parameters.
6. Report anomalies, retest and close.

## Gotchas
- Warm the unit before venting to avoid moisture condensation.
- The test is also a workmanship test: cycling reveals solder and bond failures; plan functional tests that exercise all modes.
- Test margins that exceed unit allowables risk damage; coordinate unit qualification ranges.

## Verify
- [ ] Every unit saw its required temperature extreme and passed functional tests at each plateau, and the correlated thermal model matches balance data within the stated tolerance.
