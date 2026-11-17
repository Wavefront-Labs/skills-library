---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.failure-mode-analysis
name: failure-mode-analysis
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, reliability-foundations, failure-mode-analysis, fmea, failure-mode-and-effects-analysis, single-points-of-failure, risk-priority, resilience-review]
level: advanced
status: draft
description: "Run a failure mode analysis on a cloud workload: enumerate components and their failure modes, rate impact/likelihood/detection, and turn the top risks into mitigations and tests."
sources: ["https://learn.microsoft.com/azure/well-architected/reliability/failure-mode-analysis", "https://docs.aws.amazon.com/prescriptive-guidance/latest/resilience-analysis-framework/introduction.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Failure mode analysis (FMEA)

## Steps
1. **Map the critical flows** (login, checkout) and every component they touch: DNS, CDN, LB,
   compute, DB, cache, queues, identity provider, secrets, third-party APIs, CI/CD (for recovery).
2. For each component list **failure modes**: unavailable, slow (latency), returns errors,
   returns wrong data, overloaded, misconfigured by a deploy, credentials expired, quota hit, region/AZ loss.
   The AWS Resilience Analysis Framework groups them as: shared fate, excessive load, excessive
   latency, misconfiguration and bugs, single points of failure.
3. For each mode: **effect** on the flow, **detection** (which alert fires, how fast), **current
   mitigation**, and rate severity × likelihood (1-5 each) or a risk priority number.
4. Highest scores → mitigations: redundancy, timeouts/circuit breakers, graceful degradation,
   alarms, runbooks, config validation.
5. **Turn each mitigation into a test** (chaos experiment, game day) to prove it works.
6. Revisit when architecture changes or after incidents.

## Template row
| Component | Failure mode | Effect | Detection | Mitigation | Sev | Lik | Action |
|---|---|---|---|---|---|---|---|
| Redis cache | unavailable | DB load ×5, p99 3 s | cache error alarm | timeouts + DB load shedding | 4 | 2 | chaos test quarterly |

## Verify
- [ ] FMEA table exists for each tier-0/1 workload, reviewed in the last 12 months.
- [ ] Top 5 risks have owners and tests.
