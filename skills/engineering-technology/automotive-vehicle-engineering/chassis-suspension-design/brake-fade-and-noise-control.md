---
id: engineering-technology.automotive-vehicle-engineering.chassis-suspension-design.brake-fade-and-noise-control
name: brake-fade-and-noise-control
category: engineering-technology
field: automotive-vehicle-engineering
product: chassis-suspension-design
tags: [brake-fade, brake-noise, brake-squeal, brake-judder, pad-friction, fluid-boiling, brake-fluid, complex-eigenvalue, brake-sizing, thermal-fade]
level: practitioner
status: gated
description: "Diagnose and prevent brake fade (friction, fluid, mechanical) and control squeal, groan and judder: material choice, thermal limits, CEA, dynamometer tests."
sources:
  - "Limpert, Brake Design and Safety (chapter list)"
  - "Limpert, Brake Design and Safety; SAE J2521 and J2522 dynamometer test procedures (confirm current editions); FMVSS 116 (brake fluids)"
  - "https://www.law.cornell.edu/cfr/text/49/571.116"
  - "https://www.ecfr.gov/current/title-49/part-571/section-571.116"
  - "https://saemobilus.sae.org/standards/j2521_202210-inertia-dynamometer-brake-squeal-noise-test-procedure-vehicles-without-regenerative-systems"
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# Brake fade and noise control

Safety-critical component. Use supplier data and qualified brake engineers for release decisions.

## 1. Fade types
- **Friction fade:** pad friction coefficient falls at high temperature (binder and organic decomposition, gas film); recovers when cool. Pad compound choice sets the temperature window; verify mu vs temperature curve.
- **Fluid fade:** brake fluid vapour forms at its boiling point (reduced by water absorbed over service life), giving a long, soft pedal. DOT 3, 4, 5.1 fluids differ in dry and wet boiling points (FMVSS 116 minimum equilibrium reflux boiling points: DOT 3 205 C dry / 140 C wet, DOT 4 230 C / 155 C, DOT 5.1 260 C / 180 C; other specifications may differ, check current numbers). Keep caliper and fluid temperatures below the wet boiling point with margin on the worst-case hill descent.
- **Mechanical fade:** drum expansion or caliper deflection raising pedal travel.
- **Green fade:** new pads outgassing before burnish.
Design from the energy side: see disc thermal capacity.

## 2. Tests for fade
Hill descent and repeated high-speed stops (the vehicle or dynamometer sequence from your standard or regulation), measuring mu, pedal force, temperature. Dynamometer procedures such as SAE J2522 (Dynamometer Global Brake Effectiveness) are widely used for effectiveness and fade characterisation; confirm the edition your customer requires (SAE text is paywalled (gated: unconfirmed, source is paywalled or blocked)).

## 3. Noise types
- **Squeal (above about 1 kHz; J2521 counts squeal as at least 70 dB(A) peak noise above 1.25 or 2 kHz depending on set-up):** friction-induced instability where two disc/caliper/pad modes coalesce; predicted by complex eigenvalue analysis (CEA) in FE.
- **Groan, moan (low frequency):** stick-slip at low speed and light pressure.
- **Judder:** disc thickness variation (DTV) from uneven wear or thermal deformation gives pedal and wheel vibration at wheel orders.

## 4. Countermeasures
- Squeal: shims and damping layers on the pad back, chamfers and slots, pad geometry changes, mass and stiffness changes of caliper and carrier, compressibility of pad material, friction-material tuning. Validate with a noise dynamometer test procedure (such as SAE J2521, titled Inertia Dynamometer Brake Squeal Noise Test Procedure for Vehicles without Regenerative Systems in its 2022 edition; earlier editions were titled Disc and Drum Brake Dynamometer Squeal Noise Matrix) and with vehicle tests over temperature and humidity.
- Judder: control disc runout and thickness variation at assembly (hub runout, mating faces), pad deposition, cast iron grade and cooling.
- Run CEA early; correlate with a test; do not rely on CEA alone, because it over-predicts unstable modes.

## Verify
- [ ] mu vs temperature, fade and recovery measured on dynamometer and vehicle.
- [ ] Fluid temperature margin on the worst hill descent below the wet boiling point.
- [ ] Squeal tested across temperature, humidity and wear states.
- [ ] Disc runout and DTV limits specified and audited.
