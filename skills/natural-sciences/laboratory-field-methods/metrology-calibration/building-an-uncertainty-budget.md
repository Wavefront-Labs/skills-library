---
id: natural-sciences.laboratory-field-methods.metrology-calibration.building-an-uncertainty-budget
name: building-an-uncertainty-budget
category: natural-sciences
field: laboratory-field-methods
product: metrology-calibration
tags: [metrology-calibration, metrology, measurement-uncertainty, uncertainty-budget, gum, type-a, type-b, standard-uncertainty, rectangular-distribution, triangular-distribution, sensitivity-coefficient, combined-standard-uncertainty, root-sum-square, expanded-uncertainty, coverage-factor, k-2, traceability, calibration-certificate, iso-17025, repeatability, resolution, temperature-effect, effective-degrees-of-freedom, welch-satterthwaite]
level: advanced
status: verified
description: "Build a GUM-style measurement uncertainty budget: model the measurement, list sources, convert each to a standard uncertainty (Type A/B), combine by root-sum-square and expand with k=2."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Building an uncertainty budget

**Goal:** a stated result like "10.012 g ± 0.004 g (k = 2, ~95 %)" where every
contribution to that ± is listed, quantified and traceable — following the
GUM (Guide to the Expression of Uncertainty in Measurement) approach.

## 1. Write the measurement model
Express the result as a function of its inputs: y = f(x₁, x₂, …). Example: volume
delivered by a pipette determined by weighing:
V = (m_reading − m_tare) / ρ_water(T) × (correction for air buoyancy)
Every quantity in the model, and every correction you *didn't* apply, is a candidate
uncertainty source.

## 2. List the sources
Common ones:
- **Repeatability** of the measurement (scatter of repeated readings).
- **Calibration** of the reference/instrument (from its certificate).
- **Resolution** of the readout.
- **Drift** of the instrument since its last calibration.
- **Environmental** effects (temperature, humidity, pressure) via the model.
- **Reference values** (density, constants) and their stated uncertainties.
- Operator effects, sample inhomogeneity, method bias.
Use a cause-and-effect (fishbone) diagram to avoid missing sources.

## 3. Convert each to a standard uncertainty u(xᵢ)
- **Type A** (statistical): from n repeated readings, u = s / √n for the mean (s = sample
  SD). If you report a single reading, u = s.
- **Type B** (other information):
  - Certificate gives U with coverage factor k → u = U / k (k = 2 usually).
  - Limits ±a with no further information (**rectangular**): u = a / √3.
  - Digital **resolution** d: the half-interval a = d/2, so u = d / (2√3).
  - Values more likely near the centre (**triangular**): u = a / √6.
  - Manufacturer tolerance "±0.1 %" is typically treated as rectangular.

## 4. Sensitivity coefficients
cᵢ = ∂f/∂xᵢ converts each input uncertainty into output units: uᵢ(y) = |cᵢ| · u(xᵢ).
For a temperature effect, c = (change in result per °C), often from the model or a
measured coefficient. For simple sums, c = 1; for products/quotients, it's easier to work
in relative uncertainties.

## 5. Combine and expand
- For independent inputs: **u_c(y) = √(Σ uᵢ(y)²)** (root-sum-square). Correlated inputs
  (e.g. two readings from the same uncalibrated balance) need covariance terms or must be
  combined linearly — do not treat them as independent.
- **Expanded uncertainty U = k · u_c**, with k = 2 giving roughly 95 % coverage when the
  distribution is approximately normal and degrees of freedom are large. If a Type A term
  with few readings dominates, compute effective degrees of freedom
  (Welch–Satterthwaite) and use the corresponding t-value for k.

## 6. Lay out the budget table
| Source | Value ± | Distribution | Divisor | u(xᵢ) | cᵢ | uᵢ(y) |
|---|---|---|---|---|---|---|
| Repeatability (n=10) | s = 0.0012 g | normal | √10 | 0.00038 g | 1 | 0.00038 |
| Balance calibration | U = 0.0010 g, k=2 | normal | 2 | 0.0005 g | 1 | 0.0005 |
| Resolution 0.0001 g | ±0.00005 | rectangular | √3 | 0.00003 g | 1 | 0.00003 |
| … | | | | | | |
Sort by contribution: usually one or two dominate, and those are where improvement effort
pays off. Contributions below ~1/3 of the largest barely change the total.

## 7. Report
Round the expanded uncertainty to at most two significant figures (GUM 7.2.6) and the result to the same decimal
place. State k and coverage probability. Traceability requires that the reference standards
were calibrated by a laboratory (e.g. ISO/IEC 17025-accredited) traceable to national standards.

## Gotchas
- Don't double count: if repeatability already includes operator and short-term environmental
  variation, don't add them again separately.
- Known biases should be **corrected**, not just added to the uncertainty (GUM principle);
  the correction's own uncertainty goes in the budget.
- A certificate's uncertainty applies at calibration time; add drift for elapsed time.
- Monte Carlo propagation (GUM Supplement 1) is better for strongly non-linear models or
  non-normal outputs.

## Verify
- [ ] Measurement model written; every term has an uncertainty entry or justified omission.
- [ ] Each source converted with the stated distribution and divisor.
- [ ] Sensitivity coefficients included; correlations considered.
- [ ] Expanded U with stated k; dominant contributors identified.
- [ ] Reference standards traceable with in-date certificates.
