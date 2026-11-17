---
id: engineering-technology.aerospace-engineering.flight-dynamics-control.flight-test-instrumentation
name: flight-test-instrumentation
category: engineering-technology
field: aerospace-engineering
product: flight-dynamics-control
tags: [flight-test-instrumentation, flight-test, air-data-boom, data-acquisition, calibration, irig-106]
level: practitioner
status: draft
description: "Specify a flight test instrumentation system: sensors, sampling and filtering, time synchronisation, calibration and data recording for performance and handling tests."
sources:
  - "Kimberlin, Flight Testing of Fixed-Wing Aircraft"
  - "FAA AC 25-7 (Flight Test Guide for Certification of Transport Category Airplanes)"
  - "IRIG 106 telemetry standards"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Flight test instrumentation

**Goal:** a measurement system whose accuracy suits the test objectives.

## Measurands
- Air data: a nose or wing-tip test boom (pitot-static, angle of attack and sideslip vanes) to avoid fuselage flow errors; static source position error calibration.
- Inertial: accelerometers, rate gyros, an inertial and satellite-aided navigation unit for attitude, velocity and position.
- Control: surface and control-column positions (potentiometers or LVDTs), forces from load cells, trim settings.
- Powerplant: fuel flow, engine speeds and temperatures, torque.
- Loads and structure: strain gauges and accelerometers for loads and flutter work.
- Environment: outside air temperature with recovery-factor correction.

## Design steps
1. Write the test-point list and derive what accuracy each parameter needs.
2. Select sample rates at least several times the highest frequency of interest (choose about 5 to 10 times for time-history analysis), with anti-aliasing filters before sampling.
3. Time-synchronise all channels (IRIG-B time code is common) and record absolute time with every sample.
4. Calibrate each transducer end to end, including signal conditioning and cables, before and after the campaign; record the calibration in the data package.
5. Define the recording and telemetry architecture; telemetry follows IRIG 106 standards where used.
6. Plan data quality checks: dropouts, spikes, offsets, signal-to-noise.

## Gotchas
- Lag between channels from different filters biases system identification and flutter damping estimates; characterise filter delays.
- Boom flexibility and local flow distort angle-of-attack measurements.
- Certification test requirements and means of compliance come from the airworthiness authority and its guidance such as AC 25-7D (2018).

## Verify
- [ ] An end-to-end calibration check shows each channel within its accuracy budget.
