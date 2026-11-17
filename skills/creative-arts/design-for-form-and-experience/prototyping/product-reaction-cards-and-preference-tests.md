---
id: creative-arts.design-for-form-and-experience.prototyping.product-reaction-cards-and-preference-tests
name: product-reaction-cards-and-preference-tests
category: creative-arts
field: design-for-form-and-experience
product: prototyping
tags: [product-reaction-cards, concept-testing, preference-test, desirability-testing, microsoft-desirability-toolkit, a-b-preference, concept-validation]
level: practitioner
status: draft
description: "Test concept desirability with Microsoft Product Reaction Cards and run preference tests between designs, with sample sizes, analysis and bias controls."
sources:
  - "Joey Benedek and Trish Miner, Measuring Desirability: New Methods for Evaluating Desirability in a Usability Lab Setting (Microsoft, 2002)"
  - "Nielsen Norman Group - Preference testing and concept testing (nngroup.com)"
  - "UsabilityHub / Lyssna - Preference Test guide (lyssna.com/guides/preference-test)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Product Reaction Cards and preference tests

## Product Reaction Cards (desirability toolkit)
- A set of **118 words** (positive and negative, about 60/40: accessible, appealing, busy, confusing, creative, dated, fresh, intimidating, professional, trustworthy, ...).
- **Procedure:** after a participant sees a design or finishes a task, ask them to pick **5 words** that best describe it, then explain each choice. Record words and reasons.
- **Analysis:** tally word frequency per design, build a word cloud, compare with the **target brand attributes** (`creative-arts.design-for-form-and-experience.mood-boarding.measuring-attributes-with-semantic-differential-scales`); count positive/negative balance; use reasons for qualitative themes.
- **Sample:** 10-20 for qualitative; 25+ for comparing counts.
- Use a subset of 25-60 words tailored to your context for online tests; keep both polarities.

## Preference test
- Show **two or more** designs (A/B, side-by-side or sequentially) and ask which they prefer and **why**; collect a rationale in free text, and optionally ratings of attributes (clarity, trust, appeal).
- **Controls:** randomise order and left/right position; use the same content, size and context; avoid leading questions; test with representative users; **between-subject** (each sees one) for unbiased ratings, **within-subject** for forced choice.
- **Sample size:** for 70/30 preference at 95 percent confidence about 40-50 respondents; use a binomial test or confidence interval for proportions; for 55/45 you need hundreds.
- Tools: Lyssna (UsabilityHub), Maze, Optimal Workshop, Qualtrics, Typeform.

## Reporting
Show win rate with intervals, top words, representative quotes, and a recommendation. Preference is **not** usability or business performance; combine with task-based testing (`creative-arts.design-for-form-and-experience.prototyping.running-a-prototype-walkthrough-test`).

## Verify
- [ ] Words or options randomised; both positive and negative terms included.
- [ ] Sample size supports the claimed difference; intervals reported.
- [ ] Rationales analysed alongside counts.
