---
id: engineering-technology.aerospace-engineering.spacecraft-systems-design.spacecraft-emc-testing
name: spacecraft-emc-testing
category: engineering-technology
field: aerospace-engineering
product: spacecraft-systems-design
tags: [emc-testing, electromagnetic-compatibility, mil-std-461, conducted-emissions, radiated-susceptibility, esd]
level: practitioner
status: verified
description: "Plan unit- and system-level EMC testing for spacecraft: emissions and susceptibility tests, grounding and bonding, and launch-site compatibility."
sources:
  - "MIL-STD-461 (EMI requirements and test methods)"
  - "ECSS-E-ST-20-07C (electromagnetic compatibility)"
  - "NASA GSFC-STD-7000"
  - "NASA GSFC-STD-7000B (GEVS), EMC section: https://standards.nasa.gov/standard/gsfc/gsfc-std-7000"
  - "ECSS-E-ST-20-07C Rev.2: https://ecss.nl/standard/ecss-e-st-20-07c-rev-2-electromagnetic-compatibility-3-january-2022/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# EMC testing

**Goal:** units and spacecraft do not interfere with themselves, the launcher or the ground systems.

## Unit-level tests (MIL-STD-461 style test names)
- Conducted emissions on power leads (CE101, CE102).
- Conducted susceptibility to ripple and transients (CS101, CS114, CS115, CS116).
- Radiated emissions electric and magnetic field (RE101, RE102).
- Radiated susceptibility (RS101, RS103).
The tailoring of limits comes from the spacecraft EMC specification and the launch vehicle requirements. ECSS-E-ST-20-07C Rev.2 (3 January 2022) is the European standard framework.

## Spacecraft-level
1. System EMC: self-compatibility with all units on, RF transmitters operating with receivers in the band, and margins (MIL-STD-464C section 5.1 requires a margin of at least 6 dB for safety-critical and mission-critical system functions, as quoted in GEVS; use your standard).
2. Grounding and bonding plan: single-point ground for power, structural bonding resistance requirements (milliohm level), shielded harnesses with correct termination, ESD protection.
3. RF compatibility with the launcher and the launch site (the user's guide gives limits).
4. Magnetic cleanliness for missions with magnetometers: control of magnetic materials and measure the dipole.
5. Charging: surface and internal charging control per the environment (see space environment guidelines).

## Practice
- Test early at unit level when failures are cheaper to fix.
- Use a test configuration that includes the actual harness and loads.

## Gotchas
- A unit passing alone may fail in the system because of cable coupling.
- Switching power supplies are the main source of conducted noise.

## Verify
- [ ] All unit tests meet limits or have approved waivers, and a system-level test records no anomalies in sensitive subsystems.
