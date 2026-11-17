---
id: engineering-technology.biomedical-engineering.biomechanics.knee-wear-simulation-iso-14243
name: knee-wear-simulation-iso-14243
category: engineering-technology
field: biomedical-engineering
product: biomechanics
tags: [iso-14243, orthopaedic-testing, wear-testing, knee-wear, knee-simulator, gravimetric-wear, uhmwpe]
level: advanced
status: gated
description: "Plan a total knee wear simulator test to ISO 14243: kinematic inputs, serum lubricant, gravimetric wear with soak controls, cycles and what to report."
sources: ["ISO 14243-1:2009 and Amd 1:2020 Implants for surgery - Wear of total knee-joint prostheses - Part 1: Loading and displacement parameters for wear-testing machines with load control and corresponding environmental conditions for test (https://www.iso.org/standard/44262.html)", "ISO 14243-2:2016 Part 2: Methods of measurement (https://www.iso.org/standard/69851.html)", "ISO 14243-3:2014 and Amd 1:2020 Part 3: displacement control (https://www.iso.org/standard/77175.html)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Knee wear simulation (ISO 14243)

**Goal:** measure polyethylene wear of a total knee design under standardised, physiologically derived loads, to compare designs and check for unusual wear.

Regulatory use needs the current edition of each part and an accredited laboratory; this note is orientation.

## Setup
- **Input waveforms:** ISO 14243-1 (force control) defines axial force, flexion-extension, anterior-posterior force and internal-external torque over a gait cycle (peak axial force about 2600 N (gated: unconfirmed, source is paywalled or blocked)); ISO 14243-3 gives the displacement-control version. Pick the one your submission or comparison needs.
- **Frequency and duration:** about 1 Hz and 5 million cycles are used in studies citing ISO 14243 (PMC6205607); intermediate measurement interval and the exact requirements per the standard (gated: unconfirmed, source is paywalled or blocked).
- **Lubricant:** diluted bovine serum with the specified protein content, with additives (such as EDTA and an antibiotic) and temperature controlled near body temperature; replace regularly and filter. Confirm the protein concentration in the standard.
- **Samples:** a number of test stations plus **load-soak control stations** (soaked and loaded statically but not cycled) to correct for fluid uptake.

## Measurement
1. Clean (a defined protocol), dry, condition and weigh inserts on a microbalance before test and at each interval.
2. Wear = mass loss of test insert minus the average change of soak controls; convert to volume with density.
3. Report wear rate per million cycles by linear regression after bedding-in, with run-in noted.
4. Inspect surfaces for delamination, pitting and burnishing; photograph; check wear debris if required (ISO 17853 for wear particle isolation (gated: unconfirmed, source is paywalled or blocked)).

## Gotchas
- Fluid uptake of polyethylene masks wear; soak controls are essential.
- Stations differ; randomise component assignment and monitor force and motion tracking.
- Sterilisation and ageing method of the insert change wear; state it.

## Verify
- [ ] Recorded actual waveforms track the inputs within tolerance.
- [ ] Soak control drift documented.
- [ ] Wear rate with confidence interval reported.
