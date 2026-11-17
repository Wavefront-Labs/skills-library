---
id: computing-software.cloud-infrastructure-engineering.azure.cost-management-tag-inheritance-and-tag-based-reporting
name: cost-management-tag-inheritance-and-tag-based-reporting
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, cost-management, cost-tag-inheritance, tag-cost-reporting, untagged-costs, finops]
level: practitioner
status: docs-checked
description: "Report Azure cost by tag: enable Cost Management tag inheritance from subscriptions and resource groups, handle untagged spend, and use tags in views and exports."
sources: ["https://learn.microsoft.com/azure/cost-management-billing/costs/enable-tag-inheritance", "https://learn.microsoft.com/azure/cost-management-billing/costs/cost-mgt-best-practices"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cost reporting by tag and tag inheritance

**Goal:** spend lands on a cost centre in reports even when resource-level tagging is patchy.

## Tag inheritance (billing side)
- Available for Enterprise Agreement (EA), Microsoft Customer Agreement (MCA) and Microsoft Partner Agreement (MPA) with Azure plan subscriptions.
- Enable it in the Azure portal under Cost Management configuration, at the EA billing account, MCA billing profile or subscription scope. You need a supported scope and the right permissions or the option does not appear.
- EA and subscription scope apply subscription and resource group tags; MCA billing profile scope also applies billing profile and invoice section tags.
- Inherited tags go onto child resource **usage records**, not onto the resources themselves.
- When a resource tag matches an inherited tag, the resource tag wins by default. You can switch the setting to "Use the inherited tag" so the subscription or resource group tag overrides it.
- After you change the setting or an inherited tag, usage records update in about 8-24 hours, for the current month only: enabling it on October 20 updates records from October 1 using the tags that existed on October 20.
- Purchases or resources that do not emit usage at subscription scope do not get subscription tags even when the setting is on.

## Reporting
- Cost analysis: choose a scope, then **Group by** the tag you want (for example `org`).
- Budgets can filter on inherited tags starting 24 hours after enabling inheritance.
- Downloaded usage data shows the inherited tags.
- Cost analysis supports filtering and grouping by tags, management groups and custom dimensions.

## Shrinking untagged spend
1. Group by tag to see which spend lacks it.
2. Put the tag on the resource group or subscription so inheritance covers the resources below it.
3. For shared resources used by several teams, tag the resources that make up a workload so costs can be reported across scopes, and enforce tagging with Azure Policy.

## Verify
- [ ] Tag inheritance setting shows enabled at the intended scope.
- [ ] After 24 hours, Cost analysis grouped by the tag shows inherited values for resources that lacked their own.

## Checked

Method: docs-checked 2026-11-09 against the tag inheritance page and the Cost Management best practices page (downloaded, converted to text and read). Dropped unconfirmed claims: the saved-view and scheduled-email steps, Power BI `Json.Document` and FinOps hubs tag handling, cost allocation rules, the policy modify inheritance, the amortised cost advice, tag key case merging, and the "from that day forward" resource group note. Removed the unread tag-support source.
