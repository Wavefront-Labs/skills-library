---
id: engineering-technology.automotive-vehicle-engineering.crash-safety.material-cards-and-strain-rate
name: material-cards-and-strain-rate
category: engineering-technology
field: automotive-vehicle-engineering
product: crash-safety
tags: [material-card, strain-rate, cowper-symonds, piecewise-linear-plasticity, mat-24, gissmo, failure-model, anisotropy, tensile-test, crash-cae, material-characterisation]
level: practitioner
status: gated
description: "Build a crash material card: strain-rate hardening, failure model, anisotropy, test data processing, and validation by component tests, with a worked Cowper-Symonds form."
sources:
  - "LS-DYNA user manual contents (keyword manual volumes I-III; vendor documentation at https://www.ansys.com)"
  - "Kramer, Passive Safety of Vehicles (chapter list)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Material cards and strain rate

Cowper-Symonds constants (C = 40.4 per second, p = 5), the strain-rate range, and the LS-DYNA MAT_24 and GISSMO references come from memory of the literature and manuals (gated: unconfirmed, source is paywalled or blocked).

## 1. What the card must capture
Yield and hardening up to large strains, **strain-rate sensitivity** (crash strain rates are typically from about 10 to several hundred per second in deforming zones), **failure** (necking, localisation and fracture), and where relevant anisotropy and temperature (hot-stamped steels, aluminium).

## 2. Test data
- Quasi-static tensile in rolling, diagonal and transverse directions (anisotropy r-values).
- High-rate tensile tests (servo-hydraulic machines or split Hopkinson for higher rates) at several strain rates.
- Large-strain data beyond necking: inverse identification by FE of the tensile test, or bulge test or shear tests.
- Failure tests: notched tensile, shear, hole expansion, three-point bend with varying triaxiality.
Process to true stress-true plastic strain, smooth, extrapolate hardening beyond uniform elongation with Swift/Voce or combined laws, then calibrate by simulating the tensile test.

## 3. Strain-rate models
- **Cowper-Symonds:** sigma = sigma_static x [1 + (strain_rate / C)^(1/p)]. Widely quoted constants for mild steel are C = 40.4 per second and p = 5 (check the literature for your steel; AHSS has lower rate sensitivity and different constants).
- **Tabulated rate curves:** the piecewise-linear plasticity model (LS-DYNA MAT_24) with a table of stress-strain curves at several rates is more accurate and is the usual practice.
Include a rate limit and smoothing so spurious high rates at tiny elements do not blow up the stress.

## 4. Failure
Use a damage model with triaxiality and Lode-parameter dependence (for example GISSMO in LS-DYNA, or comparable models in other solvers), with mesh-size regularisation, calibrated at the element size used in the crash models. Account for heat-affected zones near welds with softened properties. Edge-cracking in AHSS needs hole-expansion-based criteria.

## 5. Validate before using
Run component tests (hat-section axial crush, three-point bending) and compare force-displacement and fold pattern. Check mesh-size dependence. Document the card source, test lot and validity range.

## Verify
- [ ] Test data cover the real strain-rate and triaxiality range.
- [ ] Tensile test simulated to reproduce curves.
- [ ] Failure model regularised for the production mesh size.
- [ ] Component test validation recorded.
