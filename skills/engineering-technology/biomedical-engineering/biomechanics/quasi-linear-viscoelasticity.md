---
id: engineering-technology.biomedical-engineering.biomechanics.quasi-linear-viscoelasticity
name: quasi-linear-viscoelasticity
category: engineering-technology
field: biomedical-engineering
product: biomechanics
tags: [quasi-linear-viscoelasticity, soft-tissue-mechanics, viscoelasticity, qlv, stress-relaxation, reduced-relaxation-function, prony-series]
level: advanced
status: draft
description: "Fit Fung quasi-linear viscoelastic models to soft tissue relaxation tests: reduced relaxation function, elastic response, ramp correction and Prony series for finite element use."
sources: ["Fung, Biomechanics: Mechanical Properties of Living Tissues (QLV theory)", "Abramowitch and Woo, An improved method to analyze the stress relaxation of ligaments following a finite ramp time based on the quasi-linear viscoelastic theory (J Biomech Eng 2004)", "Abaqus or Ansys documentation for Prony series viscoelastic input"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Quasi-linear viscoelasticity (QLV)

**Goal:** a time-dependent stress-strain model for tissues that stiffen with strain and relax with time.

## Theory
Stress is a convolution of a reduced relaxation function G(t) with the rate of the instantaneous elastic response:
sigma(t) = integral from 0 to t of G(t - tau) (d sigma_e / d epsilon)(d epsilon / d tau) d tau.
- **Elastic response:** commonly sigma_e = A (exp(B epsilon) - 1), capturing strain stiffening with parameters A and B.
- **Reduced relaxation function (Fung):** G(t) = [1 + C (E1(t / tau2) - E1(t / tau1))] / [1 + C ln(tau2 / tau1)], with E1 the exponential integral; parameters C, tau1, tau2 describe the spectrum of relaxation times. A Prony series G(t) = g_inf + sum of g_i exp(-t / tau_i) is the common alternative and is what FE packages accept.

## Test and fitting procedure
1. Precondition the tissue (several loading cycles) to reach a repeatable response; maintain hydration and temperature.
2. Run **stress-relaxation tests** (ramp to strain then hold) at several strain levels, and optionally cyclic tests at several frequencies.
3. Fit with a ramp correction: the ramp rate is finite, so relaxation begins during the ramp, and fitting the hold portion as if the ramp were instantaneous biases tau (use the QLV convolution including the ramp).
4. Fit simultaneously the hold data at multiple strains: A and B from instantaneous (peak) response, G(t) parameters from relaxation shape.
5. Validate on independent data (creep, cyclic loading, different strain rates).

## Limits
- QLV assumes a relaxation function independent of strain; many tissues show strain-dependent relaxation (cartilage, ligaments at high strain).
- QLV extrapolates poorly beyond tested rates.

## Verify
- [ ] Fit residuals reported per test.
- [ ] Parameter confidence intervals (bootstrapped).
- [ ] Prony series reproduces the original fit in FE for a simple relaxation simulation.
