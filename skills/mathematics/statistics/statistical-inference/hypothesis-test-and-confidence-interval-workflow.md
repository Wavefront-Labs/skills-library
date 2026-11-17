---
id: mathematics.statistics.statistical-inference.hypothesis-test-and-confidence-interval-workflow
name: hypothesis-test-and-confidence-interval-workflow
category: mathematics
field: statistics
product: statistical-inference
tags: [statistics, statistical-inference, frequentist, hypothesis-testing, null-hypothesis, p-value, confidence-interval, effect-size, t-test, welch-t-test, chi-squared-test, mann-whitney, wilcoxon, power-analysis, type-i-error, type-ii-error, multiple-testing, bonferroni, holm, benjamini-hochberg, false-discovery-rate, maximum-likelihood, mle, standard-error, bootstrap, scipy, statsmodels, r]
level: practitioner
status: verified
description: "Run a frequentist analysis properly: fix the question and alpha first, pick the test, report effect size with a CI, check assumptions, and control multiple testing."
sources: ["https://stat.ethz.ch/R-manual/R-devel/library/stats/html/t.test.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hypothesis test and confidence interval workflow

**Goal:** turn "is there a difference?" into a defensible statement — an estimated
effect, its uncertainty, and a test whose error rates you actually controlled.

## 1. Decide before you look at the data
Write down, in advance:
- **The estimand** — the single number you care about (difference in means, a ratio
  of proportions, a slope). A test without a named estimand is a fishing trip.
- **H0 and H1**, and whether H1 is one- or two-sided. Default two-sided; a one-sided
  test chosen *after* seeing the direction doubles your real false-positive rate.
- **alpha** (usually 0.05) and the **smallest effect worth detecting**.
- **Sample size from a power calculation** (step 5). Stopping when p < 0.05 ("peeking")
  inflates Type I error badly — in a simulation of a z-test on null data, 5 equally spaced looks give about 14% and 20 looks about 25% false positives.

## 2. Pick the test from the data shape
| Data | Default test | Notes |
|---|---|---|
| Two independent means | **Welch t-test** | Do not use Student's equal-variance t by default; Welch costs almost nothing when variances are equal. |
| Paired measurements | Paired t-test on the differences | Pairing is a design fact, not a choice made later. |
| Two proportions | Two-proportion z / chi-squared; Fisher's exact if any expected count < 5 | |
| Contingency table | Chi-squared test of independence | Check expected counts, not observed. |
| Skewed / ordinal, small n | Mann–Whitney U / Wilcoxon signed-rank | Tests stochastic ordering, *not* "medians" unless shapes match. |
| 3+ group means | One-way ANOVA (Welch ANOVA if variances differ), then planned contrasts | |
| Awkward statistic (median, ratio) | Bootstrap percentile or BCa CI, ≥ 2,000 resamples | |

Python: `scipy.stats.ttest_ind(a, b, equal_var=False)` (runs, returns Welch df); R: `t.test(a, b)` (R documentation: `var.equal` defaults to FALSE, so Welch is the default).

## 3. Report the estimate, not just the verdict
Always give: **point estimate, 95% CI, p-value, n per group**. Example:
"Mean difference 2.4 s (95% CI 0.6 to 4.2), Welch t = 2.61, df ≈ 87, p = 0.011,
n = 45 / 46." The CI carries the information the p-value hides: a tiny p with a CI
of 0.01 to 0.03 units may be practically irrelevant; a p of 0.08 with a CI of −0.5 to
9 means "underpowered", not "no effect".

Interpretation guardrails:
- p is P(data this extreme | H0 true), **not** P(H0 true | data).
- "Not significant" ≠ "no difference". To claim equivalence, use an equivalence test
  (TOST) against a pre-stated margin.
- A 95% CI procedure covers the true value in 95% of repetitions; any single interval
  either does or does not.

## 4. Check assumptions that actually matter
- **Independence** is the one that kills you: repeated measures on the same person,
  clustered users, time-correlated rows. Violations shrink standard errors and make
  everything "significant". Fix with paired/mixed models or cluster-robust SEs.
- Normality matters less than people think for means with n ≳ 30 per group (CLT), but
  heavy tails and outliers still matter — plot the data (histogram/QQ) before testing.
- Do not run a normality test and then branch on its result; choose the robust method up front.

## 5. Power and sample size
For two means: n per group ≈ 2·(z₁₋α/₂ + z₁₋β)²·σ²/δ². With alpha 0.05 and 80% power,
(1.96 + 0.84)² ≈ 7.85, so n ≈ 15.7·σ²/δ². Detecting half a standard deviation (δ/σ = 0.5)
needs ≈ 63 per group (the exact t-based answer is 64; recomputed 62.8 and 63.77 with `statsmodels.stats.power.TTestIndPower`). Tools: `statsmodels.stats.power`,
R `pwr`, G*Power. Use a pilot or literature σ, and inflate for dropout.

## 6. Multiple comparisons
Testing m hypotheses at 0.05 each gives a family-wise error far above 0.05.
- **Holm** (step-down Bonferroni) controls family-wise error and is uniformly better
  than plain Bonferroni — use it when any false positive is costly.
- **Benjamini–Hochberg** controls the false discovery rate — use it for screening
  many features/genes/metrics.
- Python: `statsmodels.stats.multitest.multipletests(p, method="holm" | "fdr_bh")`;
  R: `p.adjust(p, "holm")`.
Subgroup analyses and "we also looked at…" count toward m even if unreported.

## Gotchas
- Huge n makes trivial effects significant; tiny n makes real effects invisible. Read the CI.
- Excluding outliers after seeing the result is a forking path; set rules in advance.
- Uncertain: the "≥ 2,000 bootstrap resamples" figure is a common rule of thumb for
  percentile CIs, not a hard threshold; BCa tails may need more.

## Verify
- [ ] Estimand, hypotheses, alpha and sample size were fixed before analysis.
- [ ] Test matches design (independent vs paired; Welch by default).
- [ ] Output reports estimate + 95% CI + p + n, in the outcome's units.
- [ ] Independence of observations was checked and handled.
- [ ] Multiple tests are adjusted (Holm or BH) and the count m is honest.
- [ ] Conclusion is phrased about the effect size, not just "significant".
