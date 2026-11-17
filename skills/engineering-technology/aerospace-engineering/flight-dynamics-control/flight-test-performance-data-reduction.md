---
id: engineering-technology.aerospace-engineering.flight-dynamics-control.flight-test-performance-data-reduction
name: flight-test-performance-data-reduction
category: engineering-technology
field: aerospace-engineering
product: flight-dynamics-control
tags: [performance-reduction, flight-test-data-reduction, standard-day-correction, specific-excess-power, energy-height, flight-test]
level: practitioner
status: draft
description: "Reduce flight test performance data to standard-day, standard-weight conditions: airspeed and altitude corrections, climb by energy method, and cruise nondimensional methods."
sources:
  - "Kimberlin, Flight Testing of Fixed-Wing Aircraft"
  - "Ward, Performance Flight Testing references (NTPS notes)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Performance data reduction

**Goal:** turn raw flight data into published performance at standard conditions.

## Instrument corrections first
- Indicated to calibrated airspeed (instrument and position error), then to equivalent and true airspeed with density from ambient pressure and temperature.
- Altitude from static pressure (pressure altitude) including position error; temperature from measured total temperature with recovery factor and Mach.

## Cruise
- Use nondimensional parameters so tests at different weights and altitudes collapse: `W/delta`, `V/sqrt(theta)` or Mach, fuel flow `Wf/(delta sqrt(theta))`, with `delta` and `theta` the pressure and temperature ratios.
- Fit specific-range curves and correct to the standard weight and the standard day.

## Climb
- Energy method: specific excess power `Ps = (T - D) V / W`; with data measured as pressure-altitude rate versus time, use the tapeline-altitude correction `(T_actual/T_standard)` and an acceleration factor.
- Correct to standard weight (rate of climb scales with weight through excess power) and to standard day.

## Take-off and landing
- Correct distances for wind, runway slope, temperature, altitude and weight using the standard relations (ground run grows faster than linearly with weight, about as the square at fixed thrust).

## Procedure
1. Edit the data and apply instrument calibrations.
2. Compute true and nondimensional parameters.
3. Apply corrections to standard conditions.
4. Fit and publish with scatter and confidence.

## Gotchas
- Mixed use of density altitude and pressure altitude is a common error.
- Climb tests in turbulent air give noisy rates; use multiple runs.
- Corrections beyond small deviations from the standard are not valid; fly close to the standard conditions.

## Verify
- [ ] Repeat runs at the same nominal condition reduce to results within the instrument accuracy.
