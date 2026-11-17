---
id: social-sciences.food-science-research.consumer-food-research.discrete-choice-experiments-on-food-labels
name: discrete-choice-experiments-on-food-labels
category: social-sciences
field: food-science-research
product: consumer-food-research
tags: [consumer-food-research, food-choice, discrete-choice-experiment, dce, choice-based-conjoint, food-labelling, front-of-pack-labels, nutri-score, organic-label, eco-label, novel-foods, alternative-protein, willingness-to-pay, wtp, mixed-logit, latent-class, conditional-logit, d-efficiency, ngene, apollo, mlogit, hypothetical-bias, cheap-talk, opt-out, attribute-non-attendance, eye-tracking]
level: advanced
status: draft
description: "Run discrete choice experiments on food labels and novel foods: attribute/level choice, efficient designs, opt-outs, hypothetical-bias controls, mixed/latent-class logit and WTP estimation."
sources:
  - "Lusk & Shogren, Experimental Auctions (2007) and Lusk (2003) on cheap talk, AJAE"
  - "Louviere, Hensher & Swait, Stated Choice Methods (2000)"
  - "Hess & Palma (2019), Apollo: a flexible estimation package, J. Choice Modelling"
  - "Hensher, Rose & Greene, Applied Choice Analysis (2nd ed.)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Discrete choice experiments on food labels

**Goal:** estimate how much consumers value food attributes — a front-of-pack nutrition
grade, an organic or carbon label, a "contains insect protein" claim — and how
preferences differ across people, using a stated-choice design grounded in random
utility theory. (Commercial pricing/conjoint work is covered in
sales-marketing.market-research-consumer-insights.pricing-research.van-westendorp-gabor-granger-and-conjoint.)

## 1. Attributes and levels
- Derive from literature, focus groups and real shelves: typically 4–6 attributes,
  including **price** (needed for WTP) and the focal label.
- Levels must be realistic and span market reality (prices from actual store audits).
- Avoid implausible combinations (e.g. a premium label on the cheapest level) or
  restrict them in the design.
- Show labels as images on a realistic pack where the label's *visual* form is what's
  studied; text-only attribute grids measure something different.

## 2. Experimental design
- **Efficient designs** (D-efficient, Bayesian D-efficient with priors from a pilot)
  generated in **Ngene** or R (`idefix`, `support.CEs`); orthogonal designs are simpler
  but less efficient.
- 2–3 product alternatives + an **opt-out / "none"** (realistic — people can walk away;
  omitting it inflates WTP).
- 8–12 choice tasks per respondent, split into blocks if the design is larger.
- Randomise task order and alternative position.

## 3. Survey and bias control
- **Hypothetical bias**: stated WTP usually exceeds real WTP. Counter with a
  **cheap-talk script**, an honesty priming/oath, or making it **incentive-compatible**
  (one choice randomly binding with real products and money — strongest, costly).
- Pilot (n ≈ 30–50) to check comprehension and obtain priors.
- Collect attitudes (food neophobia scale for novel foods, health/environment concern),
  label knowledge, and demographics for heterogeneity.
- Add debrief questions on **attribute non-attendance** ("which attributes did you
  ignore?") or use eye-tracking in lab versions.
- Samples: online panels with quotas; several hundred respondents is typical for mixed
  logit, more for latent-class segmentation (rough guide — simulate with your design).

## 4. Estimation
1. **Conditional (multinomial) logit** baseline.
2. **Mixed logit** (random parameters, e.g. normal for labels, log-normal or fixed for
   price) to capture heterogeneity; or **latent-class logit** for segments.
3. Estimate in **Apollo** (R), `mlogit`/`gmnl` (R), Stata `cmmixlogit`/`lclogit`, or
   Biogeme (Python). Use enough Halton/Sobol draws (e.g. 500+) and check stability.
4. **WTP** = −β_attribute / β_price; better, estimate in **WTP space** directly to
   avoid the extreme ratios of random coefficients. Report delta-method or Krinsky–Robb CIs.
5. Model attribute non-attendance and interactions with attitudes as extensions.

## Gotchas
- A label effect can reflect information (people learn the product is low-sugar) or
  trust in the label itself; design to separate them if that matters.
- Price levels anchor WTP — too-wide ranges inflate it.
- Status-quo/"none" heavy choosers may be protest responses; analyse, don't just delete.
- Results from Europe vs elsewhere often don't transfer for labels with regional
  recognition (e.g. Nutri-Score).
- Uncertain: sample-size heuristics and draw counts vary by model; check convergence.

## Verify
- [ ] Attributes/levels realistic (store audit) and include price and opt-out.
- [ ] Efficient design with pilot priors; blocks and randomisation in place.
- [ ] Hypothetical-bias mitigation used and reported.
- [ ] Heterogeneity modelled (mixed or latent class); WTP CIs reported.
- [ ] Attribute non-attendance considered.
