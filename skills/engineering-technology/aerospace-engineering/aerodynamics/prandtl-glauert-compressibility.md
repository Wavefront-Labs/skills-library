---
id: engineering-technology.aerospace-engineering.aerodynamics.prandtl-glauert-compressibility
name: prandtl-glauert-compressibility
category: engineering-technology
field: aerospace-engineering
product: aerodynamics
tags: [aerodynamics, compressible-flow, gas-dynamics, prandtl-glauert, compressibility-correction, karman-tsien, ackeret, critical-mach]
level: practitioner
status: verified
description: "Apply Prandtl-Glauert, Karman-Tsien and Ackeret corrections to low-speed pressure and lift data, and stop using them where they stop being valid."
sources:
  - "Anderson, Fundamentals of Aerodynamics"
  - "Anderson, Modern Compressible Flow"
  - "Liepmann and Roshko, Elements of Gasdynamics"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Compressibility corrections

**Goal:** convert incompressible pressure or lift data to subsonic compressible conditions.

## Corrections
- Prandtl-Glauert: `Cp = Cp0 / sqrt(1 - M^2)`; `cl = cl0 / sqrt(1 - M^2)`, with `beta = sqrt(1-M^2)`.
- Karman-Tsien (better for higher Mach and higher suction): `Cp = Cp0 / (beta + (M^2/(1+beta)) (Cp0/2))`.
- Supersonic linear theory (thin): `Cp = +/- 2 theta/sqrt(M^2 - 1)`.

## Critical Mach
Estimate the critical Mach by finding where `Cp0_min` (corrected with Karman-Tsien) equals `Cp*` given by
`Cp* = 2/(gamma M^2) [ ((2 + (gamma-1) M^2)/(gamma+1))^(gamma/(gamma-1)) - 1 ]`.
Drag divergence follows somewhat above critical Mach.

## Validity
- Linear subsonic corrections work for thin sections up to about M 0.7-0.8, not in the transonic regime where shocks appear.
- Pressure coefficients blow up as M tends to 1 in the formulas; ignore them there and use CFD or test data.

## Verify
- [ ] At M = 0 correction factors equal 1.
- [ ] Using a thin section, corrected `Cp` agrees with a compressible CFD run at M 0.5 within a few percent.
