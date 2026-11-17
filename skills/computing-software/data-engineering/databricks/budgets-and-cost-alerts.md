---
id: computing-software.data-engineering.databricks.budgets-and-cost-alerts
name: budgets-and-cost-alerts
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, databricks-budgets, cost-alerts, budget-policies, finops]
level: practitioner
status: docs-checked
description: "Set up Databricks budgets and cost alerts: account budgets with tag and workspace filters, thresholds, serverless usage policies, SQL alerts."
sources:
  - https://docs.databricks.com/aws/en/admin/account-settings/budgets
  - https://docs.databricks.com/aws/en/admin/usage/budget-policies
  - https://docs.databricks.com/aws/en/admin/system-tables/pricing
  - https://docs.databricks.com/aws/en/admin/system-tables/billing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Budgets and cost alerts

**Goal:** know before month-end when a team or workspace is overspending.

## Account budgets
Account admins create budgets in the account console: Usage > Budgets tab > Add budget (workspace admins can manage budgets for workspaces they administer through Governance Hub).
- Measured in USD at the SKU list price; credits and negotiated discounts are not factored in.
- Definitions limit what is tracked: workspaces, resource types, and custom tags (for example `team = marketing`). Leave them blank to track the whole account.
- Up to four shared monthly thresholds per budget, each with a unique dollar amount and a comma-separated list of email addresses. Recipients need not be Databricks users.
- Up to 1,000 budgets per account. Emails can lag usage by up to 24 hours.
- "Block usage" exists only for Unity Gateway budgets (one threshold, the highest). Budgets for other products are for monitoring and alerts; use policies and limits to constrain compute.
- Tag data is stored as plain text and may be replicated globally, so keep sensitive information out of tag names and values.

## Tag everything
- Classic compute: custom tags on compute, applied to cloud resources and usage logs (limit via compute policies).
- Serverless: **serverless usage policies** (Public Preview) hold tags that are applied to serverless activity of assigned users on notebooks, jobs, pipelines, serving endpoints and apps. Existing assets do not pick up a policy automatically, pipelines triggered by a job do not inherit the job's policy, and policies do not tag classic compute. Tags land in `custom_tags` in `system.billing.usage`.

## SQL alert on anomalies
```sql
SELECT u.usage_date, sum(u.usage_quantity * lp.pricing.effective_list.default) AS cost
FROM system.billing.usage u
JOIN system.billing.list_prices lp
  ON u.sku_name = lp.sku_name AND u.cloud = lp.cloud
 AND u.usage_start_time >= lp.price_start_time
 AND (lp.price_end_time IS NULL OR u.usage_start_time < lp.price_end_time)
WHERE u.usage_date >= current_date() - 14
GROUP BY 1 ORDER BY 1;
```
`system.billing.list_prices` has one row per price change per SKU; `pricing.effective_list.default` resolves list and promotional prices. Create a Databricks SQL alert when yesterday's cost exceeds 1.5x the 7-day average (a threshold you choose, not a Databricks default).

## Hard limits (where you need them)
- Compute policies: max workers, node types, auto termination.
- Job timeouts.

## Gotchas
- Budgets use list price, not your contract price.
- `system.billing.usage` updates every few hours, so it can show less than a budget alert email received at the same moment; it remains the source of truth for billable usage.

## Verify
A test budget with a tiny threshold sends an email; the anomaly alert fires on a synthetic spike.

## Checked

2026-11-09: reviewed against the Databricks documentation fetched this batch.

Confirmed: the budget creation path and requirements, list-price USD basis, four shared thresholds, 1,000 budget limit, 24-hour email delay, block-usage scope, serverless usage policy behaviour and limitations, tags in `system.billing.usage` `custom_tags`, and the `system.billing.list_prices` columns including `pricing.effective_list` (budgets, usage policy, billing and pricing system table pages).

Removed or corrected: "budget policies" and `budget_policy_id` (now serverless usage policies), the 50/80/100 percent thresholds and SKU filter, tag-key case sensitivity, SQL warehouse tag settings and max clusters, `max_concurrent_runs`, and the list price versus pricing.default join (now effective_list with a cloud match).

Method: documentation only; no commands were run.
