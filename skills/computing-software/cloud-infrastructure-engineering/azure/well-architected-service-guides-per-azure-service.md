---
id: computing-software.cloud-infrastructure-engineering.azure.well-architected-service-guides-per-azure-service
name: well-architected-service-guides-per-azure-service
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, well-architected-review, waf-service-guide, service-guide-checklist, design-review]
level: advanced
status: docs-checked
description: "Apply Azure Well-Architected service guides to review a workload per service: map the five pillars' checklists and configuration recommendations to findings and backlog items."
sources: ["https://learn.microsoft.com/azure/well-architected/service-guides/", "https://learn.microsoft.com/azure/well-architected/pillars", "https://learn.microsoft.com/assessments/azure-architecture-review/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Well-Architected service guides

**Goal:** go beyond the generic Well-Architected Review with per-service recommendations.

## What to expect from a service guide
Microsoft publishes a service guide for many Azure services (the index lists, for example, App Service and Event Hubs).
Open the guide for each service in your workload and read how it applies the five pillars (Reliability, Security, Cost
Optimization, Operational Excellence, Performance Efficiency). The exact sections differ per guide: read the guide
rather than assuming a fixed layout, and use the pillar identifiers that guide cites.

## Review procedure
1. List the workload's services from the architecture diagram or an Azure Resource Graph query over its resource groups.
2. For each service, open its guide; walk the recommendations with the workload team; record status (met / partial /
   not met / not applicable) with evidence.
3. Map "not met" items to the backlog with pillar and risk.
4. Where a guide names Azure Policy definitions or Advisor recommendations, use them in audit mode to measure drift.
5. Repeat after major releases.

## Tips
- Start with Reliability and Security items for production.
- Use the Azure Well-Architected Review assessment for workload-level questions and service guides for per-service depth.
- Record deliberate exceptions (for example single-region by business choice) so they are not re-raised every review.

## Verify
- [ ] Review document lists every service with status and links to backlog items.

## Checked
2026-10-28. Confirmed (Learn: well-architected/service-guides index, pillars): service guides exist per service (App Service,
Event Hubs among those listed) and cover the five pillars. Removed (unconfirmed in fetched pages): list of services such as
Azure OpenAI/Front Door/Cosmos DB, RE:05 and SE:07 identifiers, "Use Premium v3 for zone support" and other example
settings, the guaranteed checklist/configuration-table/Policy/Advisor layout, quarterly cadence.
Method: documentation only; no commands were run.
