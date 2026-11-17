---
id: computing-software.cloud-infrastructure-engineering.aws.aws-budgets-usage-ri-and-savings-plans-budgets
name: aws-budgets-usage-ri-and-savings-plans-budgets
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, budgets, usage-budget, savings-plans-budget, ri-utilization-budget, budget-actions, finops]
level: practitioner
status: draft
description: "Pick the right AWS Budgets type: cost, usage, RI and Savings Plans utilisation and coverage budgets, with thresholds on actual and forecast, alert routing and budget actions."
sources: ["AWS Cost Management User Guide - Managing your costs with AWS Budgets (budget types)", "AWS Budgets API Reference - CreateBudget", "AWS Cost Management User Guide - Configuring budget actions"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# AWS Budgets: usage, RI and Savings Plans budgets

## Budget types
| Type | Tracks | Typical use |
|---|---|---|
| `COST` | spend (unblended/amortized/net) with filters | per account, per tag, per service monthly caps |
| `USAGE` | quantity of a usage type group (GB-Mo, hours, requests) | catch runaway S3 storage, NAT GB processed, EC2 hours in sandboxes |
| `RI_UTILIZATION` | % of purchased RI hours used | alert when under ~80% (waste) |
| `RI_COVERAGE` | % of eligible usage covered by RIs | alert when coverage drops (new uncovered usage) |
| `SAVINGS_PLANS_UTILIZATION` | % of SP commitment used | alert under ~90% |
| `SAVINGS_PLANS_COVERAGE` | % of eligible spend covered by SPs | alert when under target (e.g. 70%) |

## Usage budget example
```json
{"BudgetName":"s3-storage-gb","BudgetType":"USAGE","TimeUnit":"MONTHLY",
 "BudgetLimit":{"Amount":"50000","Unit":"GB-Mo"},
 "CostFilters":{"UsageTypeGroup":["S3: Storage - Standard"]}}
```
```bash
aws budgets create-budget --account-id 111122223333 --budget file://usage.json \
  --notifications-with-subscribers '[{"Notification":{"NotificationType":"FORECASTED",
   "ComparisonOperator":"GREATER_THAN","Threshold":100,"ThresholdType":"PERCENTAGE"},
   "Subscribers":[{"SubscriptionType":"SNS","Address":"arn:aws:sns:us-east-1:111122223333:finops"}]}]'
```

## Utilisation/coverage budgets
- Granularity daily or monthly; daily catches a big drop (e.g. migration moved instances to another family the RI does not cover) within a day.
- Filter by service (EC2, RDS, ElastiCache, OpenSearch, Redshift for RIs) and linked account.
- Notifications fire when utilisation/coverage goes **below** the threshold.

## Alerts and actions
- Up to several notifications per budget; ACTUAL and FORECASTED thresholds (e.g. forecast 100%, actual 80% and 100%).
- Subscribers: email, SNS (topic policy must allow `budgets.amazonaws.com`), chat via SNS + Amazon Q Developer in chat applications.
- **Budget actions** run automatically or after approval: attach an IAM policy or SCP denying new launches, or stop specific EC2/RDS instances. Use in sandboxes, not production.

## Gotchas
- Billing data lags up to ~24 hours; budgets are not real-time guards.
- Budgets evaluate a few times a day; a spike can exceed the limit before the alert.
- Credits and refunds affect COST budgets depending on the selected cost aggregation; exclude credits to see true usage.
- Free tier usage budgets exist as templates for new accounts.

## Verify
- [ ] Each account has a cost budget with forecast alerts; SP/RI utilisation and coverage budgets exist in the management account.
- [ ] Test SNS subscription receives a budget notification.
