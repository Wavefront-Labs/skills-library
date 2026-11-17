---
id: engineering-technology.automotive-vehicle-engineering.nvh.accelerometer-and-microphone-setup
name: accelerometer-and-microphone-setup
category: engineering-technology
field: automotive-vehicle-engineering
product: nvh
tags: [nvh-sensors, accelerometer, microphone, iepe, mass-loading, calibration, transducer-mounting, nvh-measurement]
level: practitioner
status: gated
description: "Set up NVH measurement transducers: IEPE accelerometers, mounting and mass loading, microphones and calibrators, cable and grounding, and a check routine."
sources:
  - "Brüel and Kjær technical documentation on accelerometers and microphones"
  - "Harrison, Vehicle Refinement"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Accelerometer and microphone setup

1. **Accelerometers:** IEPE (constant-current powered; typical excitation current (gated: unconfirmed, source is paywalled or blocked)) are typical; choose sensitivity and range for expected levels (e.g. 100 mV/g for general body work (gated: unconfirmed, source is paywalled or blocked), lower for high-g); triaxial for 3-D.
2. Mounting: stud or adhesive/wax; mounting on a clean flat surface; resonance of the mount limits the upper frequency; keep the cable strain-relieved.
3. **Mass loading:** the sensor mass must be small relative to the structure at the measurement point (rule of thumb under 10% of local modal mass (gated: unconfirmed, source is paywalled or blocked)); check on thin panels.
4. **Microphones:** pre-polarised condenser types; free-field vs pressure vs diffuse-field response depends on the use; in-cabin measurements use pressure-type or diffuse-field microphones; binaural head for psychoacoustics.
5. Calibration: acoustic calibrator (commonly 94 dB at 1 kHz; 1 Pa re 20 uPa = 93.98 dB, computed) before and after; accelerometer calibrator (shaker) at 159.2 Hz (1000 rad/s, computed) with 10 m/s^2 (about 1.02 g) or 1 g, per the calibrator's certificate, for sensitivity check.
6. Cabling: low-noise coax, avoid ground loops (single-point grounding), keep cables away from HV lines (EV) to avoid pick-up.
7. Sample rate at least 2.56 times (common analyser convention (gated: unconfirmed, source is paywalled or blocked)) the highest frequency of interest with anti-alias filtering; check for clipping with headroom.
8. Log metadata: sensor IDs, positions, calibration values, temperature.

**Gotchas:** sensor cables moving create noise; moisture on connectors.

## Verify
- [ ] Calibrator check passes within tolerance before and after the session.
- [ ] Time history shows no clipping or DC drift.
