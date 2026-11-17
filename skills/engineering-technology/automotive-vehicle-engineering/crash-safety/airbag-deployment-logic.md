---
id: engineering-technology.automotive-vehicle-engineering.crash-safety.airbag-deployment-logic
name: airbag-deployment-logic
category: engineering-technology
field: automotive-vehicle-engineering
product: crash-safety
tags: [deployment-logic, airbag-control-unit, crash-sensing, safing-sensor, delta-v, occupant-classification, restraint-systems]
level: practitioner
status: draft
description: "Build the airbag deployment decision logic: crash-severity algorithms, satellite sensors, safing, belt and occupant inputs, calibration and no-fire verification."
sources:
  - "Kramer, Passive Safety of Vehicles"
  - "ISO 26262 for airbag ECU safety; supplier algorithm application notes"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Airbag deployment logic

1. Inputs: central accelerometer in the airbag control unit, satellite accelerometers and pressure sensors (side), belt buckle switch, seat occupancy/classification, seat position, crash type.
2. Algorithm: compute features of the acceleration signal such as velocity change (integral), windowed integrals, jerk and energy; compare with thresholds as function of time; dual thresholds for belted and unbelted occupants; different thresholds for each stage of multi-stage inflators.
3. Safing: a separate sensor or logic path must agree before any squib ignition, protecting against faults and spurious signals.
4. Calibration: a database of crash events (barriers at several speeds and angles, pole, underride, rough road, misuse events such as hammer and kerb hits) defines fire and no-fire regions with margin; time-to-fire requirements by crash type; sensing time vs the occupant position.
5. Safety: ISO 26262 ASIL requirements for the ECU (airbag ECUs commonly target the highest integrity classes for unintended deployment and failure to deploy; confirm in your HARA), diagnostics for squib loops and sensors.
6. Communication: send crash signal to other ECUs (door unlock, fuel pump cut-off, HV disconnect, eCall).
7. Verify with hardware-in-the-loop playback of recorded crash signals, and with vehicle tests.

**Gotchas:** misuse events (hard kerb strike, underbody hit) must not trigger; confirm in no-fire tests.

## Verify
- [ ] Fire/no-fire matrix passes on recorded crash and misuse data.
- [ ] Time-to-fire margins meet the restraint requirement for each crash mode.
