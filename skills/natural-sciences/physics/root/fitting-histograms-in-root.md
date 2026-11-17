---
id: natural-sciences.physics.root.fitting-histograms-in-root
name: fitting-histograms-in-root
category: natural-sciences
field: physics
product: root
tags: [root, cern-root, pyroot, th1, tf1, histogram-fitting, curve-fitting, minuit, minuit2, chi-square-fit, likelihood-fit, binned-likelihood, fit-options, tfitresult, gaussian-fit, peak-fitting, background-fit, sumw2, empty-bins, pull-distribution, goodness-of-fit, roofit, c++, python, hep, data-analysis]
level: practitioner
status: docs-checked
description: "Fit histograms in CERN ROOT correctly: TH1::Fit and TF1, chi-square vs likelihood fits, initial parameters, parameter limits, fit results, empty bins and judging the result."
sources: [https://root.cern/manual/fitting/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fitting histograms in ROOT

**Goal:** a fit whose parameters and errors are right, not just a curve that
looks plausible over the plot.

## 1. Minimal working fit (PyROOT; C++ is the same calls)
```python
import ROOT
h = f.Get("h_mass")                          # TH1 from a TFile
model = ROOT.TF1("model", "[0]*TMath::Gaus(x,[1],[2])", 80, 100)   # bracket-parameter syntax
model.SetParameters(h.GetMaximum(), 91, 2.5)  # starting values for [0], [1], [2]
model.SetParLimits(2, 0.1, 10)               # sigma must be positive
res = h.Fit(model, "S")                      # S: return the full fit result
res.Print("V")                               # full fit info incl. covariance matrix
```

## 2. Choosing the fit method
- The ROOT manual: the chi-square method excludes **empty bins** from the fit.
- The manual recommends the **log-likelihood** method (option `L`, or `WL`) for low
  statistics. Look up `WL` and the other option letters in the `TH1::Fit` reference for
  your ROOT version.
- Unbinned fits: use RooFit instead of histograms.

## 3. Options and the fit range
- Option `S` gives access to the full result of the fit including the covariance and
  correlation matrices.
- Option `+` adds the newly fitted function to the existing list instead of replacing it.
- The fit range is set with the optional `xmin` and `xmax` arguments of `Fit`.
- Other option letters (quiet, Minos errors, integral-in-bin, no-draw...): read the
  current `TH1::Fit` options table rather than relying on memory.

## 4. Getting it to converge
- **Initial values matter more than anything.** Estimate them from the histogram — a
  Gaussian starting far from the peak will "fit" the background.
- `TF1::FixParameter()` fixes a parameter; `TF1::SetParLimits()` sets bounds for one
  parameter. Use limits sparingly: a parameter hitting its limit has a meaningless error.
- Fit fixed-shape background alone first, then free everything.

## 5. Judging the fit
- Plot residuals or pulls (data − fit)/σ under the main pad; look for structure.
- Check the correlation matrix from the fit result for strongly correlated parameters.
- Run toy experiments (sample from the fitted model, refit, look at pull widths) when
  the result matters.

## Gotchas
- `h.Rebin()` changes the content per bin; re-estimate initial amplitudes.
- Option letters and defaults change between ROOT releases; confirm in the reference.

## Verify
- [ ] Fit result object inspected (covariance and correlations).
- [ ] Likelihood considered for low-count bins.
- [ ] Pull plot shows no structure.
- [ ] No parameter sits at a limit.

## Checked
2026-11-01. Confirmed on the ROOT manual "Fitting Histograms" page: bracket-parameter formula syntax, fit range via xmin/xmax, option S (full result with covariance and correlation), option + (add to list), Print("V") for full fit info, empty bins excluded in chi-square fits, log-likelihood (L or WL) recommended for low statistics, SetParLimits and FixParameter. Removed (not stated on pages read): default method and minimizer, option letters P, R, E, M, I, N, 0, Q, status code meanings, the 10-20 entry rule, gaus(0)+pol1(3) formula syntax and the correlation threshold.
Method: documentation only; no commands were run.
