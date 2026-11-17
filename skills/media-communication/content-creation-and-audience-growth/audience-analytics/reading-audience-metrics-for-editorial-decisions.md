---
id: media-communication.content-creation-and-audience-growth.audience-analytics.reading-audience-metrics-for-editorial-decisions
name: reading-audience-metrics-for-editorial-decisions
category: media-communication
field: content-creation-and-audience-growth
product: audience-analytics
tags: [audience-analytics, analytics, google-analytics, ga4, chartbeat, parse-ly, plausible, engagement-time, engaged-sessions, scroll-depth, retention, returning-visitors, loyalty, cohort-analysis, traffic-sources, referral, utm, pageviews, vanity-metrics, newsroom-analytics, editorial-metrics, dashboards, regression-to-the-mean]
level: practitioner
status: docs-checked
description: "Read audience data for editorial calls: GA4 engaged sessions, engagement and bounce rate, segmenting by channel, and what a number justifies."
sources: ["https://support.google.com/analytics/answer/12195621"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reading audience metrics for editorial decisions

**Goal:** use analytics (GA4 and similar tools) to make better editorial calls, such as
what to commission more of, what to stop and when to publish, while knowing which numbers
are noise or misleading.

## 1. GA4 engagement metrics
Both metrics are defined in terms of engaged sessions. A session is a period during which
a user is engaged with your website or app. An **engaged session** meets any of:
- lasts longer than 10 seconds;
- has a key event;
- has 2 or more screen or page views.

**Engagement rate** is the percentage of engaged sessions. **Bounce rate** is the
opposite: the percentage of sessions that were not engaged. A reader who reads for under
10 seconds, triggers no event and views one page is not engaged (if that were the only
session, engagement rate 0% and bounce rate 100%). Events such as first_visit,
first_open and session_start are excluded from the calculation of engaged sessions even
if marked as a key event.

Most GA4 reports do not show these two metrics by default. An Editor or Administrator
can add them to a detail report with Customize report, then Metrics, then Add metric.

## 2. Segment before you conclude
If engagement rate is low, GA4's guidance is to dig into reports and explorations to see
whether it is uniformly low or the result of particular channels, source/medium pairs or
pages.
- Low on a few pages: does the content match the marketing that drives readers to it, and
  does the page offer an easy path to the next step?
- Low in one channel: review the marketing for that channel (for example display ads that
  are not relevant to the site content).
- Low everywhere: check the measurement code, that all pages are tagged correctly.
Compare articles within the same traffic source before comparing articles with each other.

## 3. What the numbers justify
- One piece doing well is an anecdote; look for a pattern across several comparable
  pieces before commissioning a strand.
- Note confounders (publish time, homepage placement, newsletter inclusion, a platform
  change) before blaming the topic.
- Decide in advance which coverage is protected from traffic targets and write it down.

## 4. A weekly readout
1. Top pieces by engagement, split by source.
2. One surprise and a hypothesis about why.
3. One experiment for next week, written down with how you will judge it.

## Gotchas
- Bounce rate here is the share of sessions that were not engaged; check which definition a tool uses before comparing numbers.

## Verify
- [ ] Each tracked metric is tied to a stated editorial goal.
- [ ] Article comparisons are made within the same traffic source.
- [ ] Decisions to start or stop a strand cite a pattern across several pieces.
- [ ] Protected (non-traffic-judged) coverage is written down.

## Checked
2026-11-09. Confirmed against the Google Analytics Help page "[GA4] Engagement rate and bounce rate" (engaged session criteria, engagement and bounce rate definitions, excluded events, adding metrics to detail reports, diagnosing low engagement by channel, page and tagging). Removed unconfirmed material: the metric-by-goal table, scroll depth and retention claims, cohort and newsletter guidance, regression-to-the-mean and survivorship commentary, UTM advice, consent and Apple Mail notes, the sample-size thresholds and Chartbeat/Parse.ly comparisons.
Method: documentation only; no commands were run.
