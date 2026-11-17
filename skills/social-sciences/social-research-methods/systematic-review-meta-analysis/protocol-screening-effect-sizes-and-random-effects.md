---
id: social-sciences.social-research-methods.systematic-review-meta-analysis.protocol-screening-effect-sizes-and-random-effects
name: protocol-screening-effect-sizes-and-random-effects
category: social-sciences
field: social-research-methods
product: systematic-review-meta-analysis
tags: [systematic-review-meta-analysis, systematic-review, meta-analysis, prisma, prisma-2020, prospero, osf-registration, campbell-collaboration, search-strategy, boolean-search, grey-literature, screening, rayyan, covidence, inter-rater-agreement, data-extraction, effect-size, cohens-d, hedges-g, odds-ratio, correlation, fisher-z, random-effects, heterogeneity, i-squared, tau-squared, prediction-interval, metafor, publication-bias, funnel-plot, egger-test, risk-of-bias, rob-2, robins-i, dependent-effect-sizes, robust-variance-estimation]
level: practitioner
status: gated
description: "Run a social-science systematic review and meta-analysis: register a protocol, search and double-screen, extract and convert effect sizes, fit random-effects models, and test for bias."
sources: ["Page et al. (2021) PRISMA 2020 statement, BMJ 372:n71", "Borenstein et al., Introduction to Meta-Analysis (2nd ed., Wiley 2021)", "Cochrane Handbook for Systematic Reviews of Interventions (current version)", "Viechtbauer (2010) metafor, Journal of Statistical Software 36(3)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Systematic review and meta-analysis — from protocol to pooled estimate

**Goal:** a synthesis someone else could reproduce step by step, whose pooled effect and
heterogeneity are reported honestly enough to guide practice.

## 1. Protocol and registration
- Question in a structured frame: PICO (population, intervention, comparison, outcome) or
  PICOS/SPIDER for qualitative/mixed evidence.
- Eligibility criteria (designs, populations, years, languages), primary outcome, effect
  metric, planned moderators, risk-of-bias tool, synthesis model.
- Register before screening: **PROSPERO** (reviews with an outcome of clear relevance to human health; PROSPERO itself requires registration before data extraction starts), **OSF Registries** or a
  **Campbell Collaboration** title for social policy reviews.

## 2. Search
- 3+ databases relevant to the field (e.g. PsycINFO, ERIC, Sociological Abstracts, Web of
  Science, Scopus, EconLit), built with a librarian if possible.
- Concept blocks combined with AND, synonyms with OR, truncation and controlled vocabulary
  per database. Save exact strings and dates for the appendix.
- **Grey literature:** dissertations, working-paper series, government reports, trial
  registries; plus backward/forward citation chasing. Social-science effects are often in
  reports, not journals.

## 3. Screening
- Deduplicate, then title/abstract screening by **two independent reviewers** (Rayyan,
  Covidence, ASReview for prioritisation), then full text with reasons for exclusion
  recorded. Pilot on ~50 records to calibrate; report agreement and how conflicts were resolved.
- Fill the **PRISMA 2020 flow diagram** as you go, not from memory at the end.

## 4. Extraction
Piloted form, double extraction of effect data at least. Extract: design, sample, setting,
intervention details, outcome measure and timing, and the raw statistics (means, SDs, ns,
t, F, χ², odds, correlations).

## 5. Effect sizes
- Continuous group comparisons → **Hedges' g** (Cohen's d with small-sample correction).
- Binary → log odds ratio or log risk ratio.
- Associations → correlation, analysed as **Fisher's z**, back-transformed for reporting.
- Converting between families is possible but note it as an assumption: d = ln(OR) × √3/π, i.e. ln(OR) = d × π/√3 ≈ 1.814 d (Hasselblad-Hedges logistic conversion).
- R: `metafor::escalc()`; also `esc` for conversions from t, F, p (both on CRAN; R code not run here (gated: unconfirmed, source is paywalled or blocked)).
- Clustered trials: correct the variance for the design effect before pooling.

## 6. Synthesis
- Default to **random-effects** in social science: true effects plausibly vary across
  settings. `rma(yi, vi, method = "REML")`; use Knapp–Hartung (`test = "knha"`) for better
  coverage with few studies.
- Report **τ²/τ**, **I²** and a **95% prediction interval** — the range where a new study's
  true effect would likely fall. I² is a proportion, not an absolute amount of heterogeneity.
- **Multiple effects per study** (several outcomes or arms): multilevel model
  (`rma.mv` with random effects for study/effect) plus **robust variance estimation**
  (`clubSandwich`); do not treat them as independent.
- Moderators via meta-regression, pre-specified, with ~10 studies per moderator as a rough minimum.

## 7. Bias
- Study-level: RoB 2 (randomised), ROBINS-I (non-randomised), or a field-appropriate tool;
  two raters.
- Small-study/publication bias: funnel plot, Egger's regression test, PET-PEESE or
  selection models as sensitivity analyses. Trim-and-fill is widely used but performs
  poorly under heterogeneity — do not lean on it alone.
- Certainty of evidence: GRADE where the audience expects it.

## Gotchas
- Pre-post SDs used as if they were between-group SDs inflate effects.
- Including the same sample from two papers double counts.
- A significant pooled mean with a prediction interval crossing zero means "works on average,
  not reliably".

## Verify
- [ ] Protocol registered before screening; deviations listed.
- [ ] Full search strings, dates and grey sources reported.
- [ ] Dual screening and extraction with agreement reported; PRISMA diagram complete.
- [ ] Effect-size computations scripted and shared.
- [ ] Random-effects estimate with τ, I² and prediction interval; dependence handled.
- [ ] Risk-of-bias and small-study sensitivity analyses reported.

*Checked 2026-10-19: Python/statsmodels random-effects pooling, Hedges small-sample factor J=1-3/(4df-1) and Fisher z back-transform run; PROSPERO scope from its inclusion page via search. The metafor calls (`rma`, `test="knha"`, `rma.mv`) and clubSandwich were not run (gated: unconfirmed, source is paywalled or blocked). Registry choices reflect common practice; check the target journal or Campbell/Cochrane guidance.*
