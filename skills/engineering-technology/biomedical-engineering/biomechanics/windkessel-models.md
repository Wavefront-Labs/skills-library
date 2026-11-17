---
id: engineering-technology.biomedical-engineering.biomechanics.windkessel-models
name: windkessel-models
category: engineering-technology
field: biomedical-engineering
product: biomechanics
tags: [windkessel, arterial-compliance, vascular-impedance, lumped-parameter, cardiovascular-modeling]
level: practitioner
status: gated
description: "Use two-, three- and four-element Windkessel models for arterial load: parameters, diastolic decay, fitting to pressure and flow, and uses in device testing."
sources: ["Westerhof, Lankhaar and Westerhof, The arterial Windkessel (Medical and Biological Engineering and Computing, 2009)", "Nichols and O'Rourke, McDonald's Blood Flow in Arteries", "https://www.isbweb.org"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Windkessel models

**Goal:** a lumped description of arterial load relating pressure P and inflow Q using peripheral resistance R and compliance C.

## Models
- **Two-element:** C dP/dt = Q - P/R. In diastole (Q = 0) pressure decays exponentially, P(t) = P_start times exp(-t / (R C)); the time constant tau = R C. Example: R = 1.0 mmHg s/mL and C = 1.5 mL/mmHg gives tau = 1.5 s; over a 0.5 s diastole pressure falls to exp(-0.5/1.5), about 72 percent of its starting value (exp(-1/3) = 0.7165, computed).
- **Three-element:** adds a characteristic impedance Zc in series with the parallel RC; improves high-frequency behaviour and the systolic pressure wave.
- **Four-element:** adds an inertance L to Zc in parallel, further improving the fit at high frequency.

## Fitting
1. Measure or simulate pressure and flow (or use pressure alone with a flow estimate).
2. Estimate R from mean pressure divided by mean flow (the model forms and fitting recipe follow the cited textbooks (gated: unconfirmed, source is paywalled or blocked)); C from diastolic decay (tau / R) or from the pulse pressure method.
3. Fit Zc to the high-frequency modulus of input impedance, or by least squares on pressure waveform.
4. Check the fit by comparing predicted and measured pressure over the cycle.

## Use
- Mock circulatory loops for valve, stent graft or pump testing use hydraulic Windkessel elements to reproduce physiologic load.
- Outlet boundary condition for 3D CFD of arterial segments.
- Limits: lumped models do not capture wave transmission and reflection.

## Verify
- [ ] Unit conventions consistent (mmHg, mL, s).
- [ ] Fit residual and parameter plausibility checked.
- [ ] Applicability (frequency range) stated.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
