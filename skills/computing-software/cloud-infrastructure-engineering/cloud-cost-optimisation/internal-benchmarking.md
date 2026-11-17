---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.internal-benchmarking
name: internal-benchmarking
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, cost-benchmarking, internal-benchmarking, team-comparison, unit-cost, unit-cost-benchmark]
level: practitioner
status: docs-checked
description: "Run internal FinOps benchmarking across teams and scopes: define KPIs, standardise data, give self-service views and use incentives, per the Framework."
sources: ["https://www.finops.org/framework/capabilities/benchmarking/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Internal team benchmarking

The Framework describes internal benchmarking as comparing KPIs between teams, products and
FinOps Scopes to support decisions about technology value and optimisation.

## What makes it work
The Framework lists four conditions: clear definition of the benchmarked KPIs, transparent
communication of goals and objectives, accurate data collection and reporting, and supportive
leadership. Gamification or incentive programmes can add to it by rewarding desired behaviour
across personas.

## Steps
1. **Define and document KPIs** that reflect organisational priorities across cost, performance,
   efficiency and sustainability, and are meaningful to every persona involved.
2. **Standardise for comparison.** At Crawl, teams are compared informally with little
   standardisation. By Walk, KPIs are standardised enough for meaningful comparison of internal
   teams across scopes and technology categories.
3. **Make it self-service.** Teams should see their own KPI and benchmarking data and monitor their
   performance relative to peers without asking the FinOps team; at Run the reporting is automated.
4. **Engineering supplies telemetry.** Systems and services should emit accurate benchmarking
   data (utilisation, performance, efficiency, sustainability) in a form that allows consistent
   comparison.
5. **Close the loop.** Use gaps to produce prioritised recommendations, set improvement targets
   with Leadership and Finance, and track accountability so results do not stay observational.
6. **Govern.** Review and update KPIs iteratively to keep them aligned with business priorities.
7. **Recognise progress.** Leadership recognises and rewards teams that show measurable progress
   against KPI targets.

## Caution
Benchmarking should be one component of assessing technology value, not the only mechanism, and
comparisons across dissimilar products can create more confusion than insight (a point made on the
Unit Economics page).

## Verify
- [ ] Every benchmarked KPI has a documented definition and data source.
- [ ] Teams can see their own results without a request to the FinOps team.

## Checked
Method: docs-checked 2026-11-09 against the FinOps Framework KPIs and Benchmarking capability page (definition, maturity, activities and success measures read); the Unit Economics page was used for the caution only.
Removed as unconfirmed: the suggested metric list (rightsizing backlog, non-prod share, idle percent), amortised cost normalisation rules, the monthly publishing and yearly review cadence, the warnings about absolute spend rankings and gaming, and the working group page (404).
