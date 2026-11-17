---
id: computing-software.qa-testing-engineering.performance-testing.workload-model-from-production-logs
name: workload-model-from-production-logs
category: computing-software
field: qa-testing-engineering
product: performance-testing
tags: [workload-from-logs, workload-modelling, access-logs, traffic-mix, performance-testing]
level: practitioner
status: draft
description: "Derive a load test workload from production access logs and analytics: peak-hour selection, transaction mix, arrival rates, session lengths and data distributions."
sources:
  - https://www.istqb.org/certifications/performance-tester
  - https://grafana.com/docs/loki/latest/query/metric_queries/
  - https://docs.aws.amazon.com/athena/latest/ug/querying-alb-logs.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Deriving workload mix from production logs/analytics

**Goal:** a workload model based on evidence: which operations, how often, at what peak, with what data.

## 1. Pick the period
Peak hour of the peak day of the busiest season (plus events: sales, month end). Note the ratio of peak hour to average.

## 2. Extract operation counts
```sql
-- Athena over ALB logs: requests per normalised endpoint in the peak hour
SELECT regexp_replace(request_url, '/[0-9]+', '/:id') AS endpoint, request_verb, count(*) AS n
FROM alb_logs
WHERE time BETWEEN '2026-03-27T18:00:00' AND '2026-03-27T19:00:00'
GROUP BY 1, 2 ORDER BY n DESC LIMIT 50;
```
Loki: `sum by (route) (count_over_time({app="web"} | json [1h]))`. Also APM transaction lists (Datadog, New Relic) and product analytics funnels (sessions, conversion rates).

## 3. Build the mix
| Transaction | Peak/hour | Share | Per second |
|---|---|---|---|
| Browse product list | 540,000 | 60% | 150 |
| View product | 270,000 | 30% | 75 |
| Add to basket | 54,000 | 6% | 15 |
| Checkout | 9,000 | 1% | 2.5 |
| Search | 27,000 | 3% | 7.5 |
Cover ~90-95% of traffic plus low-volume but expensive/critical operations (exports, checkout).

## 4. Sessions and users
From analytics: session length, pages per session, think time distribution, concurrent sessions (Little's law: concurrency = arrival rate x session duration).

## 5. Data distributions
Which products are hot (Zipf-like), search terms, basket sizes, share of logged-in users, device/API clients. Feed test data files with the same skew.

## 6. Scale the model
Target = peak x growth x safety margin; document every assumption with its source.

## Gotchas
- Bot and health-check traffic inflates counts; filter user agents and internal IPs.
- CDN-served requests never reach origin; decide whether the test targets origin or edge.
- Averages over a day hide peaks; use per-minute maxima for burst sizing.

## Verify
The test's achieved per-transaction rates match the model table within ~10%, and the model document cites its log queries and date range.
