---
id: mathematics.numeracy-and-mental-calculation.estimation.fermi-estimation-and-plausibility-checks
name: fermi-estimation-and-plausibility-checks
category: mathematics
field: numeracy-and-mental-calculation
product: estimation
tags: [numeracy-and-mental-calculation, estimation, fermi-estimation, fermi-problems, back-of-the-envelope, order-of-magnitude, rounding, compatible-numbers, sanity-check, plausibility, scientific-notation, powers-of-ten, geometric-mean, decomposition, market-sizing, guesstimate, reference-numbers, unit-analysis, error-bounds, number-sense]
level: intro
status: draft
description: "Get fast approximate answers and catch wrong ones: round to compatible numbers, decompose Fermi problems, work in powers of ten, bracket with low/high bounds, and keep reference numbers handy."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fermi estimation and plausibility checks

**Goal:** produce a defensible "about how much?" in a minute, and instantly spot
answers (yours, a spreadsheet's, a headline's) that are off by a factor of 10 or more.

## 1. Rounding for speed: compatible numbers
Round to numbers that make the *operation* easy, not just to the nearest ten.
- 487 ÷ 23 → 480 ÷ 24 = 20.
- 6.8 × 31 → 7 × 30 = 210 (true 210.8).
- When multiplying, round one factor up and the other down to cancel bias:
  38 × 62 → 40 × 60 = 2,400 (true 2,356).
- Track the direction: if you rounded everything up, the estimate is an upper bound.

## 2. Powers of ten
Write numbers as a × 10ⁿ with a between 1 and 10, then multiply the a's roughly and add
exponents. 3,000 × 40,000 = 3 × 4 × 10^(3+4) = 12 × 10⁷ = 1.2 × 10⁸.
Rule of thumb for "one significant figure" work: round a to 1, 2, 3 or 5, or simply to
1 or 3 (≈ √10) for pure order-of-magnitude.

## 3. Fermi decomposition
Break an unknowable quantity into factors you can estimate.
*How many litres of milk does a city of 1 million drink per week?*
- People: 1,000,000.
- Share who drink milk regularly: ~70%? → 700,000.
- Average per drinker: ~200 ml/day? → 1.4 litres/week.
- Total ≈ 700,000 × 1.4 ≈ 1 million litres/week.
Write each factor with its basis; errors in independent factors partly cancel, which
is why Fermi estimates are often within a factor of 2–3.

## 4. Bracket with bounds
For each uncertain factor give a low and a high you'd be surprised to fall outside.
Combine lows and highs separately for an outer range; if a single number is needed, take
the **geometric mean** of low and high (low 10, high 1,000 → √(10 × 1,000) = 100), which
fits multiplicative uncertainty better than the arithmetic mean.

## 5. Plausibility checks
Before trusting any figure:
- **Units:** does the answer come out in the right units? Litres/week × weeks = litres.
- **Per-capita check:** divide by population — "£50 billion spent by a country of
  70 million on X" = ~£700 per person per year. Plausible?
- **Compare with a known quantity** (reference numbers below).
- **Extremes:** set an input to 0 or very large — does the model behave sensibly?
- **Decimal sense:** a 5% figure vs 0.05 vs 50 — the factor-100 slip is the commonest error
  in spreadsheets.

## 6. Reference numbers worth memorising
Approximate — check the current value when it matters:
- Seconds in a day ≈ 86,400 (~10⁵); in a year ≈ 3.15 × 10⁷ (π × 10⁷).
- World population ~8 billion; UK ~69 million; USA ~340 million (2020s estimates).
- 1 mile ≈ 1.6 km; 1 kg ≈ 2.2 lb; 1 inch = 2.54 cm; 1 US gallon ≈ 3.8 L.
- Walking ~5 km/h; car on motorway ~100–120 km/h; jet ~900 km/h.
- 1 litre of water = 1 kg; 1 m³ = 1,000 L.
- Rule of 72: money at r% doubles in about 72/r years (6% → ~12 years).

## 7. When an estimate is enough
Ask: would a 20% error change the decision? If not, estimate. Deciding whether a
shopping trolley is under £100, whether a trip fits in a day, whether a project is
"weeks or months" — estimates serve. Dosages, tax filings and engineering margins need
exact calculation (and checking).

## Gotchas
- Anchoring: the first number you hear pulls your estimate. Estimate independently first.
- Overconfidence: people's "90% ranges" contain the truth far less than 90% of the time;
  widen your bounds.
- Double counting factors in decomposition (counting households and people).
- Uncertain: population figures above are rounded mid-2020s values; refresh them.

## Verify
- [ ] Estimate is within a factor of ~2 of a known answer on practice problems.
- [ ] Every factor has a stated basis and a low/high range.
- [ ] Units carried through and checked.
- [ ] Per-capita or reference comparison done for large figures.
- [ ] You state whether the estimate is an upper bound, lower bound or central guess.
