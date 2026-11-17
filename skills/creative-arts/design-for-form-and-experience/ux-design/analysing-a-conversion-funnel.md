---
id: creative-arts.design-for-form-and-experience.ux-design.analysing-a-conversion-funnel
name: analysing-a-conversion-funnel
category: creative-arts
field: design-for-form-and-experience
product: ux-design
tags: [funnel-analysis, conversion-funnel, drop-off, product-analytics, analytics, ux-research]
level: practitioner
status: draft
description: "Analyse a conversion funnel: define ordered steps and the entry cohort, measure step conversion and drop-off, segment it, and turn the worst step into a research question."
sources:
  - "Nielsen Norman Group - Analytics and User Experience (nngroup.com/articles/analytics-and-user-experience)"
  - "Amplitude Academy - Funnel Analysis (amplitude.com/blog/funnel-analysis)"
  - "Google Analytics 4 Help - Funnel exploration (support.google.com/analytics)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Funnel analysis

**Goal:** find where users fail to progress and why, then choose the next piece of work.

## Build it
1. **Define steps** as events users can complete in order (view product, add to cart, start checkout, enter payment, confirm). Four to eight steps; each must be a real tracked event (`creative-arts.design-for-form-and-experience.ux-design.writing-an-event-tracking-plan`).
2. **Define the cohort and window:** users who entered at step 1 in a date range; the window in which they must finish (same session, 1 day, 7 days). State whether steps must occur strictly in order.
3. **Compute** step conversion (step n / step n-1) and overall conversion. The biggest relative drop is where to look first, but weigh by volume.

## Segment before concluding
Device and browser, new vs returning, traffic source, country, plan. A mobile-only collapse at payment is a different problem from an across-the-board drop. Compare against a previous period to see if it is new.

## From number to cause
Pair the quantitative drop with: session recordings and heatmaps for that step, error and validation event logs, a usability test of the step, support tickets. Write the hypothesis ("coupon field distracts") and test it (`creative-arts.design-for-form-and-experience.ux-design.designing-an-ab-test`).

## Gotchas
- Instrumentation gaps look like drop-off; verify events fire on every platform.
- Users who return later via another device are counted as lost in short windows.
- Optional steps do not belong in the funnel.

## Verify
- [ ] Steps, order rule, cohort and window are defined.
- [ ] Drop-offs are segmented and compared with a baseline.
- [ ] The biggest drop has a hypothesis and a planned follow-up.
