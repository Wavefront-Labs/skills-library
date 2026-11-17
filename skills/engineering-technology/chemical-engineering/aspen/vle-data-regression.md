---
id: engineering-technology.chemical-engineering.aspen.vle-data-regression
name: vle-data-regression
category: engineering-technology
field: chemical-engineering
product: aspen
tags: [chemical-engineering, aspen, aspen-binary-parameters-and-regression, vle-data-regression, data-regression, drs, vle-regression, parameter-fitting, nrtl, thermodynamic-consistency, aspen-plus, txy-data]
level: practitioner
status: draft
description: "Regress binary VLE data to NRTL or Wilson parameters in the Aspen Data Regression System, with consistency checks, weights and goodness-of-fit review."
sources:
  - "Aspen Plus and Aspen HYSYS user guides and help (AspenTech), Seider et al. Product and Process Design Principles"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Regressing VLE data to fit parameters

**Goal:** a binary parameter set that reproduces experimental VLE data over the window you need.

## Steps
1. **Collect data**: isothermal or isobaric VLE with T, P, x, y. Prefer several sources; note temperature range.
2. **Check consistency**: area (Redlich-Kister) test or point test; discard inconsistent sets or give them low weight.
3. **Create a Data Regression case** in Aspen Plus: add each data set (Mixture type: for example Txy or Pxy), name the components, enter data with units and the standard deviations (weights) for T, P, x, y.
4. **Define the regression**: choose the property method and the parameters to fit (for NRTL start with the dimensionless pair a12 and a21, add b terms only if data span a wide temperature range). Fix the non-randomness parameter c.
5. **Run**; inspect the residuals: look at standard deviation of fit, parity plot of y vs y_calc, and the Txy overlay.
6. **Use fitted values**: copy the result into the Binary Interaction form or let the regression update the parameters.

## Rules of thumb
- Fit the fewest parameters that reproduce the data (two or four).
- Use bubble-point pressure or temperature as the objective, not only y, because y is the noisiest quantity.
- Extrapolation beyond the data window is a risk; document the range.

## Gotchas
- Initial guesses matter; start from database or UNIFAC-estimated values.
- Fitting with too wide a weight tolerance can hide inconsistent data.
- Two parameter sets can fit equally well yet extrapolate differently; compare predicted infinite-dilution activity coefficients.

## Verify
- [ ] Parity and Txy overlay plots saved.
- [ ] Residual deviations within the stated acceptance.
- [ ] Regressed set documented with data sources and valid range.
