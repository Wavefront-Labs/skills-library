---
id: engineering-technology.aerospace-engineering.flight-dynamics-control.aircraft-system-identification
name: aircraft-system-identification
category: engineering-technology
field: aerospace-engineering
product: flight-dynamics-control
tags: [flight-dynamics, flight-test, parameter-identification, system-identification, 3211-manoeuvre, output-error, equation-error, cifer, sidpac]
level: advanced
status: draft
description: "Identify aerodynamic derivatives from flight data: excitation design (3-2-1-1, sweeps), data compatibility, and equation-error, output-error and frequency-domain estimators."
sources:
  - "Klein and Morelli, Aircraft System Identification: Theory and Practice"
  - "Jategaonkar, Flight Vehicle System Identification"
  - "Tischler and Remple, Aircraft and Rotorcraft System Identification"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Aircraft system identification

**Goal:** derivative estimates and confidence bounds from flight test.

## Steps
1. **Excitation:** inputs rich in frequency content around the modes of interest: 3-2-1-1 multistep, doublets, frequency sweeps, or optimised multisine inputs, applied to one control at a time or simultaneously with orthogonality. Maintain safe envelope limits.
2. **Instrumentation:** accurate angular rates, accelerations, air-data angles and control positions, with known sensor dynamics, biases and time delays.
3. **Data conditioning:** filter, resample, and reconstruct states via kinematic consistency checks (flight-path reconstruction with an extended Kalman filter).
4. **Model structure:** choose terms (for example `C_m_alpha`, `C_m_q`, `C_m_delta_e`), using stepwise regression.
5. **Estimation:** equation-error (linear regression on measured accelerations), output-error (maximum likelihood, compares simulated and measured outputs), or frequency-domain methods (CIFER).
6. **Validation:** predict an independent manoeuvre not used for estimation; evaluate Cramer-Rao bounds and residual whiteness.

## Practice
- Use NASA's SIDPAC and other codes in the literature for implementations; ensure the numerical conditioning (scale regressors).
- Repeat runs at several flight conditions to see trends.

## Gotchas
- Collinearity (correlated regressors) gives unreliable derivatives even with good fits.
- Unmodelled dynamics (actuators, structural modes) bias results.

## Verify
- [ ] The identified model reproduces a validation manoeuvre within the measurement noise.
