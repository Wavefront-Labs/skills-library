---
id: computing-software.cloud-infrastructure-engineering.azure.service-retirements-tracking-with-retirement-workbook
name: service-retirements-tracking-with-retirement-workbook
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, service-health, retirement-workbook, service-retirements, advisor, migration-planning]
level: practitioner
status: docs-checked
description: "Track Azure feature and service retirements that affect your estate using the Advisor service retirement workbook, Service Health notices and Resource Graph inventories."
sources: ["https://learn.microsoft.com/azure/advisor/advisor-how-to-plan-migration-workloads-service-retirement", "https://azure.microsoft.com/updates/?updateType=retirements", "https://learn.microsoft.com/azure/service-health/service-health-notifications-properties"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Service retirement tracking

**Goal:** know every retirement that touches your resources early enough to migrate calmly.

## Sources of truth
1. **Advisor service retirement workbook** (Advisor → Workbooks → *Service Retirement*): gives a resource-level view of service retirements affecting your resources.
2. **Service Health** advisories for retirements (set up alerts).
3. **Azure Updates** (lifecycle status of all Azure services) for things not yet in the workbook.

## Inventory queries
For each retirement the workbook does not cover, write an Azure Resource Graph query for the retiring SKU or feature using the retirement notice, save it as a shared query and pin it to a retirements dashboard.

## Process
- Register each applicable retirement in the backlog with owner, affected count, deadline, migration path and T-6 month checkpoint.
- Review monthly; re-run the workbook to watch counts drop.
- Use Azure Policy deny/audit to stop new deployments of the retiring SKU.
- Escalate items where the replacement changes pricing or architecture.

## Verify
- [ ] Workbook exported and attached to the monthly ops review; every row has an owner.
- [ ] Policy prevents new usage of retiring SKUs.

## Checked

2026-10-28. Confirmed on the Advisor Service Retirement workbook page: the workbook is under Advisor, Workbooks, Gallery, named Service Retirement, and gives a resource-level view of retirements; Azure Updates shows the lifecycle status of Azure services. Removed: the Basic public IP retirement date, the Service Health lead time and alert filter, the RSS feed claim, the three Resource Graph examples (property paths not confirmed) and the Application Gateway example.

Method: documentation only; no commands were run.
