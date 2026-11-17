---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.performance-targets
name: performance-targets
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, performance-engineering, performance-targets, sli, slo, latency-slo, throughput-targets, non-functional-requirements]
level: practitioner
status: docs-checked
description: "Set measurable performance targets: numeric targets per workload flow, SLIs as good-over-total ratios, critical user journeys, where to measure, and an error budget policy."
sources: ["https://sre.google/workbook/implementing-slos/", "https://sre.google/sre-book/service-level-objectives/", "https://learn.microsoft.com/azure/well-architected/performance-efficiency/performance-targets"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Performance targets and SLIs

## Steps
1. **Make targets numeric and tied to requirements** (Azure Well-Architected PE:01), for all workload flows.
   Set them before deployment: for a design use market research, competitive analysis and surveys; for a
   production workload with none, use production data and customer feedback.
2. **Cover the metric families** the Azure page lists: availability (error rate), capacity (throughput and
   concurrency) and response time (latency, load time). Its example targets are a share of sign-in requests
   completing within a time, written as a number plus a threshold.
3. **Start from critical user journeys** (SRE Workbook): a sequence of tasks that is a core part of the
   user's experience, such as steps of an online shopping purchase. Measure user-centric events by joining
   log events, client-side instrumentation or similar; each becomes just another SLI.
4. **Write SLIs as a ratio** of good events to total events (Workbook). Pick a small number (five or fewer)
   of SLI types that represent the most critical functionality. Availability and latency SLOs are the most
   common; freshness, durability, correctness, quality and coverage also apply.
5. **Choose where to measure.** The Workbook's example uses load balancer monitoring, closer to the user's
   experience than application server logs; measuring at the load balancer or the client is a way to
   improve an SLI.
6. **Use percentiles for latency.** The SRE Book aggregates SLI data into a rate, average or percentile and
   shows 50th, 85th, 95th and 99th percentile latencies; the Workbook's example reports 90th and 99th
   percentile figures over four weeks.
7. **Define an error budget policy** approved by the product manager, development team and SREs. Common
   actions when the budget is exhausted: stop feature launches until back within SLO, or devote engineering
   time to reliability bugs. Document the SLO and policy, and keep dashboards of SLO compliance.
8. **Iterate**: review SLOs and improve the SLI if changes cause false positives or negatives.

## Gotchas
- Targets copied from today's system bake in today's problems; anchor on user need.
- Too many SLI types dilute attention; the Workbook recommends five or fewer.

## Verify
- [ ] Each critical journey has an SLI definition, a numeric target and a measurement point.
- [ ] An error budget policy exists and key stakeholders have agreed to enforce it.

## Checked
2026-11-01. Confirmed against the SRE Workbook "Implementing SLOs", the SRE Book "Service Level
Objectives" chapter and the Azure Well-Architected "Define performance targets" page. Removed: the 400 ms,
200 ms and 800 ms example thresholds, the 28-day window, RUM metric names (LCP, INP), the growth horizon, the
15-minute freshness example, per-hop budgets, CI gates and burn-rate alerting, the quarterly review and the
"1-3 SLOs per journey" rule, none of which those pages state in that form. Dropped the AWS Well-Architected
welcome page, which has no relevant content.
Method: documentation only; no commands were run.
