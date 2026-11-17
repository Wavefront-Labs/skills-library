---
id: mathematics.applied-data-analysis-and-visualization.quantitative-reasoning.fermi-estimates-and-base-rate-checks
name: fermi-estimates-and-base-rate-checks
category: mathematics
field: applied-data-analysis-and-visualization
product: quantitative-reasoning
tags: [quantitative-reasoning, numeracy, fermi-estimation, fermi-problem, back-of-the-envelope, order-of-magnitude, sanity-check, base-rate, base-rate-fallacy, bayes-theorem, natural-frequencies, false-positive, ppv, relative-risk, absolute-risk, survivorship-bias, regression-to-the-mean, selection-bias, statistical-literacy, interpreting-statistics, critical-thinking, data-analysis]
level: intro
status: verified
description: "Estimate any quantity to within a factor of a few with Fermi decomposition, and check reported statistics with base rates, natural frequencies and a short list of standard traps."
sources: ["Weinstein & Adam, Guesstimation (Princeton UP)", "Gigerenzer, Reckoning with Risk / Calculated Risks", "Spiegelhalter, The Art of Statistics (Pelican)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fermi estimates and base-rate checks

**Goal:** produce a quick, defensible number when you have no data, and catch a wrong
or misleading number in a report before you repeat it.

## 1. Fermi estimation
1. **Define the target precisely,** with units ("litres of milk sold per year in a city of
   1 million").
2. **Decompose** into factors you can estimate: people × fraction who drink milk ×
   litres per drinker per week × 52.
3. **Estimate each factor** with a range you'd bet on; use the geometric mean of the
   bounds when unsure across orders of magnitude (between 10 and 1,000 → ~100, not 500).
4. **Multiply,** carry 1–2 significant figures, keep powers of ten explicit.
5. **Cross-check by a second route** (e.g. supply side: number of supermarkets × litres
   per store per day). Two independent routes within ~3× of each other = good enough.
Errors in independent factors partly cancel, which is why Fermi estimates work better
than they feel like they should. A factor wrong by 100× doesn't cancel — sanity-check each.

Useful anchors (approximate): world population ~8 billion; seconds in a year ≈ π × 10⁷;
a person needs ~2,000–2,500 kcal/day; a car travels ~10–20 thousand km/year.

## 2. Sanity-check a reported number
- **Units and scale:** per day or per year? thousands or millions? Re-derive it per person
  or per household and see if it is plausible.
- **Denominator:** "1,000 incidents" — out of how many? Rate per what?
- **Compared with what:** last year, a control group, the national average?
- **Implied totals:** if every school in the country did X, would the total exceed the
  number of pupils?

## 3. Base rates and Bayes with natural frequencies
A test with 90% sensitivity and 95% specificity for a condition with 1% prevalence. Take
**1,000 people**:
- 10 have it → 9 test positive.
- 990 don't → 5% = ~50 test positive falsely.
- Positives = 59; truly ill = 9 → **PPV ≈ 15%**.
Most people guess ~90%. Counting people (natural frequencies) instead of multiplying
conditional probabilities makes the base rate impossible to ignore. Same logic for fraud
alerts, screening, security scans and "AI detector" claims.

## 4. The standard traps
- **Relative vs absolute risk:** "risk up 50%" from 2 to 3 in 10,000.
- **Regression to the mean:** extreme values selected for treatment (worst schools,
  accident blackspots) improve on remeasurement even if nothing is done.
- **Survivorship / selection bias:** only successful funds, surviving planes, or
  responders are in the data.
- **Correlation vs causation:** look for a confounder that drives both (ice cream and
  drownings → summer).
- **Small samples and many comparisons:** with 20 subgroups, one "significant" result at
  p < 0.05 is expected by chance.
- **Averages hiding spread:** mean income rising while the median falls.
- **Precision theatre:** "37.42% of people" from a survey of 200 (± ~7 points).

## 5. Report your own numbers well
Give the estimate, a range, the main assumptions and which one dominates the uncertainty.
Prefer "about 20–50 thousand, most sensitive to X" over a false-precision single value.

## Uncertainty notes
Computed: PPV = 9 / (9 + 49.5) = 15.4%; pi x 10^7 = 3.14e7 s against 3.156e7 s in a Julian year; 1.96 x sqrt(0.25/200) = 6.9 points. Anchor values are rounded approximations meant for estimation only. The survey margin
(±~7 points for n = 200 at 50%) is the usual 95% simple-random-sample approximation and is
larger for non-random samples.

## Verify
- [ ] Target defined with units; decomposition written out.
- [ ] Each factor has a range; result cross-checked by a second route.
- [ ] Reported statistics checked for units, denominator and comparison.
- [ ] For any test/classifier claim, PPV worked out with natural frequencies.
- [ ] Traps list run through before quoting a claim.
