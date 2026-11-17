---
id: computing-software.cloud-infrastructure-engineering.aws.cost-explorer-filtering-grouping-and-usage-types
name: cost-explorer-filtering-grouping-and-usage-types
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cost-explorer, cost-explorer-filters, group-by-usage-type, usage-type-groups, cost-investigation, get-cost-and-usage]
level: practitioner
status: docs-checked
description: "Investigate AWS spend in Cost Explorer: filter and group by service, account, usage type, operation, tag and resource, read usage type codes, and reproduce views with the CE API."
sources: ["https://docs.aws.amazon.com/cost-management/latest/userguide/ce-filtering.html", "https://docs.aws.amazon.com/cost-management/latest/userguide/ce-advanced.html", "https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_GetCostAndUsage.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cost Explorer filtering, grouping and usage types

## 1. The investigation loop
1. **Group by Service**, daily granularity: which service moved?
2. Filter to that service, **group by Usage type**: which kind of usage moved?
3. Group by **Linked account** / **Region** / **Tag** / **Cost category**: who?
4. Group by **API operation** (the `OPERATION` dimension) for request-driven services.
5. For exact resource IDs, use your cost and usage data exports instead of Cost Explorer.

## 2. Usage types and usage type groups
A **usage type** is a unit each service uses to measure usage of a specific type of resource; for example
`BoxUsage:t2.micro(Hrs)` filters by the running hours of EC2 t2.micro instances. **Usage type groups** collect
related usage types into one filter; for example the `EC2: Running Hours` group contains the `BoxUsage:...(Hrs)`
types for several instance types, and `EC2: Data Transfer - Inter AZ` is another group. Look up the usage types
in your own account with `get-dimension-values` rather than guessing codes.

## 3. Cost views
- **Unblended** shows reservation fees as a spike on the day you are charged; **amortized** spreads those fees
  over the billing period. Use amortized for team showback. Net variants (`NET_UNBLENDED_COST`,
  `NET_AMORTIZED_COST`) are also available.
- To exclude credits, refunds or tax, filter on the `RECORD_TYPE` dimension.
- To find untagged spend, use the filter that shows only untagged resources.

## 4. API for reproducible reports
```bash
aws ce get-cost-and-usage --time-period Start=<START_DATE>,End=<END_DATE> \
  --granularity DAILY --metrics UnblendedCost UsageQuantity \
  --filter '{"Dimensions":{"Key":"SERVICE","Values":["<SERVICE_NAME>"]}}' \
  --group-by Type=DIMENSION,Key=USAGE_TYPE
aws ce get-dimension-values --time-period Start=<START_DATE>,End=<END_DATE> --dimension SERVICE
aws ce get-dimension-values --time-period Start=<START_DATE>,End=<END_DATE> --dimension USAGE_TYPE \
  --search-string <TEXT>
```
Dimensions valid for `GetCostAndUsage` filters include `AZ`, `INSTANCE_TYPE`, `LINKED_ACCOUNT`, `OPERATION`,
`PLATFORM`, `PURCHASE_TYPE`, `SERVICE`, `TENANCY`, `RECORD_TYPE` and `USAGE_TYPE`. Granularity is `DAILY`, `MONTHLY`
or `HOURLY`. Take exact service names from `get-dimension-values --dimension SERVICE`.

## Verify
- [ ] Spike traced to service, usage type and account with a saved report.
- [ ] Showback uses amortized costs grouped by cost category or tag.
- [ ] Recurring views scripted with `get-cost-and-usage`.

## Checked
2026-10-28: Confirmed against the Cost Management User Guide pages ce-filtering and ce-advanced and the Cost Explorer API Reference GetCostAndUsage page: the BoxUsage:t2.micro(Hrs) usage type example, usage type groups (EC2: Running Hours, EC2: Data Transfer - Inter AZ), the unblended versus amortized behaviour for reservation fees, the untagged-resources filter, the dimension list including OPERATION and RECORD_TYPE, and DAILY/MONTHLY/HOURLY granularity. The CLI commands passed check_commands.py. Read end to end. Removed as unconfirmed: the table of region-prefixed usage type codes, the 14-day resource-level and hourly data limits, the data refresh interval, API request pricing note, the tag activation and EC2-Other notes, and the literal EC2 service name (replaced with a placeholder).

Method: documentation only; no commands were run.
