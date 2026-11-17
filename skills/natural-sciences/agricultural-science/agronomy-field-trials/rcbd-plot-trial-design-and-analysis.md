---
id: natural-sciences.agricultural-science.agronomy-field-trials.rcbd-plot-trial-design-and-analysis
name: rcbd-plot-trial-design-and-analysis
category: natural-sciences
field: agricultural-science
product: agronomy-field-trials
tags: [agricultural-science, agronomy-field-trials, field-trials, plot-trials, experimental-design, rcbd, randomised-complete-block, blocking, randomisation, replication, split-plot, alpha-lattice, anova, linear-mixed-model, lme4, asreml, emmeans, spatial-analysis, plot-harvester, yield-measurement, grain-moisture, yield-adjustment, power-analysis, cv-percent, lsd, multiple-comparisons, treatment-randomisation]
level: practitioner
status: gated
description: "Design and analyse an agronomy plot trial: block across the gradient, randomise and replicate properly, harvest yield at standard moisture, fit a mixed model, and report effect sizes not letters."
sources: [Gomez & Gomez 1984 Statistical Procedures for Agricultural Research, Piepho et al. papers on mixed models for field trials, R packages lme4, emmeans, agricolae]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RCBD plot trial: design and analysis

**Goal:** test agronomic treatments (rates, products, timings, varieties) in the field
and come out with treatment differences you can trust, with a design that handles soil
variability rather than being swamped by it.

## 1. Before the first stake
- **One clear question** and its primary response (usually yield, t/ha at standard
  moisture). Secondary measures (establishment, NDVI, protein) are fine but don't power
  the trial for them.
- **Power:** use the site's expected CV (yield CVs of ~5–12% are typical for good grain
  trials) to choose replication. Computed (two-sided t-test on a treatment pair, 6 treatments, alpha 0.05, 80 % power, CV = residual CV of the plot yield): detecting a 5 % difference at CV 8 % needs about 41 blocks, 10 % needs about 11 and 15 % about 5; with 4 blocks the smallest detectable difference is about 10.6 % at CV 5 %, 17 % at CV 8 % and 25 % at CV 12 %. Run a quick power calculation, don't default to 4.
- **Site:** uniform history, away from headlands, trees, old fence lines and wheel
  tracks. Walk it; look at yield maps or EM surveys if available.

## 2. Design
- **Randomised complete block (RCBD):** each block holds every treatment once; lay
  blocks **across** the known gradient (slope, soil change) so each block is as uniform
  as possible — blocks are long *perpendicular* to the gradient.
- Randomise treatments independently within each block (R: `agricolae::design.rcbd`,
  or `sample()` per block); keep the seed and the plan.
- Many entries (e.g. >15 varieties) → incomplete blocks (alpha-lattice) instead of
  huge blocks that aren't uniform.
- Factors applied to large areas (tillage, irrigation) → **split-plot**: main plots for
  the hard-to-change factor, subplots for the other. Analyse as split-plot — the main
  factor has far fewer error degrees of freedom.
- Include **buffers/guard rows** between plots for spray drift, fertiliser movement and
  edge effects; harvest the centre.

## 3. Running it
- Apply treatments with calibrated plot equipment; record dates, rates, conditions.
- Keep a field book (paper or app) by plot number, plus photos.
- **Harvest:** plot combine, record plot weight, harvested area (measure actual plot
  length after trimming ends), and grain moisture. Adjust:
  `yield_std = yield_wet × (100 − M_measured) / (100 − M_standard)`, standard moisture
  per crop (e.g. ~12.5–14% for wheat, 15–15.5% for maize — use your market's standard).
- Note damaged plots and causes *before* seeing yields; exclusions decided after the
  results look like cherry-picking.

## 4. Analysis
Mixed model: treatment fixed, block random (or fixed in a single RCBD — equivalent
for treatment tests when balanced).
```r
# R code below was not run (R is not installed in the review environment) (gated: unconfirmed, source is paywalled or blocked)
library(lme4); library(emmeans)
m <- lmer(yield ~ treatment + (1|block), data = d)
plot(m); qqnorm(resid(m))                    # check residuals and outliers
anova(m)                                       # with lmerTest for p-values
emmeans(m, pairwise ~ treatment, adjust = "tukey")
```
- For rate trials, fit a **response curve** (linear-plateau, quadratic) rather than
  pairwise comparing every rate; report the economic optimum with price ratios.
- Large trials with spatial trends: add row/column effects or spatial correlation
  (e.g. `SpATS`, ASReml AR1×AR1).
- Report means with SE or 95% CI, the CV, and effect sizes in t/ha. Letter displays
  ("a/ab/b") hide magnitudes; include them only if the audience expects them.
- Multi-site/year: analyse sites together with site × treatment interaction — one site
  is one environment, not a recommendation.

## Gotchas
- Pseudo-replication: subsamples within a plot are not replicates.
- Treatments applied in strips without randomisation can't be separated from the strip.
- Missing plots unbalance the RCBD; mixed models handle this, classic ANOVA tables don't.

## Verify
- [ ] Replication chosen by power calculation from realistic CV.
- [ ] Blocks oriented across the gradient; randomisation plan and seed archived.
- [ ] Yields moisture-adjusted on measured harvest area; exclusions documented pre-analysis.
- [ ] Mixed model with residual checks; effect sizes with CIs and CV reported.
