---
id: computing-software.cloud-infrastructure-engineering.aws.cost-anomaly-root-cause-analysis
name: cost-anomaly-root-cause-analysis
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cost-anomaly-detection, anomaly-root-cause, cost-explorer, finops, anomaly-feedback, usage-type]
level: practitioner
status: docs-checked
description: "Trace Cost Anomaly Detection alerts to root cause: anomaly root causes by service, account, region and usage type, drilling into Cost Explorer and CUR, and feedback."
sources: ["https://docs.aws.amazon.com/cost-management/latest/userguide/ce-filtering.html", "https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_GetCostAndUsage.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cost anomaly root cause analysis

## Monitors and alerts (setup recap)
- Monitor dimension (`MonitorDimension`): `SERVICE`, `LINKED_ACCOUNT`, `TAG` or `COST_CATEGORY`; monitor type is
  `DIMENSIONAL` or `CUSTOM` (custom monitors use a `MonitorSpecification` expression).
- Subscriptions (`create-anomaly-subscription`): subscriber type `EMAIL` or `SNS`; frequency `IMMEDIATE`,
  `DAILY` or `WEEKLY`; alert on impact with `ThresholdExpression` (the plain `Threshold` field is deprecated).

## Read the anomaly
```bash
aws ce get-anomalies --date-interval StartDate=<START_DATE>,EndDate=<END_DATE> \
  --total-impact NumericOperator=GREATER_THAN,StartValue=100 \
  --query 'Anomalies[].{id:AnomalyId,impact:Impact.TotalImpact,start:AnomalyStartDate,root:RootCauses}'
```
Each anomaly has `Impact` (`MaxImpact`, `TotalImpact`, `TotalImpactPercentage`), an `AnomalyScore`
(`MaxScore`, `CurrentScore`) and `RootCauses`. A root cause can name `Service`, `Region`, `LinkedAccount`,
`LinkedAccountName` and `UsageType`, with its own `Impact`. The usage type tells you what changed.
`--total-impact` takes a `NumericOperator` of `EQUAL`, `GREATER_THAN_OR_EQUAL`, `LESS_THAN_OR_EQUAL`,
`GREATER_THAN`, `LESS_THAN` or `BETWEEN` (with `EndValue`); `--feedback` filters by `YES`, `NO` or `PLANNED_ACTIVITY`.

## Drill down
1. Cost Explorer: filter by the root cause's service and usage type, choose daily granularity, and group by
   linked account (Cost Explorer filters include service, usage type, usage type group and more).
2. Use your cost and usage data exports for exact resources and hours.
3. Correlate with change history: deployments, CloudTrail events for resource creation, traffic graphs.

## Feedback and closure
```bash
aws ce provide-anomaly-feedback --anomaly-id "$ID" --feedback PLANNED_ACTIVITY   # or YES / NO
```
Record cause, fix and avoided cost in a FinOps log.

## Verify
- [ ] Each anomaly over threshold has an owner, root cause and feedback within a week.
- [ ] Recurring causes produce preventive controls (lifecycle rules, endpoints, budgets).

## Checked
2026-10-28: Confirmed against the botocore ce model (GetAnomalies input and output shapes, AnomalyFeedbackType, NumericOperator, MonitorType, MonitorDimension, AnomalySubscriptionFrequency, SubscriberType, deprecated Threshold) and the Cost Explorer filtering page (service, usage type, usage type group filters). The get-anomalies and provide-anomaly-feedback commands passed check_commands.py. Read end to end. Removed as unconfirmed: the table of usage type patterns and their usual causes, example usage type names, the 14-day resource-level data claim, the Athena CUR query, and "near real time" alert wording.

Method: documentation only; no commands were run.
