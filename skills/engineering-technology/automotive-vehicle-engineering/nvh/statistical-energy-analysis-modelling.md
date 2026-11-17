---
id: engineering-technology.automotive-vehicle-engineering.nvh.statistical-energy-analysis-modelling
name: statistical-energy-analysis-modelling
category: engineering-technology
field: automotive-vehicle-engineering
product: nvh
tags: [sea-modelling, sea, statistical-energy-analysis, fe-sea, modal-density, coupling-loss-factor, va-one, body-acoustics, high-frequency-noise, power-balance, hybrid-fe-sea]
level: practitioner
status: gated
description: "Build a vehicle SEA model: subsystem definition, modal density and loss factors, power inputs, validity limits at mid-high frequency, FE-SEA hybrids and correlation."
sources:
  - "Harrison, Vehicle Refinement (chapter list)"
  - "Lyon and DeJong, Theory and Application of Statistical Energy Analysis (textbook; confirm edition)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Statistical energy analysis (SEA) modelling

## 1. Idea
At mid and high frequencies the structure and air cavities have many modes, so deterministic FE becomes costly and sensitive. SEA divides the system into subsystems (panels, cavities, beams) and predicts the average vibrational or acoustic energy in each by solving a power balance across coupling loss factors (CLFs), with damping loss factors (DLFs) dissipating energy.

## 2. Equations in brief
For each subsystem i: P_in,i = omega x eta_i x E_i + sum_j omega x (eta_ij E_i - eta_ji E_j), with eta_ij CLFs and consistency relationship n_i eta_ij = n_j eta_ji where n is the modal density (numerically checked: with this relation two coupled lightly damped subsystems reach equal modal energy E/n). Solve the linear system for energies E at each frequency band (third-octave bands typical), then convert energy to SPL (cavity) or velocity (plate).

## 3. Applicability
SEA is valid when each subsystem has enough modes in the band and modal overlap is adequate, meaning roughly above a few hundred hertz for vehicle panels and cavities (gated: unconfirmed, source is paywalled or blocked) (the limit depends on size and damping; the general criterion is several modes per subsystem in the band). Below that, use FE or hybrid FE-SEA (deterministic FE of stiff parts coupled to SEA subsystems) or acoustic FE (see acoustic FE coupling).

## 4. Building a vehicle model
1. **Subsystems:** each major panel (dash, floor, roof, doors, glass, trunk panels) as plate subsystems; cabin and engine bay cavities as acoustic subsystems; exterior as semi-infinite fluid.
2. **Properties:** area, thickness, material, curvature; for composites and laminates use equivalent properties; trim layers as noise control treatments (porous layers, mass layers) via transfer-matrix methods.
3. **Damping loss factors:** from measurement (decay) or damping treatment data.
4. **Sources:** engine and tyre sound power, wind pressure (from CFD or tunnel measurement), road excitation at mounts, as power inputs.
5. **Leaks and seals:** model leak areas as direct paths.

## 5. Use
Compare treatment options early (dB per kg of an acoustic package), predict airborne cabin noise at speed, design for wind noise. Calibrate with measured panel-level TL and cabin SPL, and update loss factors; sensitivity study on uncertain parameters.

## 6. Pitfalls
Missing flanking paths, wrong CLF at corners and joints, ignoring non-resonant transmission, using SEA below its validity range, trim modelled without realistic boundary conditions. Treat results as band-averaged predictions with an uncertainty of several dB (gated: unconfirmed, source is paywalled or blocked).

## Verify
- [ ] Frequency range above the SEA validity limit, or hybrid used.
- [ ] Damping and CLF inputs measured or justified.
- [ ] Sources and leaks represented.
- [ ] Model correlated to a baseline vehicle test.
