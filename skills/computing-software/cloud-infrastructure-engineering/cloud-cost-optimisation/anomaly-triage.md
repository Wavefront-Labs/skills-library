---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.anomaly-triage
name: anomaly-triage
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, cost-anomaly-detection, anomaly-triage, root-cause-analysis, usage-type, cloudtrail, activity-log, audit-logs, cost-spike-runbook]
level: practitioner
status: docs-checked
description: "Triage a cost anomaly fast: confirm it's real, narrow by account/service/usage type/resource, find who changed what in audit logs, decide stop/accept/fix, and close the loop."
sources: ["https://www.finops.org/framework/capabilities/anomaly-management/", "https://docs.aws.amazon.com/awscloudtrail/latest/userguide/view-cloudtrail-events.html", "https://learn.microsoft.com/azure/azure-monitor/essentials/activity-log"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Anomaly triage runbook

## 1. Is it real? (5 min)
- Check data issues first: duplicate load, restated data, a commitment purchase in billed view,
  credits expiring, end of free tier. Compare effective vs billed.

## 2. Narrow down (15 min)
Drill in order: account/subscription/project → service → **usage type / SKU** →
region → resource id → hourly timeline (when did it start?).

## 3. Find the change (15 min)
- Audit logs around the start time: CloudTrail event history, Azure Activity Log, GCP Cloud Audit Logs. Who/what created or changed it?
- Deploy history and feature flags in that window.
- Usage metrics: request counts, egress bytes, log ingestion volume.

## 4. Classic causes
Runaway autoscaling or retry loop; logs at debug level; new NAT gateway path or cross-AZ chatter;
data replication/backup misconfig; forgotten load test / GPU instance; public bucket egress;
recursive Lambda / queue loop; leaked credentials mining crypto (treat as security incident).

## 5. Decide
- **Stop** (security, obvious mistake): scale down, delete, block — with owner approval or per
  pre-agreed policy.
- **Accept** (expected growth/launch): annotate, update forecast.
- **Fix** (inefficiency): ticket with owner and estimated savings.

## 6. Close
Record cause, $ impact, time to detect, time to resolve; add a preventive control (budget action,
quota, policy, usage alarm) for repeatable classes.

## Verify
- [ ] Each anomaly ticket has cause, impact and resolution recorded.
- [ ] Crypto-mining-like spikes trigger the security incident path.

## Checked
2026-11-01. Confirmed the audit-log sources in the CloudTrail event history and Azure Activity Log pages, and that the FinOps
Framework anomaly management capability covers detection, alerting and response. Removed:
the example AWS usage-type names and CloudTrail event names (not found in the pages read). The step time-boxes are
suggestions, not documented figures.
Method: documentation only; no commands were run.
