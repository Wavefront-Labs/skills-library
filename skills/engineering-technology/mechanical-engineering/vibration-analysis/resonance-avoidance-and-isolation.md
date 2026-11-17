---
id: engineering-technology.mechanical-engineering.vibration-analysis.resonance-avoidance-and-isolation
name: resonance-avoidance-and-isolation
category: engineering-technology
field: mechanical-engineering
product: vibration-analysis
tags: [vibration, resonance, natural-frequency, modal-analysis, separation-margin, campbell-diagram, vibration-isolation, transmissibility, isolators, static-deflection, damping, balancing, iso-1940, iso-21940, iso-10816, iso-20816, rotor-dynamics, bump-test, impact-test, condition-monitoring, frequency-response, machinery-vibration]
level: practitioner
status: gated
description: "Keep machines off resonance: natural frequency estimates, separation margins, isolator selection from static deflection and transmissibility, ISO balance grades."
sources: ["Rao, Mechanical Vibrations (Pearson)", "Harris' Shock and Vibration Handbook (McGraw-Hill)", "ISO 21940-11 (formerly ISO 1940-1) Mechanical vibration — Rotor balancing — Balance quality requirements", "ISO 20816-1 (formerly ISO 10816-1) Mechanical vibration — Measurement and evaluation of machine vibration", "API 684, Rotordynamic Tutorial"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Resonance avoidance and isolation — design for quiet machines

**Goal:** ensure no structural or rotor natural frequency sits near an excitation
frequency, isolate what must be isolated, and specify balance and acceptance levels.

## 1. List the excitations
Rotating speed 1x (unbalance), 2x (misalignment, reciprocating second order),
blade/vane pass (blades x rpm), gear mesh (teeth x rpm), electrical 2x line frequency
(100/120 Hz in motors), bearing defect frequencies, and the full speed range for VFD
drives. Plot them against speed on a **Campbell (interference) diagram**.

## 2. Estimate natural frequencies
- Single DOF: `fn = (1/2 pi) sqrt(k/m)`. From static deflection: `fn [Hz] ~ 15.76 / sqrt(delta [mm])`
  (e.g. 1 mm sag -> ~16 Hz; 25 mm -> ~3.2 Hz; constant recomputed: g/(2 pi) with g in mm/s2 gives 15.76).
- Beams/plates: closed-form tables (Blevins, Formulas for Dynamics...) for quick checks.
- Real structures: FE modal analysis with realistic boundary conditions (bolted bases are
  softer than "fixed"; include the foundation or frame stiffness and attached masses).
- Confirm on hardware with an **impact (bump) test**: hammer + accelerometer, read peaks
  in the FRF; damping from half-power bandwidth `zeta ~ df / (2 fn)`.

## 3. Separation margin
Keep each natural frequency at least **~10–20 %** away (rule of thumb (gated: unconfirmed, source is paywalled or blocked)) from every excitation in the
operating range (API rotating-equipment practice defines margins based on amplification
factor; use your industry standard where one applies). Lightly damped steel structures
have zeta ~0.01–0.05, so dynamic amplification at resonance `Q ~ 1/(2 zeta)` is 10–50x.
Fixes, in order of effectiveness: change stiffness (gussets, shorter spans), change mass
distribution, change speed range or blade counts, then add damping.

## 4. Isolation
Transmissibility (single DOF): `T = sqrt((1 + (2 zeta r)^2) / ((1 - r^2)^2 + (2 zeta r)^2))`,
`r = f_forcing / fn`. Isolation only begins above `r = sqrt(2)`.
- Target **r >= 3** (about 88 % isolation undamped, `T = 1/(r^2 - 1)`).
- Procedure: lowest forcing frequency f -> fn = f/3 -> required static deflection
  `delta = (15.76/fn)^2` mm -> choose mounts for load per mount and that deflection.
  Example (recomputed): 1480 rpm fan (24.7 Hz) -> fn <= 8.2 Hz -> delta >= ~3.7 mm -> rubber mounts
  marginal, springs comfortable.
- Machines pass through resonance on start-up: add damping or snubbers so transient
  amplitude is limited.
- Centre of gravity: place mounts so the CG is near the elastic centre to avoid coupled
  rocking modes. Support structure must be much stiffer (≥ ~10x) than the isolators, or
  the floor's own resonance comes into play.

## 5. Balancing
Permissible residual unbalance (ISO 21940-11, formerly 1940-1):
`U_per [g mm] = 9549 x G x m [kg] / n [rpm]`. G6.3 for general machinery, fans, pumps;
G2.5 for turbines, compressors, machine-tool drives; G1 for grinders. Split U_per between
correction planes per the standard's rules. Example: 50 kg fan rotor at 1480 rpm, G6.3 ->
U_per ~ 2030 g mm total (recomputed: 2032). The G grades and the 9549 constant come from ISO 21940-11, which is paywalled and could not be fetched (gated: unconfirmed, source is paywalled or blocked); confirm in the standard.

## 6. Acceptance
Measure overall velocity (mm/s RMS, typically 10–1000 Hz) on bearing housings and assess
against ISO 20816 (formerly 10816) zones for the machine class. The older ISO 10816-1
Class I–IV zone limits (e.g. Class II small machines on rigid foundations: A/B ~1.12,
B/C ~2.8, C/D ~7.1 mm/s) are widely quoted (gated: unconfirmed, source is paywalled or blocked); the newer parts use machine-specific values —
check the part for your machine type.

## Verify
- [ ] Campbell diagram covers all excitation orders over the full speed range.
- [ ] Every mode within the range has >= the required separation margin, confirmed by test.
- [ ] Isolators give r >= 3 at the lowest forcing frequency; supporting structure stiff.
- [ ] Balance grade specified and U_per computed per plane.
- [ ] Commissioning vibration within the agreed ISO 20816 zone (typically A/B).
