---
id: creative-arts.design-for-form-and-experience.ux-design.designing-an-ab-test
name: designing-an-ab-test
category: creative-arts
field: design-for-form-and-experience
product: ux-design
tags: [ab-test-design, ab-testing, product-analytics, experimentation, hypothesis, statistical-power, conversion-optimisation]
level: practitioner
status: draft
description: "Design a valid A/B test: hypothesis, one primary metric, guardrails, sample size from baseline and minimum detectable effect, fixed duration, and no peeking."
sources:
  - "Kohavi, Tang and Xu, Trustworthy Online Controlled Experiments (Cambridge University Press, 2020)"
  - "Nielsen Norman Group - A/B Testing 101 (nngroup.com/articles/ab-testing-and-ux)"
  - "Evan Miller - Sample Size Calculator (evanmiller.org/ab-testing)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Designing an A/B test

**Goal:** a test whose result you can trust and act on.

## Steps
1. **Hypothesis:** "Changing X to Y for audience Z will move metric M because reason R." No reason, no test.
2. **Primary metric:** one (e.g. checkout completion per visitor). Add **guardrail metrics** that must not worsen (page load, refund rate, support contacts) and a few diagnostics.
3. **Unit of randomisation:** usually user, not session or page view. Keep users in their variant across visits. Check that the metric's denominator is the same unit.
4. **Sample size:** from baseline rate, **minimum detectable effect** (relative lift worth shipping, say 5 percent) alpha 0.05 and power 0.8. Example: baseline 10 percent, detect +5 percent relative needs roughly 60k users per arm. If traffic cannot reach it, test a bigger change or use qualitative methods.
5. **Duration:** run for the planned n and for at least one or two full weekly cycles (7 or 14 days) to cover weekday effects and novelty.
6. **Sample ratio check:** verify the actual split matches the planned (chi-square test). A mismatch means a bug; discard the result.
7. **Analyse once** at the planned end. Peeking and stopping on first significance inflates false positives (use sequential methods only if built in).
8. **Decide** with the interval, not only p: ship if the interval's lower bound is above your cost threshold and guardrails hold.

## Gotchas
- Many variants or many metrics raise false positives; correct (Bonferroni) or state them as exploratory.
- Novelty and primacy effects fade; for big UI changes re-check after two weeks.
- Do not test when you cannot act on either outcome.

## Verify
- [ ] Hypothesis, primary metric, guardrails and sample size written before launch.
- [ ] Sample ratio check passed; run length met.
- [ ] Decision recorded with interval and guardrail status.
