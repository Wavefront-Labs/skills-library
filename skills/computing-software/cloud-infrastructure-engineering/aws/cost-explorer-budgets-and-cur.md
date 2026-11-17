---
id: computing-software.cloud-infrastructure-engineering.aws.cost-explorer-budgets-and-cur
name: cost-explorer-budgets-and-cur
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cost-explorer, budgets, cost-and-usage-report, cur, cur-2, cost-allocation, data-exports, athena-cur, budget-actions, cost-categories, finops, showback, chargeback, savings-plans-coverage, reserved-instance-utilization, billing-conductor, consolidated-billing, unblended-amortized-net, cost-explorer-api, get-cost-and-usage]
level: practitioner
status: draft
description: "Set up AWS cost visibility: Cost Explorer views and API, Cost Categories for showback, Budgets with actions, and Cost and Usage Reports (Data Exports) queried in Athena."
sources: ["AWS Cost Management User Guide - Analyzing your costs with AWS Cost Explorer", "AWS Cost Management User Guide - Managing your costs with AWS Budgets", "AWS Data Exports User Guide - Cost and Usage Report 2.0", "AWS Cost Management User Guide - Cost Categories"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cost Explorer, Budgets and CUR — know the bill before finance does

**Goal:** every team sees its own spend (showback), overruns alert the owner the same day,
commitments are tracked, and the raw CUR in Athena answers anything the console cannot.
(Rightsizing and commitment purchasing: `computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.rightsizing-and-commitments`.)

## 1. Foundations (payer account)
- **Consolidated billing** via Organizations; member accounts see their own costs only if
  the payer enables *Cost Explorer access for linked accounts*. Enable Cost Explorer once
  (data starts from enablement; 13 months history + 12 months forecast).
- Activate **cost allocation tags** (`cost-center`, `application`, `environment`) and
  AWS-generated `aws:createdBy`. Define **Cost Categories** (rules mapping accounts/tags/
  services → `Team: Payments`, with a default "Unallocated") — they apply across Cost
  Explorer, Budgets and CUR and fix the "untagged" problem at the account level.
- Choose the **cost metric** deliberately: *Unblended* (what each account was charged),
  *Amortized* (upfront RI/SP spread evenly — the right one for showback), *Net* (after
  credits/discounts), *Blended* (averaged rates; avoid).
- **Split cost allocation data** for ECS/EKS splits shared cluster cost by task/pod CPU/memory.

## 2. Cost Explorer
- Core views to save: *Monthly by service*, *Daily by account (last 14 d)*, *By Cost
  Category Team, amortized*, *Savings Plans coverage/utilisation*, *RI utilisation*,
  *Usage type* for data transfer (`DataTransfer-Out-Bytes`, `…-Regional-Bytes`).
- Filters: exclude credits/refunds/support for run-rate; group by `Usage Type` or
  `API operation` to find the surprise (e.g. `NatGateway-Bytes`, `TimedStorage-ByteHrs`).
- **Hourly + resource-level** granularity (opt-in, 14 days) for EC2 instance ids.
- API: `aws ce get-cost-and-usage --time-period Start=2026-10-01,End=2026-10-15 --granularity DAILY --metrics AmortizedCost --group-by Type=DIMENSION,Key=SERVICE`
  (billed per request; cache). `get-cost-forecast`, `get-savings-plans-coverage`,
  `get-rightsizing-recommendation`.
- Forecast uses ML on history; new workloads make it useless for ~2 weeks.

## 3. Budgets
```bash
aws budgets create-budget --account-id <payer> --budget '{"BudgetName":"team-payments-monthly","BudgetLimit":{"Amount":"12000","Unit":"USD"},"TimeUnit":"MONTHLY","BudgetType":"COST","CostFilters":{"CostCategory$Team":["Payments"]},"CostTypes":{"IncludeCredit":false,"IncludeRefund":false,"UseAmortized":true}}' \
  --notifications-with-subscribers '[{"Notification":{"NotificationType":"ACTUAL","ComparisonOperator":"GREATER_THAN","Threshold":80,"ThresholdType":"PERCENTAGE"},"Subscribers":[{"SubscriptionType":"SNS","Address":"arn:aws:sns:…:cost-alerts"}]},{"Notification":{"NotificationType":"FORECASTED","ComparisonOperator":"GREATER_THAN","Threshold":100,"ThresholdType":"PERCENTAGE"},"Subscribers":[{"SubscriptionType":"EMAIL","Address":"payments-leads@example.com"}]}]'
```
- Types: **Cost**, **Usage** (e.g. GB of NAT), **RI/SP utilisation** (alert < 90 %),
  **RI/SP coverage** (alert < 70 %). Use **FORECASTED** thresholds to catch overruns early
  in the month; **auto-adjusting budgets** (based on trailing average) for growth teams.
- **Budget actions**: on threshold, apply an IAM/SCP deny policy or stop EC2/RDS instances
  (sandbox accounts: `Deny ec2:RunInstances` at 100 %). Needs a budgets role; approval optional.
- Budgets evaluate ~3×/day on billing data that lags 8–24 h — not real-time; pair with
  Cost Anomaly Detection for spikes.
- One budget per team/account from a loop in IaC; SNS → Slack with the cost category in the subject.

## 4. CUR / Data Exports
- Create **CUR 2.0** (Data Exports) to S3: Parquet, hourly granularity, resource ids on,
  split cost allocation on, `overwrite` versioning; delivered 1–3×/day; month restated until finalised (~day 3–5 of next month).
- Query with Athena (the export creates a Glue crawler/table setup):
  ```sql
  SELECT line_item_usage_account_id, product_servicecode, line_item_resource_id,
         SUM(line_item_unblended_cost) cost
  FROM cur WHERE bill_billing_period_start_date = DATE '2026-10-01'
    AND line_item_line_item_type IN ('Usage','DiscountedUsage','SavingsPlanCoveredUsage')
  GROUP BY 1,2,3 ORDER BY cost DESC LIMIT 50;
  ```
  Key columns: `line_item_line_item_type` (Usage, Tax, Fee, Credit, RIFee, SavingsPlanRecurringFee…),
  `line_item_usage_type`, `pricing_term`, `resource_tags_user_<tag>`, `cost_category_<name>`,
  `savings_plan_savings_plan_effective_cost`, `reservation_effective_cost` (for amortised).
- Deploy **CUDOS / Cloud Intelligence Dashboards** (QuickSight) on the CUR for ready-made
  FinOps views; or the **Cost Optimization Hub** export for recommendations.
- **Billing Conductor** when you need to re-rate costs for internal customers (custom pricing plans) in showback.

## 5. Cadence
- Daily: anomaly + budget alerts to owners. Weekly: top-10 movers by usage type.
- Monthly: close with finalised CUR; showback by Cost Category; unallocated < 5 %.
- Quarterly: coverage/utilisation review → commitment purchases.

## Gotchas
- Cost allocation tags are not retroactive; Cost Categories *are* (back to history in Cost Explorer).
- Amortised vs unblended mismatch between teams' reports and finance's invoice causes endless reconciliation — publish which metric each report uses.
- Budget emails go to spam; use SNS → chat/pager and keep ≤ 10 subscribers per notification.
- CUR size grows with resource ids + hourly: partition by month in Athena and use columnar filters, or costs explode.
- Marketplace, support and tax lines have no resource id and no tag — expect them in "Unallocated".
- Unconfirmed: current CUR 2.0 column names vs legacy CUR (`line_item_*` vs nested) — check the Data Exports schema page before writing queries.

## Verify
- [ ] Cost Explorer "by Cost Category Team, amortized" shows < 5 % Unallocated for last month.
- [ ] Each team has a budget with ACTUAL 80 % and FORECASTED 100 % alerts to a channel they read.
- [ ] A sandbox budget action denies `RunInstances` when tested with a low threshold.
- [ ] Athena query over CUR reproduces last month's invoice total within rounding (`line_item_unblended_cost` incl. tax/fees).
- [ ] Savings Plans utilisation budget alerts below 90 %.
