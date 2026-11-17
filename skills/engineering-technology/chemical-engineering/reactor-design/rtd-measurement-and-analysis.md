---
id: engineering-technology.chemical-engineering.reactor-design.rtd-measurement-and-analysis
name: rtd-measurement-and-analysis
category: engineering-technology
field: chemical-engineering
product: reactor-design
tags: [chemical-engineering, reactor-design, rx-nonideal-flow, rtd-measurement-and-analysis, rtd, tracer-test, residence-time-distribution]
level: practitioner
status: draft
description: "Measure a residence time distribution with a tracer pulse or step and compute E(t), mean residence time and variance."
sources:
  - "Fogler Elements of Chemical Reaction Engineering, Levenspiel Chemical Reaction Engineering, Froment Bischoff and De Wilde Chemical Reactor Analysis and Design"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Rtd measurement and analysis

**Goal:** Measure a residence time distribution with a tracer pulse or step and compute E(t), mean residence time and variance.

## Steps
1. Choose an inert tracer that is easily detected and does not change the flow; inject as a pulse (or step) at the inlet and record outlet concentration C(t).
2. Pulse: E(t) = C(t) / integral of C dt; the mean tm = integral of t E dt; variance sigma2 = integral of (t - tm)^2 E dt.
3. Step: F(t) = C(t)/C0 and E(t) = dF/dt.
4. Compare tm with V/Q to detect dead zones or bypass (tm less than V/Q suggests dead volume).
5. Normalised form: E(theta) = tau E(t), with theta = t/tau.

## Gotchas
- Tracer injection and detection lines add delay; correct for them.
- Noise in the tail inflates the moments; truncate or fit.

## Verify
- [ ] Area under E(t) equals 1.
- [ ] Mean of E(t) matches V/Q within the tracer uncertainty.
