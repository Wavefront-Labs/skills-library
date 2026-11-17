---
id: natural-sciences.astronomy-astrophysics.cosmology.cosmological-parameter-estimation-with-mcmc
name: cosmological-parameter-estimation-with-mcmc
category: natural-sciences
field: astronomy-astrophysics
product: cosmology
tags: [cosmology, parameter-estimation, mcmc, cobaya, cosmomc, montepython, camb, class, boltzmann-code, likelihood, planck, cmb, bao, supernovae, lcdm, priors, convergence, gelman-rubin, getdist, posterior, nuisance-parameters, tension, hubble-tension, s8, model-comparison, bayesian-evidence]
level: advanced
status: verified
description: "Run and sanity-check a cosmological parameter fit: Boltzmann code + likelihoods in Cobaya, priors and nuisance parameters, MCMC convergence, GetDist contours and tension metrics."
sources: ["Cobaya documentation (cobaya.readthedocs.io)", "Lewis, GetDist documentation", "Planck 2018 results VI: Cosmological parameters"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cosmological parameter estimation with MCMC

**Goal:** posterior constraints on cosmological parameters from data such as CMB, BAO and
supernovae that are converged, reproducible and correctly interpreted — including what
the priors are doing.

## 1. The pieces
- **Theory code:** a Boltzmann solver (CAMB or CLASS) turns parameters into observables
  (CMB spectra, distances, matter power spectrum).
- **Likelihoods:** published data packages (Planck, ACT/SPT, DESI/SDSS BAO, Pantheon+/DES
  SNe…). Each brings **nuisance parameters** (foregrounds, calibration, SN absolute magnitude).
- **Sampler:** Metropolis-Hastings (Cobaya, CosmoMC, MontePython), or nested sampling
  (PolyChord, MultiNest) when you also want Bayesian evidence.

## 2. A minimal Cobaya setup
```yaml
theory:
  camb: {extra_args: {lens_potential_accuracy: 1}}
likelihood:
  bao.desi_2024_bao_all: null       # name exists in Cobaya 3.6.2 (a DESI DR2 set also ships); run cobaya-install first
  sn.pantheonplus: null
params:
  H0: {prior: {min: 40, max: 100}, ref: 68, proposal: 1}
  ombh2: {prior: {min: 0.005, max: 0.1}, ref: 0.0224, proposal: 0.0002}
  omch2: {prior: {min: 0.001, max: 0.99}, ref: 0.12, proposal: 0.002}
  # ... plus fixed or sampled As, ns, tau as the data require
sampler:
  mcmc: {Rminus1_stop: 0.01, max_tries: 1000}
output: chains/run1
```
Install likelihood data with `cobaya-install` (without it Cobaya raises ComponentNotInstalledError). Checked on Cobaya 3.6.2 + CAMB 2.0.5: this YAML builds and evaluates as written (As, ns, tau fall back to CAMB defaults), and a 600-step run with the GetDist block below works. *Likelihood names change between releases; check the current list.* Run with MPI across several chains (`mpirun -n 4 cobaya-run`).

## 3. Priors and degeneracies
- Uniform priors on **which** parameter matters: flat in H0 vs flat in θ* gives different
  posteriors when data are weak. Report the parameterisation.
- Data combinations break degeneracies: BAO alone constrains rd·H0, not H0, unless you add
  a BBN prior on ωb or CMB data. Know which parameters are actually constrained.
- Projection effects: marginal posteriors in high-dimensional spaces can peak away from the
  best fit. Report the best-fit (from a minimizer) alongside means.

## 4. Convergence
- **Gelman–Rubin R−1** across chains: below ~0.01–0.02 for main parameters, and check the
  tails (R−1 on confidence limits) too.
- Discard **burn-in** yourself: Cobaya's `burn_in` defaults to 0 and GetDist's `ignore_rows` defaults to 0, so pass `settings={"ignore_rows": 0.3}` as below (checked in both default files).
- Use a **covariance matrix** from a previous run to speed up proposals.
- Fast/slow parameter split: nuisance parameters are cheap; Cobaya exploits this automatically.

## 5. Analysis with GetDist
```python
from getdist import loadMCSamples, plots
s = loadMCSamples("chains/run1", settings={"ignore_rows": 0.3})
print(s.getInlineLatex("H0", limit=1))       # 68% constraint as LaTeX
print(s.getTable(limit=1).tableTex())        # full parameter table
g = plots.get_subplot_plotter(); g.triangle_plot(s, ["H0", "omegam", "sigma8"], filled=True)
```
Report 68% intervals (or one-tailed 95% limits for parameters hitting a prior edge).

## 6. Tensions and model comparison
- Quantify disagreement between datasets with a named metric (difference in parameter means
  in σ, suspiciousness, parameter-shift probability) — "3σ tension" depends on the metric.
- Extended models (wCDM, Σmν, Neff): compare with Δχ² at best fit plus Bayesian evidence or
  information criteria; evidence depends strongly on prior widths.

## Gotchas
- Combining datasets that share data or are correlated (double-counting).
- Forgetting a required nuisance prior (e.g. SN absolute magnitude calibration).
- Accuracy settings too low in CAMB/CLASS for high-ℓ or lensing data.
- Stopping on R−1 that is good for the means but not the tails.

## Verify
- [ ] Every likelihood's version and nuisance treatment stated.
- [ ] R−1 < ~0.01–0.02 for all reported parameters; chains plotted and look stationary.
- [ ] Results reproduced with a different seed (and ideally a different sampler).
- [ ] Best-fit χ² per dataset reasonable for its degrees of freedom.
- [ ] Prior-dominated parameters identified and reported as such.
