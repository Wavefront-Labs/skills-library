---
id: engineering-technology.agricultural-and-biosystems-engineering.food-process-engineering.viscometer-measurement-practice
name: viscometer-measurement-practice
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: food-process-engineering
tags: [agricultural-and-biosystems-engineering, food-process-engineering, viscometry, rotational-viscometer, rheometer, brookfield-spindle, couette, wall-slip, thixotropy, flow-curve-measurement, food-rheology]
level: practitioner
status: draft
description: "Measure food rheology properly: geometry choice, temperature control, pre-shear, shear rate range, wall slip, thixotropy, calibration oils and reporting."
sources:
  - "Steffe, Rheological Methods in Food Process Engineering"
  - "ISO standards catalogue (https://www.iso.org)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Viscometer measurement practice

**Goal:** flow curve data that can be trusted to design pumps, pipes and mixers.

## Choose the instrument and geometry
- Rotational rheometers with concentric cylinder, cone and plate or parallel plate give well-defined shear rates. Cone and plate suits smooth fluids; concentric cylinders suit low viscosity and particles; serrated or vane geometries suit gels and fluids with particles and slip.
- Simple spindle viscometers (such as those from Brookfield) give a relative viscosity at an unknown shear rate for non-Newtonian foods; use for quality control only, or calibrate with the mixer-viscometer method (Steffe) for estimates.
- Capillary and tube viscometers for process lines; Bostwick consistometer and flow cups are empirical industry tests.

## Method
1. Control the temperature (jacket or Peltier) and equilibrate the sample.
2. Pre-shear and rest steps to define a reproducible structure; record the sequence because time dependence (thixotropy) matters.
3. Ramp up and down or step the shear rate across the range of the real process; report both.
4. Check for wall slip (compare gap sizes or use a serrated tool) and edge effects, sedimentation and evaporation.
5. Particle size versus gap: gap should be at least about 10 times the largest particle.
6. Calibrate with certified viscosity standard oils at the test temperature; check torque range (data in the lowest 10 percent of the range are unreliable).

## Report
Instrument, geometry, temperature, shear history, rate range, model parameters and standard error.

## Verify
- [ ] Standard oil reading within the stated tolerance.
- [ ] Replicate samples agree.
- Unconfirmed: the tolerance values from your instrument's manual.
