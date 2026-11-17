---
id: mathematics.applied-data-analysis-and-visualization.descriptive-statistics.choosing-summaries-that-do-not-mislead
name: choosing-summaries-that-do-not-mislead
category: mathematics
field: applied-data-analysis-and-visualization
product: descriptive-statistics
tags: [descriptive-statistics, summary-statistics, mean, median, mode, trimmed-mean, geometric-mean, harmonic-mean, weighted-average, standard-deviation, iqr, mad, percentiles, quantiles, rates, ratios, per-capita, percentage-points, relative-change, index-numbers, base-year, simpsons-paradox, average-of-ratios, denominators, misleading-statistics, data-analysis]
level: intro
status: verified
description: "Choose centre, spread, rates and index numbers that describe data honestly: mean vs median, the right average for ratios, denominators, percentage points, and weighting."
sources: ["Freedman, Pisani & Purves, Statistics (Norton)", "Huff, How to Lie with Statistics (1954)", "OECD/ILO consumer price index manuals (index number concepts)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choosing summaries that do not mislead

**Goal:** pick the one or two numbers that fairly represent a dataset, and avoid the
classic summaries that are technically correct and practically misleading.

## 1. Centre
- **Mean** when the distribution is roughly symmetric and totals matter (budget per head).
- **Median** for skewed data (incomes, house prices, response times) — the mean is pulled
  by the tail. Report both if the audience may expect either; the gap itself is information.
- **Trimmed mean** (e.g. 10% each side) when you want mean-like behaviour that resists outliers.
- **Geometric mean** for growth factors: returns of +50% then −50% average to 0%
  arithmetically but the asset lost 25%; geometric mean of 1.5 and 0.5 is ≈ 0.866 →
  −13.4% per period.
- **Harmonic mean** for averaging rates over equal *amounts* (average speed over equal
  distances; average price per share when investing equal money each time).
- Mode only for categories or clearly peaked discrete data.

## 2. Spread
- SD with the mean; **IQR** (or 10th–90th percentiles) with the median.
- MAD (median absolute deviation) as a robust SD; ×1.4826 ≈ SD for normal data.
- Range is dominated by two extreme points — rarely the right choice.
- Always state n. A percentage of 12 people is not the same claim as of 12,000.

## 3. Rates and ratios
- **Choose the denominator deliberately**: accidents per driver, per trip, per km driven
  give different rankings. Name the denominator in the label.
- **Average of ratios ≠ ratio of totals.** Mean of hospital-level death rates weights a
  tiny hospital equally with a large one; total deaths ÷ total patients doesn't. Decide
  which question you are answering.
- **Simpson's paradox:** a rate can be higher overall yet lower in every subgroup when
  group mixes differ. Show stratified rates or a standardised rate (direct
  standardisation to a common population mix).
- Small denominators produce extreme rates; show counts alongside, or use funnel plots /
  shrinkage when ranking units.

## 4. Changes and percentages
- **Percentage points vs percent:** 4% → 6% is +2 percentage points but +50%.
- Relative risk sounds bigger than absolute risk: "doubles the risk" from 1 in 10,000 to 2 in
  10,000. Give both.
- A fall of 50% needs a rise of 100% to recover. Don't average percentage changes.
- Choose the base period consciously; starting a chart or comparison at an unusual
  peak or trough manufactures a trend.

## 5. Index numbers
- An index = value / base value × 100. Make the base year and basket explicit.
- **Laspeyres** (base-period weights) tends to overstate price rises when people substitute;
  **Paasche** (current weights) tends to understate; Fisher = geometric mean of the two.
- Chain-linking avoids stale weights but makes components non-additive.
- Deflate money series to real terms before comparing across years; say which price index.

## 6. Weighting
Survey or sample data with design weights must be summarised with them (`np.average(x,
weights=w)`, R `weighted.mean`), and so must any average of group averages (weight by
group size). Unweighted summaries of weighted samples describe the sample, not the population.

## Uncertainty notes
These are standard conventions; the Laspeyres/Paasche bias direction holds under
typical substitution behaviour, not always. Statistical-agency index methods are more
involved than shown here.
Checked numerically: geometric mean of 1.5 and 0.5 is 0.866; MAD x 1.4826 matches SD on normal data; with a
two-good example where the consumer substitutes away from the dearer good, Laspeyres 1.50 >= Fisher 1.29 >= Paasche 1.11.

## Verify
- [ ] Centre and spread chosen to match the distribution shape, with n stated.
- [ ] Every rate names its numerator and denominator.
- [ ] Average-of-ratios vs ratio-of-totals choice is deliberate.
- [ ] Changes reported as percentage points where the quantity is already a percentage.
- [ ] Absolute and relative figures both given for risks.
- [ ] Weights applied where the data or the grouping requires them.
