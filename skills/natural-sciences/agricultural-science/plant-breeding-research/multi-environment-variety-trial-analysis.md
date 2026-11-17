---
id: natural-sciences.agricultural-science.plant-breeding-research.multi-environment-variety-trial-analysis
name: multi-environment-variety-trial-analysis
category: natural-sciences
field: agricultural-science
product: plant-breeding-research
tags: [agricultural-science, plant-breeding-research, plant-breeding, variety-trials, met, multi-environment-trials, genotype-by-environment, gxe, blup, blue, mixed-model, heritability, broad-sense-heritability, cullis-heritability, stability-analysis, ammi, gge-biplot, finlay-wilkinson, factor-analytic, asreml, lme4, metan, check-varieties, genomic-selection, marker-assisted-selection, selection-response, breeders-equation]
level: advanced
status: draft
description: "Analyse multi-environment variety trials: per-site QC, BLUEs vs BLUPs, heritability per site, GxE via factor-analytic or GGE models, stability, and turning results into selection decisions."
sources: [Smith, Cullis & Thompson 2005 (factor-analytic MET models), Piepho & Möhring 2007 (heritability), Yan & Kang 2003 GGE Biplot Analysis, R packages lme4, metan, ASReml-R documentation]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Multi-environment variety trial (MET) analysis

**Goal:** rank breeding lines or varieties tested across many sites and years, separate
real genetic merit from environment noise, and understand genotype × environment
interaction (GxE) well enough to decide what to advance or release.

## 1. Per-trial quality control first
Each site-year is an environment. For each:
- Fit the trial's own design model (RCBD, alpha-lattice, row-column, with spatial terms
  if field-laid in a grid) and inspect residuals, outliers and field trends.
- Compute **heritability** (repeatability) on an entry-mean basis. For unbalanced or
  spatial designs use the Cullis formula: `H² = 1 − mean(PEV of BLUP differences) /
  (2·σ²_g)`. Trials with very low H² (often <~0.2–0.3, a judgement call) or with obvious
  damage are dropped or down-weighted *with a documented rule*.
- Check CV and that the checks (standard varieties) behaved as expected.

## 2. BLUEs vs BLUPs
- **BLUEs** (genotype fixed) — unbiased means; use them for a two-stage analysis or when
  reporting variety performance to growers.
- **BLUPs** (genotype random) — shrink toward the mean according to information; better
  for **ranking and selection**, especially with unbalanced data where lines are tested
  in different numbers of sites. Never compare raw means of lines seen at different sites.
- Two-stage (per-site BLUEs + weights → combined model) vs single-stage (all plot data
  at once): single-stage is optimal but heavier; weighted two-stage is the pragmatic
  default for large programmes.

## 3. Model GxE
Start simple, add complexity only if it fits better (compare by AIC/likelihood):
1. Main effects + G×E as a single variance (compound symmetry) — assumes all
   environments correlate equally.
2. Heterogeneous genetic variance per environment.
3. **Factor-analytic (FA1, FA2…)** models (ASReml, `sommer`): estimate the genetic
   correlation between every pair of environments with few parameters; standard in
   large breeding programmes.
Visual tools: **GGE biplot** (which-won-where, mega-environments) and **AMMI** (R
`metan`). Finlay–Wilkinson regression gives a simple stability slope against an
environment index. Treat biplots as exploratory; they hide how much variance the first
two components miss — report that percentage.

## 4. Stability vs performance
A stable but low-yielding line isn't useful. Rank by predicted performance in the
target population of environments (overall BLUP or regional BLUPs from the FA model),
then consider stability (e.g. sensitivity to stress environments) as a secondary filter.
Define the **target population of environments** explicitly — trials should sample it.

## 5. From analysis to selection
- **Breeder's equation:** response R = i · h² · σ_p (per cycle); divide by cycle
  length for gain per year. Shorter cycles (genomic selection, speed breeding) often win
  more than higher accuracy.
- Genomic selection: train a GBLUP or similar model on phenotyped, genotyped lines using
  MET BLUEs (deregressed if using BLUPs); validate by cross-validation *across* sets
  or years, not random plots from the same trials.
- Marker-assisted selection suits large-effect loci (disease resistance genes); for
  yield, polygenic genomic prediction is the norm.

## Gotchas
- Year effects are huge: one year of data across many sites is still one year.
- Checks are often grown everywhere, new lines in few places — unbalance plus fixed
  effects misleads.
- Confounding site with management (irrigated vs dryland) under one "environment" label.
- Reporting letters of significance among 200 lines is meaningless; report BLUPs, SEs
  and reliability.

## Verify
- [ ] Each site-year QC'd with its design model; heritability computed; exclusion rule written.
- [ ] Ranking based on BLUPs (or weighted BLUEs) from a model handling unbalance.
- [ ] GxE model chosen by likelihood comparison; variance explained by biplots stated.
- [ ] Selection tied to the defined target environments and expected genetic gain.
