---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.migration-cost-tracking
name: migration-cost-tracking
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, workload-onboarding, migration-cost-tracking, double-running, migration-business-case]
level: practitioner
status: draft
description: "Track migration costs and double running: tagging migration spend, ramp curves vs plan, on-prem decommission savings, credits and business case variance."
sources: ["https://www.finops.org/framework/capabilities/onboarding-workloads/", "https://aws.amazon.com/migration-acceleration-program/", "https://learn.microsoft.com/azure/cloud-adoption-framework/strategy/cloud-migration-business-case"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Migration cost tracking and double running

## Steps
1. **Tag migration spend**: `migration-wave`, `migration-phase=(build|parallel-run|steady)`
   on target resources; separate accounts for migration tooling (DMS, replication servers,
   transfer appliances).
2. **Ramp curve**: plan cloud spend per workload by month (build, parallel run, cutover,
   steady state after rightsizing); compare actuals monthly.
3. **Double running**: track the overlap where both on-prem and cloud costs exist; on-prem
   costs stop only when hardware is decommissioned, contracts cancelled and licences
   reclaimed. Report expected vs actual overlap months per wave.
4. **On-prem savings ledger**: decommissioned servers, racks, power, support contracts,
   licences, datacentre exit milestones, with finance-confirmed amounts.
5. **Credits and funding**: provider migration programmes (AWS MAP credits, Azure Migrate and
   Modernize, Google RaMP) - track credits applied by account and their expiry; they can mask
   real run cost.
6. **Business case variance**: compare actual one-off and run costs with the business case
   each quarter; explain drivers (delays extend double running; skipped rightsizing raises run cost).
7. **Post-migration optimisation** wave: rightsizing and commitments typically 1-3 months
   after cutover, once usage stabilises.

## Gotchas
- Credits hide the true run rate; report costs before and after credits.
- Delayed decommissioning is the biggest source of business case overrun.

## Verify
- [ ] Migration dashboard with ramp vs plan and double running per wave.
- [ ] Decommission savings confirmed by finance.
