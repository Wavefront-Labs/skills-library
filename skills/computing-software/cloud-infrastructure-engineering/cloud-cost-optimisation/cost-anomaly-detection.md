---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.cost-anomaly-detection
name: cost-anomaly-detection
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, cost-anomaly-detection, anomaly-detection, aws-cost-anomaly-detection, cost-explorer, aws-budgets, budget-actions, azure-cost-management, cost-alerts, azure-anomaly-alerts, gcp-budgets, gcp-anomaly-detection, billing-export, bigquery-billing-export, cur, focus, cost-spikes, runaway-costs, nat-gateway, egress, logging-costs, ai-api-spend, triage, cost-guardrails, quotas, native-anomaly-detection]
level: practitioner
status: draft
description: "Catch cost spikes within a day: native anomaly detection and budgets per team, a daily billing-export query for the gaps, a triage runbook, and preventive guardrails for runaway resources."
sources: ["AWS Cost Anomaly Detection User Guide", "Microsoft Cost Management - Anomaly alerts and budgets", "Google Cloud Billing - Budgets and cost anomalies", "FinOps Foundation - Anomaly management capability"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cost anomaly detection — find the runaway resource the next morning, not at month-end

**Goal:** an unexpected spend increase is noticed within ~24 hours by the team that caused it,
triaged with a runbook, and the class of mistake is prevented next time.

## 1. Know the latency of your data
Billing data is not real-time: AWS Cost Explorer/CUR and Azure Cost Management typically lag
several hours up to ~24 h (some services longer); GCP billing export to BigQuery updates several
times a day. A misconfigured job can spend a lot before any cost tool sees it — pair cost
alerts with **usage** alerts (e.g. CloudWatch metric on invocations, egress bytes, log ingestion GB) for fast-moving risks.

## 2. Native detection first
- **AWS Cost Anomaly Detection:** ML-based monitors by service, linked account, cost category or cost-allocation tag; alert subscriptions with an absolute and/or percentage impact threshold (e.g. > $100 and > 20%), daily or individual alerts via SNS/Slack/email.
- **Azure Cost Management:** anomaly alerts per subscription (daily), plus budgets with alert thresholds and action groups.
- **Google Cloud:** budgets with threshold rules on actual and **forecasted** spend, Pub/Sub notifications for automation; cost anomaly detection in the Billing console.
Scope monitors by **team/cost centre** (tags or accounts) so alerts go to the owner, not a central FinOps inbox that forwards them days later.

## 3. Fill the gaps with your own query
Native ML misses slow drifts and new services. A daily job over the billing export:
```sql
-- BigQuery billing export; same idea on CUR in Athena or FOCUS-format data anywhere
WITH daily AS (
  SELECT DATE(usage_start_time) d, project.id p, service.description s, SUM(cost) c
  FROM `billing.gcp_billing_export_v1_XXXX`
  WHERE usage_start_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 35 DAY)
  GROUP BY 1,2,3)
SELECT * FROM (
  SELECT d, p, s, c,
    AVG(c) OVER w AS mean28, STDDEV(c) OVER w AS sd28
  FROM daily WINDOW w AS (PARTITION BY p, s ORDER BY d ROWS BETWEEN 28 PRECEDING AND 1 PRECEDING))
WHERE d = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)
  AND c > mean28 + 3*sd28 AND c - mean28 > 50   -- both relative and absolute floor
```
Add a "new service appeared in this project" check — first-ever spend on a service is a common signal.
Normalising to the FOCUS schema lets one query cover several providers.

## 4. Triage runbook
1. Confirm: is it real (not a one-off upfront commitment purchase, a credit expiry, or a billing data correction)?
2. Locate: drill by account → service → usage type → resource ID (CUR `line_item_resource_id`, or resource-level export).
3. Owner: tag/account owner notified; if unknown, the anomaly also becomes a tagging fix.
4. Contain: stop/scale down, fix config, or accept as expected (launch, migration) and annotate.
5. Record: cost impact, cause, prevention item — a short anomaly log reviewed monthly.

## 5. Usual suspects
NAT gateway data processing and cross-AZ/egress traffic; log ingestion after a DEBUG flag;
recursive serverless triggers (function writes to the bucket that triggers it); forgotten GPU
instances or notebooks; managed-service autoscaling without a max; LLM/AI API calls in a loop;
snapshots and backups without lifecycle; public data downloaded repeatedly from object storage.

## 6. Prevent
Max limits on autoscaling, service quotas set deliberately lower in sandboxes, budget actions
that apply restrictive policies or stop resources in non-prod (AWS Budgets actions, GCP budget
Pub/Sub → function), TTL tags on experimental resources with a reaper.

## Gotchas
- Percentage-only thresholds alert on $2 → $6; absolute-only thresholds miss small teams. Use both.
- Anomaly models need history; new accounts produce noise or nothing for the first weeks.
- Shared resources (one NAT, one cluster) hide which team spiked — allocate or split them.
- Automated shutdown on production is risky; restrict hard actions to non-prod.

## Verify
- [ ] Every team/cost centre has a monitor routed to its own channel.
- [ ] Usage-based alerts exist for fast-moving risks (egress, logs, function invocations, AI API spend).
- [ ] A daily custom query catches drifts and new-service spend.
- [ ] Anomaly log with cause and prevention item is reviewed monthly.
- [ ] Non-prod has budget actions or quotas capping runaway spend.

Uncertain: billing data latencies vary by provider and service; measure yours. The SQL is a sketch — adapt table names and columns to your export.
