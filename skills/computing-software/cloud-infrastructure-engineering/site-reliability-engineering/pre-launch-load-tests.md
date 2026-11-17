---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.pre-launch-load-tests
name: pre-launch-load-tests
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [launch-load-tests, pre-launch-stress, load-testing, launch-planning, traffic-modelling, k6]
level: practitioner
status: docs-checked
description: "Load test a launch: model launch-day traffic (peak, spike, mix), test end to end including dependencies, verify overload behaviour, and turn results into go/no-go criteria."
sources: ["https://sre.google/sre-book/reliable-product-launches/", "https://sre.google/sre-book/launch-checklist/", "https://grafana.com/docs/k6/latest/testing-guides/test-types/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pre-launch load tests

The SRE Book launch coordination checklist lists, under volume estimates, capacity and performance:
traffic estimates, the launch "spike", traffic mix, a load test and end-to-end test, and capacity per
datacenter at max latency. A launch load test differs from routine capacity benchmarking: it models a
specific event.

## 1. Model launch traffic
- Expected users at peak x requests per user per minute x mix of endpoints.
- Spike factor: estimate the launch "spike" explicitly (announcements and push notifications can cause one).
- Add organic load already present on shared dependencies.
```
peak_qps = 200k users_at_peak * 6 req/min / 60 = 20k QPS; spike x3 = 60k QPS for 10 min
mix: 70% GET /feed, 20% GET /item, 8% POST /like, 2% POST /upload
```

## 2. Test types
| Test | Shape | Purpose |
|---|---|---|
| Peak | hold modelled peak | SLOs met at peak with headroom |
| Spike | sharp jump above peak | autoscaling, cold caches, connection storms |
| Soak | sustained load for hours | leaks, log/disk growth, connection churn |
| Overload | beyond the spike | graceful degradation / shedding works (see `stress-tests-and-breaking-points`) |

## 3. Scope
- End to end through the real edge (CDN, WAF, LB), so their limits are tested too.
- Include dependencies, with their owners' agreement and a heads-up (you are load-testing them as well).
- Production-like data size; synthetic users flagged to exclude from analytics.

## 4. Go/no-go criteria
```
Peak: SLO latency and error targets met, with CPU and DB connection headroom you define
Spike: SLO recovered within a stated time; no crash loops
Overload: excess rejected (for example 503); recovers when load drops
```
Fail any -> fix or reduce launch scope (invite-only, region-limited).

## Gotchas
- Load generators in one region test only that path; generate from where users are.
- Tests against production during business hours need approval and abort criteria.
- Caches warmed by the test give optimistic results; include a cold-cache spike.

## Verify
- [ ] Traffic model written with sources for each number.
- [ ] Results for all four test types attached to the launch review.

## Checked
2026-11-01. Confirmed in the SRE Book Launch Coordination Checklist (launch spike, traffic mix, load test, end-to-end test, capacity at max latency, impact on other services, graceful degradation) and Reliable Product Launches at Scale. The worked QPS example is arithmetic on invented inputs. Removed the invented checklist quote, the 5-10x spike claim, test durations and ratios, and the numeric go/no-go thresholds. The k6 test-types page was fetched but only used for the test-type names (average, stress, soak, spike).
Method: documentation only; no commands were run.
