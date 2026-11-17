---
id: computing-software.data-engineering.data-warehouse-architecture.tco-and-build-vs-buy
name: tco-and-build-vs-buy
category: computing-software
field: data-engineering
product: data-warehouse-architecture
tags: [data-warehouse-architecture, platform-selection, tco, build-vs-buy, total-cost-of-ownership, finops, cost-modelling, vendor-evaluation, architecture-decision]
level: advanced
status: draft
description: "Estimate total cost of ownership for data platform options and decide build vs buy: cost components, people cost, 3-year model, sensitivity analysis, hidden costs and exit costs."
sources:
  - https://www.finops.org/framework/
  - https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/welcome.html
  - https://cloud.google.com/architecture/framework/cost-optimization
  - https://www.gartner.com/en/information-technology/glossary/total-cost-of-ownership-tco
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# TCO and build vs buy

**Goal:** compare platform or tool options on their full cost over the period you'll live with them, including people and exit, and make a defensible build-vs-buy call.

## 1. Cost components (3-year horizon)
| Category | Items |
|---|---|
| Platform usage | compute (credits/DBUs/slots/nodes), storage, data transfer/egress, serverless premiums |
| Licences/subscriptions | SaaS tools (EL, orchestration, catalog, observability), support plans, editions needed for features (e.g. security tiers) |
| People | build effort (FTE-months × loaded cost), ongoing operation/maintenance FTE, on-call, training/hiring |
| Infrastructure around it | networking (private links, NAT), monitoring, CI/CD, secrets, environments (dev/test copies) |
| Migration | dual running period, translation, testing, consultants |
| Risk/exit | lock-in cost to leave later (data export, rewrite), outage impact |
People cost usually dominates small/mid platforms — a "free" open-source tool needing 1.5 FTE to run is not free.

## 2. Build the model
- Workload drivers: data volume growth, query volume/concurrency, number of pipelines, users.
- Convert drivers to units per option (TB scanned, credit-hours, DBU-hours, node-hours) using **measured PoC numbers**, not vendor calculators alone.
- Apply negotiated discounts / commitments explicitly as assumptions.
- Monthly model for 36 months with growth; include ramp-up and dual-run.
- Sensitivity: vary growth (±50%), query efficiency, discount, FTE estimates; show which assumption flips the decision.

## 3. Build vs buy criteria
| Favour **buy** | Favour **build** |
|---|---|
| commodity capability (connectors to popular SaaS, BI, catalog) | core differentiator for the business |
| small team, need speed | strong team with spare capacity, long horizon |
| vendor roadmap matches needs | requirements unusual / vendors don't fit |
| compliance certifications needed quickly | strict data residency/sovereignty that vendors can't meet |
Middle ground: buy managed open-source (managed Airflow/Kafka/Flink) — open interfaces lower exit cost while removing ops toil.

## 4. Hidden costs to surface
- Egress and cross-region transfer; idle provisioned capacity; dev/test environments; observability ingestion fees.
- Per-seat licences that scale with org growth.
- Upgrade treadmill for self-hosted (major version migrations).
- Vendor price changes — model a renewal increase.

## 5. Present the decision
One page: options, 3-year TCO with ranges, non-cost scores (capability fit, risk, time to value, team skills), recommendation, key assumptions and the triggers for revisiting (e.g. "revisit if monthly spend exceeds X or volume doubles").

## Verify
- [ ] People cost and exit cost are included for every option.
- [ ] Usage estimates come from a PoC on representative workload.
- [ ] Sensitivity analysis shows which assumptions change the ranking.
