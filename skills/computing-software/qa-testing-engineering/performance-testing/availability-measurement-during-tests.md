---
id: computing-software.qa-testing-engineering.performance-testing.availability-measurement-during-tests
name: availability-measurement-during-tests
category: computing-software
field: qa-testing-engineering
product: performance-testing
tags: [availability-testing, uptime, synthetic-monitoring, slo, reliability-testing]
level: practitioner
status: draft
description: "Measure availability during load, failover and soak tests: probe-based success ratio, error budget maths, downtime windows and reporting against the SLO."
sources:
  - https://www.istqb.org/certifications/certified-tester-advanced-level-technical-test-analyst-ctal-tta
  - https://sre.google/sre-book/embracing-risk/
  - https://sre.google/workbook/implementing-slos/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Availability measurement during tests

**Goal:** turn "it stayed up" into a number: the proportion of good requests or time during the test, compared with the SLO.

## Two definitions
- **Request-based:** good requests / total requests (SRE book). Use load-test results directly: non-5xx and under the latency threshold count as good.
- **Time-based:** minutes the service was up / total minutes, from a probe every N seconds. Simpler, coarser.

## Set up measurement
- Run an independent **probe** alongside the test (k6 or curl loop, Blackbox Exporter, synthetic monitor) hitting a health-relevant endpoint every 1-5 s from outside the cluster, logging timestamp, status and latency.
- Health endpoint must exercise real dependencies (DB read), not only return 200 from the web tier.
- Keep the load generator's own errors separate from server errors.

## Compute

```python
good = sum(1 for r in probes if r.status < 500 and r.ms < 1000)
availability = good / len(probes)
downtime_s = (len(probes) - good) * probe_interval_s
```

Allowed downtime: 99.9% = 43.2 min per 30 days; 99.95% = 21.6 min; 99.99% = 4.3 min. A failover test that takes 90 s consumes a significant share of a 99.99% monthly budget.

## During specific tests
- **Failover:** measure the outage window (first failed probe to first good probe) and errors seen by load traffic.
- **Rolling deploys:** availability should stay at 100% if drain and readiness probes work.
- **Soak:** look for degradation late in the run (leaks, pool exhaustion) that dents availability.

## Verify
The test report states availability with its definition, the longest outage window, and whether the run would have stayed within the SLO's error budget.
