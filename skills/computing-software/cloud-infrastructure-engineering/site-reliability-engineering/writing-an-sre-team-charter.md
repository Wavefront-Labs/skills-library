---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.writing-an-sre-team-charter
name: writing-an-sre-team-charter
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [sre, sre-engagement, sre-charter, team-mission, engagement-model, responsibilities]
level: advanced
status: docs-checked
description: "What the SRE Workbook says an SRE team charter should reflect, with the engagement phases, workload principles and handback conditions a charter has to take a position on."
sources: ["https://sre.google/workbook/team-lifecycles/", "https://sre.google/workbook/engagement-model/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Writing an SRE team charter

The Workbook says little about charter format. It says: "Each SRE team should have a clear charter that reflects their services, technology, and operations" (Engagement Model, "Adapting SRE Team Structures to Changing Circumstances"). The points below are what the two chapters give you to put into one.

## Services and scope
- Services covered by the team. Group teams by product or by technology stack (for example storage or networking); the Workbook recommends technology over developer reporting structure to avoid churn during developer reorganisations.
- When a team splits, components can be left with no owner; mitigate by designating one team responsible for everything not covered in the other team's charter, or by appointing a senior SRE as technical lead across both (Team Lifecycles, "Pitfalls").
- Split options listed: architectural (compute, storage, network; frontend and backend), language, and location.
- Singleton teams are generally less effective and more vulnerable to reorganisations outside the team; the Workbook creates them only for clearly defined business needs.

## Where SRE engages (Engagement Model, "The Service Lifecycle")
Phases: architecture and design; active development; limited availability; general availability; deprecation; abandoned; unsupported. The chapter says SRE may begin at any phase, strongly recommends defining SLOs before general availability, and recommends the developer team keeps a small share of operational and incident work in GA, for example one developer permanently in the on-call rotation.

## Principles the team asserts (Team Lifecycles)
1. SRE needs SLOs with consequences.
2. SREs must have time to make tomorrow better than today (a healthy balance of operations and project work; one team in the chapter reached a goal of more than 50% project work).
3. SRE teams regulate their own workload: they choose if and when to onboard a service, can reduce toil by lowering the SLO or moving work to another team, and can hand a service back if it cannot be run at SLO within agreed toil constraints. The chapter says this needs strong leadership and clear up-front commitment from senior management.

## Ending the relationship
Say when a service is handed back: when SRE no longer provides enough business value (service optimised, less relevant, end of life). See `ending-sre-engagement-and-handback`.

## Checked
- 2026-11-08: all quotes and points above were confirmed on the Workbook Team Lifecycles and Engagement Model pages.
- Removed: the numbered template (mission example, RACI, success metrics, intake rules, yearly review), the "toil capped at 50%" principle (the chapter mentions a more-than-50% project-work goal for one team, not a cap), and the SRE Book introduction and how-SRE-relates sources, which no remaining claim uses.
Method: docs-only read of cited pages, 2026-11-08
