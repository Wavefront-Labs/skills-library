---
id: business-finance.product-management.product-analytics.metric-trees-funnels-retention-and-experiment-reads
name: metric-trees-funnels-retention-and-experiment-reads
category: business-finance
field: product-management
product: product-analytics
tags: [product-management, product-analytics, north-star-metric, metric-tree, kpi-tree, funnel-analysis, conversion-funnel, retention, cohort-analysis, retention-curve, dau-mau, activation, a-b-testing, ab-test, experiment-analysis, statistical-significance, sample-ratio-mismatch, guardrail-metrics, amplitude, mixpanel, posthog, google-analytics, event-tracking]
level: practitioner
status: draft
description: "Measure a product: build a north-star metric tree, read funnels and cohort retention correctly, and interpret A/B results (power, SRM, guardrails, peeking) for product decisions."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Metric trees, funnels, retention and experiment reads

**Goal:** decide with numbers you understand, and catch the common ways product data
misleads, without needing to be a data scientist.

## 1. North-star metric and its tree
Pick one **north-star metric** that captures delivered customer value and leads
revenue (e.g. "weekly active teams that ran ≥1 report", not "signups" or "page views").
Decompose it into a **metric tree**: inputs the team can move.
```
Weekly active reporting teams
 ├─ new teams activated  = signups × activation rate
 ├─ retained teams       = last week's actives × week-on-week retention
 └─ resurrected teams
```
Each squad owns one or two input metrics. Add **guardrails** (latency, error rate,
support contacts, unsubscribes) that must not degrade.

## 2. Event tracking basics
Name events consistently (`object_action`: `report_created`, `invite_sent`), document
them in a tracking plan with properties, and QA them in staging. In tools like
Amplitude, Mixpanel or PostHog, most "the numbers look weird" incidents are broken
instrumentation, duplicate events or bot traffic. Check that before theorising.

## 3. Funnel analysis
- Define steps and a **conversion window** (e.g. within 7 days). Results change a lot
  with the window; state it.
- Look at the **biggest absolute drop** and segment it (device, channel, plan, country,
  new vs returning). Aggregates hide segment problems (Simpson's paradox).
- Funnels show *where*, not *why*: pair with session replays or interviews.

## 4. Retention and cohorts
- Plot **cohort retention curves** (by signup week/month): % of the cohort active in
  each later period. Flattening = a retained core; continuous decay toward zero = a leak.
- Use a meaningful "active" definition (did the core action), not "logged in".
- Compare cohorts before/after changes; a newer cohort's curve sitting above older ones
  is the clearest evidence an improvement worked.
- DAU/MAU ("stickiness") suits daily-use products; it misleads for naturally weekly or
  monthly products (payroll, tax).

## 5. Reading an A/B test
Before launch:
- Write hypothesis, **primary metric**, guardrails, minimum detectable effect, and
  **sample size from a power calculation** (commonly 80% power, 5% significance).
  Fix the run length up front; run whole weeks to cover weekday effects.
After:
- **Sample ratio mismatch (SRM)**: if a 50/50 test has, say, 50.8/49.2 split with large
  n, a chi-square test will flag it; an SRM means assignment or logging is broken, so the
  result is untrustworthy. Fix, don't interpret.
- **Don't peek and stop early** on a significant-looking day with fixed-horizon stats;
  it inflates false positives heavily. Use sequential methods if you need early stops
  (many platforms offer them; check which method your tool uses).
- Report the **effect size with confidence interval**, not only "p < 0.05". A
  significant +0.2% may not be worth shipping complexity.
- Check guardrails and key segments; beware testing many metrics/segments and
  reporting the one that "won" (multiple comparisons).
- **Novelty effects**: engagement lifts that fade in week 2-3. Look at the trend over the run.
- Inconclusive is a valid result: it bounds the effect.

## 6. Turning analysis into a decision
One slide: question, metric, result with interval, segments, guardrails, decision and
what you'll watch next. Pre-agree the ship rule (e.g. "ship if primary ≥ +1% and no
guardrail worse than −0.5%") to avoid motivated reasoning.

## Gotchas
- Vanity metrics (cumulative signups) always go up.
- Correlation in observational data ("users who use feature X retain better") is usually
  selection: engaged users try more features. Test causally before investing.
- Changing a metric definition mid-quarter breaks every trend line; version definitions.

## Verify
- [ ] North-star and input metrics written down with exact definitions.
- [ ] Funnel analysis states its conversion window and checks segments.
- [ ] Retention measured on the core action, by cohort.
- [ ] Every experiment has a pre-registered sample size, primary metric and ship rule.
- [ ] SRM checked before reading results.
