---
id: computing-software.cloud-infrastructure-engineering.aws.service-quotas-automatic-management
name: service-quotas-automatic-management
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, service-quotas, automatic-quota-management, quota-utilization, quota-notifications]
level: practitioner
status: docs-checked
description: "Turn on Service Quotas automatic management to watch quota utilisation, get notified before exhaustion and optionally have increases requested for you, with exclusions."
sources: ["https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Quotas-Visualize-Alarms.html", "https://github.com/boto/botocore/tree/develop/botocore/data/service-quotas"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Service Quotas automatic management

**Goal:** stop discovering quota exhaustion through failed deployments; let Service Quotas track
utilisation for supported quotas and notify (or request increases) ahead of time.

## What it does
- Monitors utilisation of supported quotas in the account.
- **Notify only** (`NotifyOnly`): sends notifications (to the `NotificationArn`) when utilisation crosses thresholds.
- **Notify and adjust** (`NotifyAndAdjust`): additionally submits quota increase requests automatically for supported
  adjustable quotas, within AWS's limits, so headroom grows with usage.
- Exclusion list for quotas you manage deliberately (e.g. kept low as a cost guardrail).

## Enable
Use the console or the API (`StartAutoManagement`, `GetAutoManagementConfiguration`, `UpdateAutoManagement`, `StopAutoManagement`):
1. Choose the mode (`OptInType`: `NotifyOnly` or `NotifyAndAdjust`; `OptInLevel` is `ACCOUNT`).
2. Set the notification (`NotificationArn`).
3. Add exclusions (`ExclusionList`).
4. Repeat per account; roll out with automation across the organization.

## How it fits with other controls
| Control | Role |
|---|---|
| Automatic management | continuous headroom for supported quotas |
| AWS/Usage alarms with `SERVICE_QUOTA()` | precise alarms on the few critical quotas |
| Throttling metrics | rate-based quotas (API TPS) |

## Gotchas
- Not every quota is covered; keep explicit alarms on the critical ones.
- Auto-increases raise blast radius (e.g. runaway scaling can now launch more instances): keep budgets and anomaly detection on.
- Some quotas are deliberately low as guardrails (vCPU in sandbox accounts); exclude them.

## Verify
- [ ] Mode and notification configured in each production account.
- [ ] A notification received for a test or real threshold crossing; exclusions documented.

## Checked

2026-10-28

Confirmed: SERVICE_QUOTA() metric math function for quota lines and alarms (CloudWatch guide); StartAutoManagement/Get/Update/Stop operations, OptInType NotifyOnly and NotifyAndAdjust, OptInLevel ACCOUNT, NotificationArn, ExclusionList (botocore service-quotas).

Removed: User Notifications channel list, console path, per-Region claim, Slack/chat-application detail, request-template and Trusted Advisor rows; replaced prose sources.

Method: documentation only; no commands were run.
