---
id: engineering-technology.aerospace-engineering.spacecraft-systems-design.gevs-environmental-test-levels
name: gevs-environmental-test-levels
category: engineering-technology
field: aerospace-engineering
product: spacecraft-systems-design
tags: [spacecraft, environmental-testing, gevs, gsfc-std-7000, protoflight, qualification, acceptance-test, test-margins]
level: practitioner
status: verified
description: "Plan an environmental test campaign from NASA GEVS: qualification, protoflight and acceptance approaches, test types and margins, with confirmation steps for current levels."
sources:
  - "NASA GSFC-STD-7000 (General Environmental Verification Standard, GEVS)"
  - "ECSS-E-ST-10-03C (Testing)"
  - "Launch vehicle user guides"
  - "NASA GSFC-STD-7000B (GEVS): https://standards.nasa.gov/standard/gsfc/gsfc-std-7000"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# GEVS environmental test levels

**Goal:** a verification campaign matched to hardware heritage and risk. Check the current standard and programme requirements for exact levels and durations.

## Approaches
- **Prototype qualification:** a qualification unit is tested above the flight limit level for longer; flight units then get acceptance testing.
- **Protoflight:** the flight unit is tested at qualification amplitudes for acceptance-length durations; common for single-unit missions.
- **Acceptance:** flight units tested at the flight limit level to find workmanship defects.
- GSFC-STD-7000B (GEVS) test factors for random vibration and acoustics: prototype qualification at flight limit level plus 3 dB for 2 minutes per axis; protoflight at limit level plus 3 dB for 1 minute per axis; acceptance at limit level for 1 minute per axis. Structural loads: 1.25 times limit load for qualification and protoflight, 1.0 for acceptance. A plus 6 dB qualification margin is not a GEVS value (it is older expendable-launch-vehicle practice); use the programme and launcher requirements.

## Test types
Mass properties, sine vibration (resonance survey), random vibration, acoustic, shock, thermal vacuum and thermal cycling, EMC/EMI, magnetics, deployment and functional tests, leak tests.

## Procedure
1. Derive maximum predicted environments from the launch vehicle user guide and analysis.
2. Decide the approach per item based on heritage.
3. Write the test plan and procedure; define pass/fail criteria and notches.
4. Perform functional tests before, during and after environmental exposures.
5. Report with traceability to the verification matrix.

## Gotchas
- Using test levels from another programme without reconciling the launcher environment.
- Skipping the post-test functional check.

## Verify
- [ ] Each test level is traceable to the maximum predicted environment with the stated margin.
