---
id: mathematics.statistics.multivariate-analysis.pca-and-factor-analysis-in-practice
name: pca-and-factor-analysis-in-practice
category: mathematics
field: statistics
product: multivariate-analysis
tags: [statistics, multivariate-analysis, pca, principal-component-analysis, factor-analysis, efa, exploratory-factor-analysis, cfa, dimension-reduction, eigenvalues, scree-plot, parallel-analysis, loadings, rotation, varimax, oblimin, standardisation, kmo, bartlett-test, cronbach-alpha, biplot, sklearn, psych-package, prcomp]
level: practitioner
status: gated
description: "Reduce many correlated variables: when to use PCA versus factor analysis, scaling, choosing the number of components, rotation, reading loadings, and avoiding common misreads."
sources:
  - https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html
  - https://cran.r-project.org/package=psych
  - https://pypi.org/project/factor-analyzer/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PCA and factor analysis in practice

**Goal:** summarise many correlated variables into a few dimensions, and know whether
those dimensions are a compression (PCA) or a claim about latent constructs (FA).

## 1. Pick the right tool
| Question | Use |
|---|---|
| "Compress these 40 variables for plotting or as model inputs" | **PCA** |
| "Do these 12 questionnaire items measure 3 underlying traits?" | **Exploratory factor analysis (EFA)** |
| "Does my hypothesised 3-factor structure fit new data?" | **Confirmatory factor analysis (CFA)** (lavaan, semopy) |
PCA components are exact linear combinations of all variables explaining total variance.
FA models only the **shared** variance and assumes latent factors cause the items.
On well-behaved data they often look similar; their interpretation is not.

## 2. Prepare the data
- **Standardise** (z-score) unless all variables share units and their variances are
  meaningful. Unscaled PCA on income (£) and age (years) is just "income".
  R `prcomp(x, scale. = TRUE)`; sklearn `StandardScaler` then `PCA`.
- Handle missing data deliberately (complete cases, or imputation); never fill with 0.
- Check outliers — a single extreme point can capture a whole component.
- For FA: correlations should be substantial. **KMO** > ~0.6 (gated: unconfirmed, source is paywalled or blocked) and a significant
  **Bartlett's test** suggest FA is worth trying (`psych::KMO`, `factor_analyzer`).
- Ordinal Likert items: use **polychoric** correlations for FA (`psych::fa(cor = "poly")`).

## 3. How many components or factors
Don't rely on one rule:
- **Parallel analysis** (best single rule): keep components whose eigenvalue exceeds
  those from random data of the same size. `psych::fa.parallel()`.
- **Scree plot**: keep those before the elbow.
- **Kaiser (eigenvalue > 1)**: over-extracts with many variables; use only as a ceiling.
- **Cumulative variance** (e.g. 80%) for compression use cases.
- Interpretability: a factor with only 1–2 strong items is usually not a factor.

## 4. Rotation (FA, sometimes PCA)
Unrotated solutions put everything on factor 1. Rotate for interpretability:
- **Varimax** (orthogonal) — factors uncorrelated. Rarely realistic for human traits.
- **Oblimin / promax** (oblique) — factors may correlate; inspect the factor correlation
  matrix. Default to oblique in social science; if correlations come out < ~0.3,
  orthogonal is fine.

## 5. Read the loadings
- Loadings are correlations (or regression weights, for oblique *pattern* matrices)
  between variables and factors. |loading| ≥ ~0.4 is a common "salient" cutoff (gated: unconfirmed, source is paywalled or blocked).
- Flag **cross-loading** items (≥ 0.3 on two factors (gated: unconfirmed, source is paywalled or blocked)) and items loading on none.
- Name factors from the items, then check the name against a held-out sample.
- For scales, report internal consistency (Cronbach's α or, better, McDonald's ω).

## 6. PCA output you should report
Explained variance ratio per component, cumulative variance, loadings (or components ×
SD for correlation-scale loadings), and a **biplot** for 2-D views. In sklearn,
`pca.components_` are unit eigenvectors, not loadings — multiply by
`sqrt(pca.explained_variance_)` to get loadings on standardised data (checked: equals the item-component correlations to within the n/(n-1) factor).
  `factor_analyzer` 0.5.1 (`calculate_kmo`, `FactorAnalyzer`) failed at call time with scikit-learn 1.9.1 (`force_all_finite` renamed `ensure_all_finite`); pin an older scikit-learn or use `psych` in R.

## Gotchas
- Sign of a component is arbitrary; software may flip it between runs or versions.
- PCA is not feature selection — every component uses every variable.
- Fit scaling and PCA **on the training set only** in predictive pipelines (sklearn `Pipeline`).
- EFA and CFA on the *same* data is circular; split the sample.
- Uncertain: loading cutoffs (0.3/0.4) and KMO thresholds are conventions that vary by field.

## Verify
- [ ] Chose PCA (compression) or FA (latent constructs) for a stated reason.
- [ ] Variables standardised (or justified otherwise); outliers checked.
- [ ] Number of dimensions supported by parallel analysis plus interpretability.
- [ ] Rotation choice justified; factor correlations inspected if oblique.
- [ ] Loadings table shows salient and cross-loading items.
- [ ] Structure confirmed on held-out data or flagged as exploratory.
