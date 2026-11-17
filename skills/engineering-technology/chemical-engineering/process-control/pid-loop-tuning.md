---
id: engineering-technology.chemical-engineering.process-control.pid-loop-tuning
name: pid-loop-tuning
category: engineering-technology
field: chemical-engineering
product: process-control
tags: [chemical-engineering, process-control, pid, pi-controller, loop-tuning, controller-tuning, bump-test, step-test, fopdt, first-order-plus-dead-time, simc, skogestad, lambda-tuning, imc, ziegler-nichols, cohen-coon, integrating-process, level-control, cascade-control, proportional-band, reset, derivative-filter, dcs, plc, isa-5.1]
level: practitioner
status: gated
description: "Tune PID loops from a bump test: FOPDT model fit, SIMC/lambda tuning rules, controller form and units, loop-type defaults, cascade order and tuning checks."
sources:
  - "Skogestad, S. (2003) Simple analytic rules for model reduction and PID controller tuning, Journal of Process Control 13(4):291-309, https://doi.org/10.1016/S0959-1524(02)00062-8"
  - "https://skoge.folk.ntnu.no/publications/2003/tuningPID/"
  - "Seborg, Edgar, Mellichamp and Doyle, Process Dynamics and Control (textbook, method only)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PID loop tuning from a bump test

**Goal:** tune a loop from a measured model so it is fast enough, robust to model error,
and doesn't oscillate, instead of trial-and-error on a running plant.

## 1. Before tuning: check the loop is tunable
- Valve: stroke it in manual. Stiction or deadband > ~1% shows up as a stair-step or limit
  cycle; no tuning fixes it. Check sizing (valve not at 5% or 95% open).
- Transmitter: range sensible, filter (damping) not hiding the process; noise level known.
- Know the controller's **form** (ideal/ISA, series, parallel) and units: gain Kc vs
  proportional band PB = 100/Kc (%); integral in min/repeat (τI) vs repeats/min (1/τI).
  Mistaking these is the most common tuning error.

## 2. Bump test (manual mode)
Step the output 5–10% (enough to see above noise, safe for the process), at steady state.
Record PV and OP. Fit **FOPDT**:
- K = ΔPV%/ΔOP% (both in % of span: controller gain is dimensionless in %/%),
- θ = dead time until PV starts moving,
- τ = time from end of θ to 63% of the final change.
Repeat in the opposite direction; if K differs a lot, the process is non-linear: tune for the
higher gain. If PV ramps without levelling (levels, some pressures), it is **integrating**:
k' = (slope of PV in %/min)/ΔOP%.

## 3. Tuning rules (PI first; most process loops need only PI)
**SIMC (Skogestad)**, choose closed-loop time constant τc (τc = θ is a good robust default):
- Self-regulating: Kc = (1/K)·τ/(τc + θ), τI = min(τ, 4(τc + θ)).
- Integrating: Kc = 1/(k'(τc + θ)), τI = 4(τc + θ).
**Lambda/IMC:** Kc = τ/(K(λ + θ)), τI = τ, with λ = 1–3·τ for smooth, robust loops (gated: unconfirmed, source is paywalled or blocked); see `engineering-technology.chemical-engineering.process-control.imc-lambda-tuning`.
Worked example: OP 40 → 50%, temperature rises 2.5% of span; θ = 1 min, τ = 8 min.
K = 0.25. SIMC with τc = 1: Kc = 4·8/2 = 16, τI = min(8, 8) = 8 min. The high gain is right
because the process gain is small; if noise makes OP jumpy, raise τc to 2–3 min
(Kc = 8 to 10.7) or filter PV lightly. Ziegler–Nichols gives roughly quarter-decay response, too
aggressive for most process plants; use it only as a reference.

## 4. Derivative
Add D only for lag-dominant loops (τ ≫ θ, e.g. some temperatures), with a derivative filter
(α ≈ 0.1) and derivative on PV, not error. SIMC series-form τD = τ2 for second-order models.
Never use D on flow or noisy level loops.

## 5. Loop-type defaults (starting points, then verify)
- **Flow:** fast, noisy; PI with Kc ≈ 0.3–0.8, τI ≈ 0.05–0.3 min (indicative (gated: unconfirmed, source is paywalled or blocked)).
- **Level:** usually averaging control to absorb surges: use the integrating rule with a slow
  τc set by allowed level swing, not tight control. Tight level only where needed (e.g. a
  reboiler or compressor knock-out).
- **Pressure:** liquid-full is fast like flow; gas pressure is integrating-ish.
- **Temperature:** slow, lag-dominant; PI or PID.
- **Composition/analyser:** large dead time; consider τc ≥ θ and feedforward.

## 6. Cascade and interaction
Tune the inner loop first, in auto, and make it ≥ 4–5× faster than the outer. The outer loop
then sees "inner loop + process" as its plant; bump-test it with the inner in cascade. Use
RGA (relative gain array) to check pairing before blaming tuning for interacting loops.
Put anti-reset-windup/external reset on the outer controller.

## Gotchas
- Direct vs reverse action wrong = runaway the moment you go to auto.
- Tuning at one throughput may be unstable at another (valve gain changes); test at both.
- Changes on a live plant need the site's management-of-change and operator agreement;
  safety instrumented functions are not tuned this way.

## Verify
- [ ] Valve stiction and sizing checked first; controller form and units confirmed.
- [ ] FOPDT (or integrating) model fitted from at least two bump tests.
- [ ] Tuning from a named rule with τc/λ recorded.
- [ ] Setpoint step: overshoot ≤ ~10%, settles within ~3–4 (τc + θ) (rule-of-thumb targets (gated: unconfirmed, source is paywalled or blocked)), no sustained oscillation.
- [ ] Disturbance test (or load change) rejected; OP not saturating or chattering.
