---
id: computing-software.qa-testing-engineering.performance-testing.performance-requirements-and-slos
name: performance-requirements-and-slos
category: computing-software
field: qa-testing-engineering
product: performance-testing
tags: [performance-requirements, slo, non-functional-requirements, sla, percentile-targets]
level: practitioner
status: draft
description: "Write measurable performance requirements: percentile latency targets at stated load, throughput, error budgets, resource limits, and conditions that make them testable."
sources:
  - https://sre.google/sre-book/service-level-objectives/
  - https://www.iso.org/standard/35733.html
  - https://www.istqb.org/certifications/performance-tester
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Writing measurable performance requirements and SLOs

**Goal:** requirements a test can pass or fail. "The system shall be fast" is untestable; "p95 < 500 ms" alone is incomplete.

## Template
```
For <operation/transaction>,
under <load: X requests/s or N concurrent users with the reference workload mix>,
with <data volume and environment>,
<percentile> response time shall be <= <value> measured at <where: server/edge/client>,
error rate shall be < <value>,
over a <duration> steady-state window.
```
Example: "Checkout API: at 25 checkouts/s within the peak-hour mix (450 req/s total), with 50M orders in the DB, p95 server response <= 800 ms and p99 <= 2 s, error rate < 0.1%, sustained for 30 minutes."

## Ingredients
- **Latency** as percentiles (p50, p95, p99), never averages alone.
- **Throughput** target and the workload mix it refers to.
- **Errors**: rate and which status codes count.
- **Resource budgets**: CPU < 70% at peak, memory stable over 8 h soak.
- **Scalability**: handles 2x peak with horizontal scaling within N minutes.
- **Client-side**: Core Web Vitals (LCP <= 2.5 s, INP <= 200 ms, CLS <= 0.1 at p75).

## SLO view (production)
SLI = good events / valid events (e.g. requests under 800 ms and non-5xx). SLO = 99.5% over 28 days. Error budget = 0.5%. Load test thresholds should be tighter than the SLO to leave headroom.

## Turning into test thresholds
```js
thresholds: {
  'http_req_duration{name:POST /checkout}': ['p(95)<800', 'p(99)<2000'],
  'http_req_failed{name:POST /checkout}': ['rate<0.001'],
}
```

## Gotchas
- Requirements without load conditions cannot be verified; every target needs its load and data context.
- Copying industry numbers without user research or business input; derive from user expectations and current baselines.
- Measuring at the wrong point (client vs server) gives different numbers; state it.

## Verify
Each requirement names operation, load, data, percentile, target, error rate and window, and maps one-to-one to a test threshold.
