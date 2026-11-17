---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.waste-benchmark
name: waste-benchmark
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, benchmarking, waste-benchmark, idle-resources, waste-percentage, finops-kpis, optimisation-recommendations]
level: practitioner
status: docs-checked
description: "Measure waste as a share of spend: define waste classes, compute from recommendation and utilisation data, benchmark teams internally and track the trend."
sources: ["https://www.finops.org/framework/capabilities/benchmarking/", "https://www.finops.org/framework/capabilities/workload-optimization/", "https://www.finops.org/framework/capabilities/rate-optimization/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Waste percentage benchmark

"How much of our spend is waste?" needs a defined, repeatable answer. A waste percentage computed the same way every
period lets you compare teams and track progress.

## Define waste classes
Start from the Framework's usage optimisation categories and record which you include:

| Class | What it is (Framework wording) |
|---|---|
| Waste reduction | resources provisioned but no longer needed: stranded storage volumes, excessive backups or snapshots, unused sandbox resources, redundant licences, inactive SaaS entitlements |
| Rightsizing | resources that cannot be scaled but have consistently low utilisation |
| Workload management | resources running when the workload is not required, mainly pre-production |
| Modernisation | older resource generations or tiers with better price-performance alternatives |
| Unused commitment | the Framework KPI Percentage of Commitment Discount Waste: cost of unused commitment discount divided by total cost of the commitment discount, times 100 |

Apply the classes in a fixed priority order so one resource is counted once (a design choice of this skill, not a
Framework rule). Keep a waste management library documenting known waste patterns, remediation and estimated value,
as the Framework describes.

## Compute
Waste percentage = waste amount for the period divided by total cost for the same scope and period. State the cost
basis (for example amortised) and the data sources, and take utilisation from monitoring or observability data, since
cost data alone cannot show idleness.

## Benchmark
- **Internal**: compare teams and scopes on standardised KPI definitions with transparent goals and accurate data.
  The Framework says gamification or incentive programmes can strengthen internal benchmarking.
- **External**: compare with peers carefully to protect pricing, usage and other commercially sensitive information.
  Sources named by the Framework include the FinOps Foundation community, State of FinOps data, analysts, integrators and
  providers. Definitions differ, so treat external figures as context only.
- Report the trend over time, and keep benchmarking one input among several approaches.

## Gotchas
- Check longer-cycle peaks (month-end, quarter-end) before calling low utilisation waste.
- Some low utilisation is justified by business value; record such exceptions rather than counting them as waste.

## Verify
- [ ] Waste class definitions, priority order and cost basis are published.
- [ ] Each team's waste percentage is computed from the same method and data each period.

## Checked
Confirmed on the FinOps Framework Usage Optimization page (waste, workload management, rightsizing, modernisation
categories, waste management library, long-cycle utilisation caution, justified higher utilisation), the Benchmarking
page (internal and external benchmarking guidance, gamification) and the Rate Optimization page (Percentage of
Commitment Discount Waste formula). Removed: CPU and network idle thresholds, 14-day window, the industry 25-30 percent
waste figure, the CLI commands for recommendation APIs, the CommitmentDiscountStatus FOCUS column, and the wg/finops-kpis,
AWS Compute Optimizer and Azure Advisor sources (unread).
Method: docs-checked 2026-11-09 against finops.org Framework Usage Optimization, Benchmarking and Rate Optimization capability pages
