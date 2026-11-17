---
id: engineering-technology.aerospace-engineering.matlab-simulink.monte-carlo-parameter-sampling
name: monte-carlo-parameter-sampling
category: engineering-technology
field: aerospace-engineering
product: matlab-simulink
tags: [matlab, simulink, monte-carlo-dispersions, monte-carlo, dispersions, parameter-sampling, latin-hypercube, lhsdesign, sobol]
level: practitioner
status: docs-checked
description: "Sample uncertain parameters for Monte Carlo dispersion runs with random, Latin hypercube or Sobol sampling, using proper distributions and correlations."
sources:
  - "https://www.mathworks.com/help/stats/lhsdesign.html"
  - "https://www.mathworks.com/help/stats/sobolset.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Parameter sampling for dispersions

**Goal:** a sample set that exercises the uncertainty space.

## Methods
- Plain random sampling (`randn`, `rand`): simple but converges slowly.
- **Latin hypercube** (`lhsdesign(n, p)`): n-by-p sample with one value from each of n equal intervals per column, values in (0,1).
- **Sobol sequence** (`sobolset(d)`): quasirandom point set that fills space uniformly; `d` is the number of dimensions.

## Procedure
1. List dispersed parameters (mass, cg, aerodynamic coefficients, thrust, winds, sensor bias) with nominal values and distributions (normal with sigma, uniform bounds, truncated normal for physical limits).
2. Generate unit-hypercube samples `U = lhsdesign(N, p)`; map each column to its distribution with the inverse CDF.
3. Include correlations (use a Cholesky factor of the covariance for correlated normals).
4. Truncate at physically meaningful limits and record the sample matrix with the run.

## Gotchas
- Dispersing a coefficient and its dependents independently breaks physical consistency (for example total mass vs component masses).
- Sampling in the wrong units.
- Using +/- 3 sigma without justification: use measured or programme-agreed uncertainties.

## Verify
- [ ] Sample histograms match the intended distributions and correlation matrix.

## Checked
2026-11-01. Confirmed on the MathWorks pages: `lhsdesign(n,p)` syntax, per-column stratification and (0,1) range; `sobolset(d)` as a quasirandom Sobol point set. Removed: the Halton set (page only lists it under See Also), the norminv call (not on the pages read) and the textbook source.
Method: documentation only; no commands were run.
