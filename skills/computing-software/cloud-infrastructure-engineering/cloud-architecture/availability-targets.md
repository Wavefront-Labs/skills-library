---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.availability-targets
name: availability-targets
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, reliability-foundations, availability-targets, slo, sli, error-budget, nines, downtime-budget, dependency-availability, criticality-tiers]
level: practitioner
status: docs-checked
description: "Set availability targets per workload that the architecture can actually meet: tie to business impact, convert nines to downtime, check dependency ceilings, and express as SLOs."
sources: ["https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/availability.html", "https://sre.google/workbook/implementing-slos/", "https://learn.microsoft.com/azure/well-architected/reliability/metrics"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Setting availability targets

## Steps
1. **Start from impact**: what does an hour down cost (revenue, safety, regulatory, reputation)?
   Group workloads into tiers. AWS's example mapping: 99% for batch and ETL jobs, 99.9% for
   internal tools, 99.95% for online commerce, 99.99% for video delivery, 99.999% for ATM and telecom.
   Higher targets cost more, so identify the true need first.
2. **Convert to budgets** (AWS Well-Architected lists 3 d 15 h, 8 h 45 min, 4 h 22 min and 52 min per year for 99% to 99.99%):
   | Target | Downtime/30 days | /year |
   |---|---|---|
   | 99% | 7.2 h | 3.65 d |
   | 99.9% | 43 min | 8.8 h |
   | 99.95% | 22 min | 4.4 h |
   | 99.99% | 4.3 min | 53 min |
3. **Check the ceiling**: with hard dependencies the availability is the product of the
   availabilities, so 3 components at 99.95% give about 99.85% before your own failures (AWS's
   example: 99.99% x 99.99% x 99.99% = 99.97%). Independent redundant components (for example
   in different Availability Zones) raise it: two at 99.9% give 99.9999%. Estimate an unpublished
   dependency from MTBF and MTTR.
4. **Match architecture**: high targets need automated recovery from all failures and testing
   of capacity changes, deployments and data migrations to the same goal.
5. **Express as SLOs** on SLIs such as the proportion of successful requests and the proportion
   faster than a threshold. Load-balancer metrics or client-side instrumentation are closer to
   the user experience than application-server logs. The error budget is only useful with an
   error budget policy that says what happens when it runs out.
6. Include planned maintenance in the budget; AWS advises against excluding it.

## Gotchas
- Asking for 100%: Google's SRE workbook notes each extra nine costs more while customer benefit approaches zero.
- Measuring availability from inside the system (health checks) instead of from user requests.

## Verify
- [ ] Each workload has a tier, SLO and documented dependency ceiling.
- [ ] Alerting warns of threats to the error budget before they become deficits.

## Checked
2026-11-08. Confirmed: AWS Well-Architected availability page (yearly downtime table, hard-dependency product, redundant components, MTBF/MTTR, planned maintenance advice, cost of availability) and the SRE workbook (SLI as proportion of successful requests, load balancer vs client-side SLIs, error budget policy, 100% not reasonable, alerting before deficits). The downtime table arithmetic was recomputed. Azure reliability metrics page: stakeholders weigh downtime revenue loss against the cost of reliability (supports step 1). Removed: tier percentages, "99.9% achievable multi-AZ", multi-region for tier 0, burn-alert tiers.
Method: documentation only; no commands were run.

Related: computing-software.cloud-infrastructure-engineering.cloud-architecture.cost-vs-resilience-tradeoffs
