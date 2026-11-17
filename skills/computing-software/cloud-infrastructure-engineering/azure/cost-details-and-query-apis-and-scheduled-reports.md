---
id: computing-software.cloud-infrastructure-engineering.azure.cost-details-and-query-apis-and-scheduled-reports
name: cost-details-and-query-apis-and-scheduled-reports
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, cost-management, cost-details-api, cost-query-api, finops-automation]
level: practitioner
status: docs-checked
description: "Pull Azure cost data programmatically: Exports for scale, the Cost Details async API for on-demand files, and the Query API for aggregates."
sources: ["https://learn.microsoft.com/azure/cost-management-billing/automate/usage-details-best-practices", "https://learn.microsoft.com/rest/api/cost-management/generate-cost-details-report", "https://learn.microsoft.com/rest/api/cost-management/query/usage"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cost Details and Query APIs

**Goal:** feed cost data to scripts and dashboards without scraping the portal.

## Which route
| Need | Use |
|---|---|
| Recurring cost details at scale | **Exports**: recurring dumps to a storage account on a custom schedule, with optional file partitioning. Microsoft's recommended and most scalable option |
| On-demand cost details for small datasets | **Cost Details API** (async report). Use when Exports to storage are not feasible for security or manageability reasons |
| Aggregated usage for a scope | **Query API** |
| Large files in Excel or the portal | Avoid; files over 1 to 2 GB take very long to generate on demand |

The Cost Details API replaces the earlier Usage Details APIs. It is only available for Enterprise Agreement and Microsoft Customer Agreement customers; pay-as-you-go and Visual Studio customers use the legacy usage details route.

## Cost Details API practices
- Reports refresh every four hours, so query for the latest data at most once per day.
- Downloaded data for historical invoices does not change unless Microsoft notifies you, so cache it in a queryable store.
- Chunk calls into small date ranges (by day or week) for manageable files.
- For scopes with lots of usage (a billing account), call child scopes instead; if rate limits hit at a lower scope, try a higher scope.
- Roughly 1 GB of cost details is about 1 million rows. If the dataset exceeds 2 GB a month, switch to Exports.
- The create call returns a Location header; use that link with the Get Operation Results operation to fetch the result.

## Query API
`POST https://management.azure.com/{scope}/providers/Microsoft.CostManagement/query?api-version=<version>` with a body containing `type`, `timeframe` and `dataset` (and `timePeriod` when the timeframe is custom). Responses are 200 with a result, or 204 with no content. Large results carry a `nextLink` containing a `$skiptoken` for the next page.

Supported scopes include subscription, resource group, management group, billing account, department, enrollment account, billing profile, invoice section and (for partners) customer.

## Verify
- [ ] Script totals match portal cost analysis for the same scope and period.

## Checked
Method: docs-checked 2026-11-09 against usage-details-best-practices, the generate-cost-details-report overview and the Query - Usage reference (all downloaded with curl as Learn markdown and read in full or by section). Dropped rate-limit header names, scheduled email views, the example request bodies, latency figures and role claims, which these pages do not confirm.
