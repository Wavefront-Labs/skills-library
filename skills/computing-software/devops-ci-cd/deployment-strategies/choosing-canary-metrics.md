---
id: computing-software.devops-ci-cd.deployment-strategies.choosing-canary-metrics
name: choosing-canary-metrics
category: computing-software
field: devops-ci-cd
product: deployment-strategies
tags: [deployment-strategies, canary-metrics, canary-analysis, golden-signals]
level: advanced
status: draft
description: "Choose canary analysis metrics that actually detect bad releases: golden signals per version, business KPIs, minimum traffic, comparison to baseline and sensible thresholds."
sources: ["https://sre.google/workbook/canarying-releases/", "https://argo-rollouts.readthedocs.io/en/stable/features/analysis/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Choosing canary metrics

A canary is only as good as the metrics judging it.

## Must-haves (per version label)
- **Error rate**: 5xx (and relevant 4xx like 429/499) ratio for canary pods only.
  ```promql
  sum(rate(http_requests_total{app="api",version="canary",code=~"5.."}[2m]))
  / sum(rate(http_requests_total{app="api",version="canary"}[2m]))
  ```
- **Latency**: p95/p99 from histograms, canary vs stable.
- **Saturation**: CPU throttling, memory growth (leaks show over time), restarts/OOMKills.
- **Business signal** where possible: checkout success, login success, events processed.

Metrics need a `version`/`rollouts-pod-template-hash` label; without per-version metrics you are
measuring the blend.

## Comparison, not absolutes
Compare canary to **baseline** (a fresh deployment of the current version receiving the same
traffic share) rather than to the long-running stable fleet, which differs in warm caches and age.

## Traffic sufficiency
At 5% traffic and low RPS, one error is 10% error rate. Require minimum request counts
(`count > 500` before judging) or longer intervals; consider `inconclusive` results that pause for humans.

## Thresholds
- Error rate: absolute ceiling (e.g. < 1%) and relative (no more than baseline + 0.5 pp).
- Latency: p95 no more than 10-20% above baseline.
- Use `failureLimit`/consecutive failures to avoid single-scrape blips.

## Verify
- [ ] Replaying a known bad release in staging fails analysis; a no-op release passes repeatedly.
