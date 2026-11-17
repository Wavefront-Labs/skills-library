---
id: engineering-technology.biomedical-engineering.biomedical-instrumentation.cole-model
name: cole-model
category: engineering-technology
field: biomedical-engineering
product: biomedical-instrumentation
tags: [cole-model, bioimpedance, impedance-measurement, cole-cole-plot, impedance-spectroscopy, extracellular-resistance, intracellular-resistance, nonlinear-fit]
level: advanced
status: gated
description: "Fit a Cole impedance model to bioimpedance spectra: R0, Rinf, tau and alpha, extraction of extracellular and intracellular resistance, fitting methods, artefacts and validation."
sources: ["Cole, Permeability and impermeability of cell membranes for ions (Cold Spring Harbor Symp Quant Biol 1940)", "Grimnes and Martinsen, Bioimpedance and Bioelectricity Basics"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Cole model fitting for bioimpedance

**Goal:** summarise a tissue impedance spectrum in a few parameters that relate to tissue structure.

## Model
Z(omega) = R_inf + (R_0 - R_inf) / (1 + (j omega tau)^alpha)
- **R_0:** resistance at low frequency (current flows around cells, so mostly extracellular water).
- **R_inf:** resistance at very high frequency (current passes through cell membranes, total body water).
- **tau:** time constant; characteristic frequency f_c = 1 / (2 pi tau).
- **alpha** (0 to 1): spread of time constants; typical tissue 0.6-0.9 (gated: unconfirmed, source is paywalled or blocked); 1 gives an ideal single-time-constant semicircle.

## Derived quantities (parallel two-compartment model; R_i identity checked numerically: R_inf = R_e R_i/(R_e + R_i) inverts to the formula below, and the Cole arc peaks at omega tau = 1 for alpha 0.8)
- Extracellular resistance R_e = R_0.
- Intracellular resistance R_i = R_0 R_inf / (R_0 - R_inf).
- Membrane capacitance estimates from f_c and R values (depends on the assumed model; state it).

## Fitting procedure
1. Measure impedance (magnitude and phase) at 20-50 logarithmically spaced frequencies, typically 1 kHz to 1 MHz for body measurements (see four-electrode-measurement).
2. **Clean the data:** remove points distorted by cable capacitance or electrode artefacts at the highest frequencies (inductive-looking tails in the Cole plot). Verify with Kramers-Kronig consistency checks if possible.
3. **Fit** the complex Z by nonlinear least squares (Levenberg-Marquardt), minimising weighted errors of real and imaginary parts; initialise R_0 and R_inf from low and high-frequency ends, tau from the peak of the negative imaginary part, alpha as 0.8.
4. **Constraints:** R_0 greater than R_inf, 0 < alpha <= 1; test multiple initial values.
5. **Uncertainty:** bootstrap or use the covariance matrix; report confidence intervals.
6. **Visual check:** plot the Cole-Cole plot (negative imaginary versus real) with the fitted arc.

## Gotchas
- A narrow frequency range cannot estimate R_inf or R_0 well; extrapolation is sensitive.
- Poor electrode contact makes low-frequency data unreliable.
- Different formulations (Cole in impedance versus admittance or conductivity) yield different parameters; state which.

## Verify
- [ ] Test the fit on a synthetic spectrum with noise and recover known parameters.
- [ ] Measurements of an RC network matching a Cole-like response give expected values.
- [ ] Residuals show no structure.
