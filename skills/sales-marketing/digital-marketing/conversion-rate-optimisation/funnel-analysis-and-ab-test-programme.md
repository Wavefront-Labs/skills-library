---
id: sales-marketing.digital-marketing.conversion-rate-optimisation.funnel-analysis-and-ab-test-programme
name: funnel-analysis-and-ab-test-programme
category: sales-marketing
field: digital-marketing
product: conversion-rate-optimisation
tags: [conversion-rate-optimisation, conversion-rate-optimization, cro, funnel-analysis, drop-off, landing-page-optimisation, checkout-optimisation, ab-testing, split-testing, multivariate-testing, hypothesis, pie-prioritisation, ice-score, sample-size, statistical-significance, minimum-detectable-effect, session-recordings, heatmaps, hotjar, microsoft-clarity, user-testing, friction, ga4, optimizely, vwo]
level: practitioner
status: draft
description: "Turn more visitors into buyers: find the leaking funnel step, research why with recordings and user tests, prioritise hypotheses, run properly sized A/B tests and read them without fooling yourself."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Conversion rate optimisation — funnel, research, test, decide

**Goal:** a steady programme of evidence-based changes that raise conversion, rather
than redesigns driven by opinion.

## 1. Find where the funnel leaks
- Define the funnel steps in analytics (e.g. GA4 funnel exploration): landing → product
  view → add to cart → checkout start → payment → purchase (or for lead gen: landing →
  form start → form submit → qualified).
- Segment each step by **device**, **traffic source**, new vs returning, and landing page.
  Averages hide the problem: mobile checkout may convert at half of desktop.
- Pick the step with the largest absolute loss of potential revenue, not just the worst rate.

## 2. Find out *why* (qualitative research)
- **Session recordings and heatmaps** (Microsoft Clarity, Hotjar or similar): watch
  20–50 sessions of people who dropped at the leaking step. Note rage clicks, dead
  clicks, scrolling past the CTA, form-field hesitation, error messages.
- **On-page polls / exit surveys:** "What's stopping you from buying today?"
- **User tests:** 5 people attempting a task while thinking aloud catch most major
  usability problems.
- **Form analytics:** which field causes abandonment.
- **Check the basics:** page speed, broken elements on specific browsers/devices,
  surprise costs (shipping shown late), forced account creation.

## 3. Write and prioritise hypotheses
Format: "Because we saw **[evidence]**, we believe **[change]** for **[audience]** will
**[improve metric]**." Score with a simple framework — **ICE** (impact, confidence,
ease) or **PIE** (potential, importance, ease), 1–10 each. Fix obvious bugs
immediately without testing — testing a broken checkout button wastes traffic.

## 4. Run a proper A/B test
- Tools: Optimizely, VWO, AB Tasty, Convert, or server-side/feature-flag testing.
  (Google Optimize was retired in 2023.)
- **Primary metric** chosen upfront (e.g. purchases per visitor), plus guardrails
  (revenue per visitor, refund rate).
- **Sample size before launch:** set baseline conversion rate, minimum detectable effect
  (MDE) and 95% significance/80% power in a calculator. Example: baseline 3%, wanting to
  detect a 10% relative lift → roughly 50k+ visitors per variant. If you don't have
  the traffic, test bigger changes or higher-traffic steps.
- Run for **full weeks** (at least 1–2 business cycles), even if significance arrives early.
- QA every variant on main browsers/devices before launch; check the split is ~50/50
  (a **sample ratio mismatch** signals a broken test).

## 5. Read the result
- Stopped at the planned sample/duration? Sample ratio OK?
- Look at the confidence interval for the lift. Interval crossing zero = inconclusive,
  not "no effect".
- Check key segments (device) for opposite effects, but treat segment findings as new
  hypotheses, not wins.
- Ship winners, document everything (hypothesis, screenshots, result, learning) in a
  test log, and plan the next iteration.

## Gotchas
- Peeking and stopping early inflates false positives dramatically.
- Many tests lose or are flat — that's normal; the learning still counts.
- Novelty effects fade; re-check big wins after a few weeks.
- Conversion rate up but average order value down can lose money; watch revenue per visitor.
- Testing tools that flicker (original visible before variant) bias results.

## Verify
- [ ] Funnel built and segmented by device and source; biggest revenue leak identified.
- [ ] At least two qualitative sources explain the leak.
- [ ] Hypotheses written with evidence and scored.
- [ ] Sample size, duration and primary metric fixed before launch; SRM checked.
- [ ] Results logged with confidence intervals and a next step.
