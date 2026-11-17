---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.cost-vs-resilience-tradeoffs
name: cost-vs-resilience-tradeoffs
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, resilience, reliability, cost, tradeoffs, availability-math, nines, serial-availability, parallel-redundancy, expected-loss, cost-of-downtime, rto, rpo, tiering, criticality-tiers, well-architected, redundancy, n-plus-one, over-provisioning, business-impact-analysis, finops, architecture-decision-record, adr]
level: advanced
status: draft
description: "Decide how much resilience to buy: availability math for serial and redundant components, cost of downtime vs cost of redundancy, criticality tiers, and recording the trade-off in an ADR."
sources: ["AWS Well-Architected Reliability and Cost Optimization Pillars", "Google SRE Book - Embracing Risk", "Azure Well-Architected Framework - Reliability tradeoffs"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cost vs resilience trade-offs — buy the nines the business will pay for

**Goal:** every workload gets a resilience level justified by numbers — expected cost of
downtime against the cost of the redundancy that prevents it — and the decision is written down.

## 1. Do the availability math first
- **Serial dependencies multiply:** a request through LB (99.99%) → app (99.95%) → DB (99.95%)
  → payment API (99.9%) is at best 0.9999 × 0.9995 × 0.9995 × 0.999 ≈ **99.79%**. You cannot
  promise more than your weakest serial chain without removing or hedging dependencies.
- **Parallel redundancy:** two independent copies at 99.5% give 1 − 0.005² = 99.9975% —
  *only if failures are independent*. Same region, same deploy pipeline, same config push
  = correlated failures; real gain is far smaller. Treat independence as an assumption to defend.
- Each extra nine is roughly 10x less downtime and typically several times the cost
  (more regions, more on-call rigour, slower change). Budget: 99.9% ≈ 43 min/month; 99.99% ≈ 4.3 min.

## 2. Price the downtime
Expected annual loss ≈ P(outage per year) × mean duration × cost per hour.
Cost per hour includes: lost revenue (net of what users retry later), SLA credits,
support load, staff overtime, regulatory exposure, reputational churn (estimate, and say so).
Example: an API earning $20k/h with ~85% of revenue recovered on retry loses ~$3k/h.
A warm-standby region costing $25k/year to cut expected regional-outage downtime
from 8 h/year to 0.5 h/year saves ~$22k/year — roughly break-even, so the decision turns
on the non-revenue factors. Make that explicit instead of defaulting to "more is safer".

## 3. Tier workloads
| Tier | Example | Target | Pattern |
|---|---|---|---|
| 0 — critical | checkout, auth | 99.95-99.99%, RTO min, RPO ~0 | multi-AZ + warm standby/active-active |
| 1 — important | search, notifications | 99.9%, RTO < 1 h | multi-AZ, pilot light |
| 2 — internal | reporting, admin | 99.5%, RTO < 24 h | single AZ OK, backups |
| 3 — batch/dev | CI, sandboxes | best effort | spot, rebuild from code |

Most estates over-engineer tier 2-3 (multi-AZ dev databases) and under-engineer the
dependencies of tier 0 (one NAT gateway, one IdP).

## 4. Cheap resilience before expensive resilience
Ordered roughly by value per dollar:
1. Timeouts, retries with jittered backoff, circuit breakers, idempotency keys.
2. Safe deploys: canary, automated rollback, feature flags — deploys cause most incidents.
3. Multi-AZ for stateful tiers (managed DB Multi-AZ ≈ 2x DB cost, but the DB is usually the SPOF).
4. Graceful degradation: serve cached or partial results when a dependency fails.
5. Backups that are *tested*.
6. Only then: second region.

## 5. Record it
Write an ADR per tier-0/1 workload: target, chosen pattern, monthly cost delta, expected-loss
estimate, accepted risks, review date. Product owners sign the accepted risk — not just engineering.

## Gotchas
- Redundant components that share a control plane, a credential, or a config file fail together.
- Paying for active-active but deploying to both regions at once removes most of the benefit; stagger deploys.
- Over-provisioned standby capacity is also a cost lever: commitments can cover it, spot cannot.
- "Five nines" quoted from a provider SLA is a credit promise, not an engineering prediction.
- Expected-loss numbers for rare events are guesses; use ranges and test sensitivity.

## Verify
- [ ] Every production workload has a tier with target, RTO and RPO.
- [ ] Serial availability of the critical path is computed and ≥ the promised SLO.
- [ ] Tier-0/1 have an ADR with cost delta and expected-loss estimate, signed by a product owner.
- [ ] Cheap mitigations (timeouts, retries, safe deploys) are in place before multi-region spend.
- [ ] Tier 2-3 workloads are not paying for tier-0 redundancy.

Uncertain: dollar figures are illustrative; downtime cost models vary widely by business.
Related: computing-software.cloud-infrastructure-engineering.cloud-architecture.multi-region-high-availability-design, computing-software.cloud-infrastructure-engineering.cloud-architecture.disaster-recovery-planning
