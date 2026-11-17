---
id: sales-marketing.market-research-consumer-insights.pricing-research.van-westendorp-gabor-granger-and-conjoint
name: van-westendorp-gabor-granger-and-conjoint
category: sales-marketing
field: market-research-consumer-insights
product: pricing-research
tags: [pricing-research, price-research, willingness-to-pay, wtp, van-westendorp, price-sensitivity-meter, psm, newton-miller-smith, gabor-granger, demand-curve, price-elasticity, conjoint, choice-based-conjoint, cbc, discrete-choice, sawtooth, conjointly, price-feature-trade-off, promotion-response, revenue-maximisation, consumer-insights]
level: advanced
status: draft
description: "Research what buyers will pay: run Van Westendorp for an acceptable range, Gabor-Granger for a demand curve, choice-based conjoint for price-feature trade-offs, and read promo response."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Van Westendorp, Gabor-Granger and conjoint — pricing research

**Goal:** give a pricing decision evidence about willingness to pay, choosing
the method that fits the question. Rule of thumb: Van Westendorp for a
**new product's plausible range**, Gabor-Granger for a **demand/revenue curve at
specific prices**, conjoint when price must be traded against **features or
competitors**. All stated-preference methods overstate real willingness to pay —
read the *shape* of results more than the absolute numbers.

## 1. Van Westendorp Price Sensitivity Meter
Show the product description, then ask four open numeric questions:
1. At what price would it be so **cheap** you'd doubt the quality? (*too cheap*)
2. At what price would it be a **bargain** — a great buy for the money? (*cheap*)
3. At what price would it start to seem **expensive** but you'd still consider it? (*expensive*)
4. At what price would it be **too expensive** to consider? (*too expensive*)
Analysis:
- Clean illogical answers (too cheap ≥ cheap ≥ expensive ≥ too expensive must be
  ordered) — drop or fix those respondents; typically 5–15%.
- Plot cumulative % for *too cheap* and *cheap* (descending with price) and
  *expensive* and *too expensive* (ascending). Also plot "not cheap" (1 − cheap)
  and "not expensive" (1 − expensive).
- Common intersection reads (definitions vary across practitioners):
  - **PMC** (marginal cheapness) = too cheap × not cheap;
  - **PME** (marginal expensiveness) = too expensive × not expensive;
  - Range of acceptable prices = PMC to PME;
  - **OPP** (optimal) = too cheap × too expensive; **IPP** (indifference) = cheap × expensive.
- **Newton-Miller-Smith extension:** add purchase-likelihood questions at the
  respondent's own "cheap" and "expensive" prices to get a demand/revenue curve.
Limits: no competitive context; answers anchor on any price cues in the concept.

## 2. Gabor-Granger
- Pick 5–7 price points across a realistic range. Ask purchase likelihood
  (5-point scale or yes/no) at a starting price, then move up if yes / down if no
  (or show each respondent one random price — **monadic** — to avoid anchoring;
  needs more sample).
- Demand at each price = % "definitely" + a down-weighted "probably" (common
  calibration e.g. 70–80% of definites, 20–30% of probables — **uncertain:**
  calibrate against your own launch history if you have it).
- Revenue index = price × demand; profit index = (price − unit cost) × demand.
  Pick the price maximising the objective; look for steep cliffs (often just above
  round-number thresholds like 9.99 → 10.49).

## 3. Choice-based conjoint (CBC)
- Define attributes (brand, 2–5 features, price) with 2–5 levels each; price levels
  spanning the realistic range.
- Each respondent sees 8–15 choice tasks of 3–4 profiles plus "none". Tools:
  Sawtooth (Lighthouse Studio/Discover), Conjointly, Qualtrics Conjoint, or R/Python
  with an HB or multinomial-logit estimator.
- Sample: ≥ 300 per segment you need to read, more with many attributes.
- Outputs: part-worth utilities, attribute importance, **willingness to pay**
  per feature (utility difference ÷ price utility per unit), and a **market
  simulator** that predicts share of preference at given prices vs competitors.
- Use the simulator to test price moves, feature bundles and competitor reactions.
- Include the "none" option so you can see demand loss, not just share shifts.

## 4. Promotion-response reads
Prefer real data: store/e-commerce tests (A/B price cells, matched-store tests)
with a pre-period and control. Read uplift, cannibalisation, pull-forward (post-promo
dip) and incremental margin, not just unit lift.

## Gotchas
- Never show the current price in the concept unless that's the question.
- Heavy category users and category experts skew all methods; quota by user type.
- Conjoint predicts *share of preference*, not market share — awareness and
  distribution aren't in the model.
- Report price ranges and sensitivity, not a single "the price is $X".

## Verify
- [ ] Method chosen to match the question (range / curve / trade-off).
- [ ] VW illogical responses cleaned; intersection definitions stated.
- [ ] Gabor-Granger intent calibrated and objective (revenue vs profit) explicit.
- [ ] Conjoint design balanced, includes "none", sample ≥ 300 per key segment.
- [ ] Recommendations given as a range with sensitivities.
