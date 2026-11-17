---
id: social-sciences.psychology.behavioural-data-analysis.mixed-effects-models-and-effect-sizes
name: mixed-effects-models-and-effect-sizes
category: social-sciences
field: psychology
product: behavioural-data-analysis
tags: [behavioural-data-analysis, psychology, statistics, mixed-effects-models, linear-mixed-models, lmm, glmm, multilevel-models, lme4, lmer, glmer, afex, emmeans, brms, random-slopes, crossed-random-effects, convergence, singular-fit, contrasts, sum-coding, anova, repeated-measures-anova, effect-size, cohens-d, partial-eta-squared, bayes-factor, bayesfactor, r-language, jasp]
level: practitioner
status: gated
description: "Analyse behavioural data with linear and generalised mixed models in lme4: random-effects structure, convergence fixes, contrasts, effect sizes and Bayes factors."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mixed-effects models and effect sizes for behavioural data

**Goal:** analyse trial-level human data with participants and stimuli as random
effects, get a model that converges honestly, and report effects people can interpret.

## 1. Why mixed models instead of averaged ANOVA
Averaging each participant's trials then running repeated-measures ANOVA ignores
item variability (the "language-as-fixed-effect fallacy") and throws away information
about unbalanced or missing trials. A mixed model on raw trials handles crossed
participants × items, unbalanced data, and binary outcomes (accuracy) via GLMM.

## 2. Set up the data and contrasts
- Long format: one row per trial, columns `subj`, `item`, `cond`, `rt`, `correct`.
- Factors as factors. Use **sum/deviation coding** (`contr.sum`, or ±0.5 for two
  levels) so main effects are average effects, not simple effects at a reference level:
```r
library(lme4); library(afex); library(emmeans)
contrasts(d$cond) <- contr.sum(2)
m <- lmer(log(rt) ~ cond + (1 + cond | subj) + (1 + cond | item), data = d)
```
- Accuracy: `glmer(correct ~ cond + (1 + cond | subj) + (1 | item), family = binomial, data = d)`.

## 3. Random-effects structure
- Include **random slopes** for within-unit factors (cond varies within subj and
  within item → slopes for both). Random intercepts only inflate Type I error
  (Barr et al. 2013 "keep it maximal").
- If the maximal model fails to converge or is singular, simplify in principled steps:
  drop random correlations (`||` in afex/lme4 with numeric predictors), then the
  smallest-variance slopes. Report what you dropped. (Matuschek et al. 2017 argue for
  parsimonious models; both views are defensible — pick one and preregister.)
- Convergence tips: scale continuous predictors, try `control = lmerControl(optimizer = "bobyqa")`,
  check `allFit()` — if all optimisers agree, the warning is likely benign.

## 4. Inference
- p-values for `lmer`: Satterthwaite or Kenward–Roger df via `lmerTest`, or
  `afex::mixed(..., method = "KR")`. Likelihood-ratio tests for GLMMs.
- Follow-up contrasts and simple effects: `emmeans(m, pairwise ~ cond | group)` with a
  stated multiple-comparison correction (Holm, Tukey).
- **Bayesian alternative:** `brms` for full posteriors; `BayesFactor` or JASP for Bayes
  factors — useful to quantify evidence *for* a null. Report priors and check
  sensitivity to them.

## 5. Effect sizes
- Always report **unstandardised effects** in the original unit with CIs ("38 ms
  [22, 54]") — usually the most interpretable.
- Standardised: Cohen's d (state which: d_s between groups, d_z or d_av within),
  partial η² or generalised η² for ANOVA (generalised is comparable across designs).
- In mixed models, standardised d is ambiguous; one approach divides the fixed effect by
  the square root of the summed variance components (Westfall et al. 2014). Say what you did.

## 6. Messy human data
- Plot raw data per participant before modelling — spaghetti plots catch coding errors,
  reversed scales, bots.
- Missing data: mixed models use all available trials (fine under MAR); for
  questionnaire missingness use multiple imputation (`mice`), not listwise deletion.
- Check residuals (`performance::check_model`) — skew in RT suggests log or a GLMM.
- Ceiling/floor effects on accuracy make interactions uninterpretable on the
  probability scale; the logit scale of a GLMM helps.

## Gotchas
- Treatment (dummy) coding with interactions silently turns "main effects" into simple effects.
- A non-significant interaction is not evidence the effects are equal.
- Don't compare a significant effect in group A with a non-significant one in B —
  test the interaction.
- Uncertain: df approximations differ; small samples can give noticeably different p.
- Checked 2026-10-19: `lme4`, `afex`, `emmeans`, `lmerTest`, `brms`, `BayesFactor`, `performance` and `mice` exist on CRAN. The R code, the Barr et al. (2013), Matuschek et al. (2017) and Westfall et al. (2014) attributions and the `allFit()` advice were not run or re-read (gated: unconfirmed, source is paywalled or blocked).

## Verify
- [ ] Contrasts set deliberately and stated.
- [ ] Random-effects structure justified; any simplification reported.
- [ ] Convergence checked with alternative optimisers.
- [ ] Raw-unit effects with CIs and a named standardised effect size reported.
- [ ] Model diagnostics and per-participant plots inspected.
