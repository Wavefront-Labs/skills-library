---
id: creative-arts.design-for-form-and-experience.ux-design.choosing-metrics-with-the-heart-framework
name: choosing-metrics-with-the-heart-framework
category: creative-arts
field: design-for-form-and-experience
product: ux-design
tags: [heart-framework, goals-signals-metrics, ux-metrics, product-analytics, ux-measurement]
level: practitioner
status: draft
description: "Pick UX metrics with Google's HEART framework: set goals per dimension, define signals, then choose a small set of trackable metrics tied to product goals."
sources:
  - "Rodden, Hutchinson and Fu, Measuring the User Experience on a Large Scale: User-Centered Metrics for Web Applications, CHI 2010 (Google)"
  - "Nielsen Norman Group - UX metrics articles (nngroup.com/topic/metrics)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# HEART framework and goals-signals-metrics

**Goal:** choose a few metrics that show whether the experience is improving, instead of tracking everything that is easy to count.

## The five dimensions
- **Happiness:** attitude, satisfaction, perceived ease (surveys, NPS, SUS).
- **Engagement:** depth of involvement (sessions per user per week, actions per session).
- **Adoption:** new users of a product or feature (accounts created, first use of feature X within 7 days).
- **Retention:** users who stay (30-day return rate, churn).
- **Task success:** efficiency, effectiveness, errors (completion rate, time on task, error rate).

## Goals-Signals-Metrics process (per project)
1. **Goal:** what the product or feature is meant to achieve for users and the business ("people find a relevant recipe quickly").
2. **Signal:** the behaviour or attitude that would show the goal is met ("they click a result and stay on it", "they rarely reformulate the query").
3. **Metric:** a number built from the signal, defined precisely enough to implement ("share of searches ending in a result click within 30 s; excludes bots").
4. Not every dimension applies to every project. Choose 2-3 that match the goal and drop the rest on purpose.

## Worked row
Feature: saved searches. Adoption: share of weekly active users creating a saved search in their first 14 days. Retention: users with a saved search returning in week 4 against users without. Task success: time from query to saved.

## Gotchas
- Vanity metrics (page views) fail the signal test. Each metric must move if the experience improves.
- Pair behavioural metrics with attitudinal ones; one explains the other.
- Capture the baseline before shipping the change.

## Verify
- [ ] Each chosen metric traces to a goal through a signal.
- [ ] Definitions are implementable (events, filters, time window).
- [ ] Baseline captured; target or direction stated.
