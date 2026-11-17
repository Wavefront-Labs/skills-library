---
id: computing-software.data-science-and-analytics.experiment-design.experiment-hypothesis-metrics
name: experiment-hypothesis-metrics
category: computing-software
field: data-science-and-analytics
product: experiment-design
tags: [oec-metric, guardrail-metrics, experiment-hypothesis, ab-design]
level: practitioner
status: draft
description: "Write a falsifiable hypothesis, choose one primary metric (OEC) with guardrails and define unit of randomisation before launching."
sources:
  - https://experimentguide.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Experiment definition
- Hypothesis: "Changing X for population P will move metric M by at least delta because ..."
- OEC: one primary metric sensitive and aligned with long-term value; guardrails: latency, errors, unsubscribes, revenue.
- Unit: user/device/account (not page view) so the metric's independence holds.
- Fix before launch: duration, sample size, analysis plan, decision rule.
## Gotchas
- Too many metrics without a primary one invites cherry-picking.
- Ratio metrics (per-session) need delta-method or bootstrap variance at the user level.
## Verify
- [ ] The pre-registered analysis plan exists in writing before data arrives.
