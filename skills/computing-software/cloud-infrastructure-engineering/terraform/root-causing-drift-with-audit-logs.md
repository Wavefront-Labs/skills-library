---
id: computing-software.cloud-infrastructure-engineering.terraform.root-causing-drift-with-audit-logs
name: root-causing-drift-with-audit-logs
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, drift-root-cause, cloudtrail-drift, drift-detection, azure-activity-log, gcp-audit-logs]
level: practitioner
status: docs-checked
description: "Find who or what changed a Terraform-managed resource out of band using CloudTrail, Azure Activity Log or GCP Audit Logs, then fix the process, not just the diff."
sources: ["https://docs.aws.amazon.com/awscloudtrail/latest/userguide/view-cloudtrail-events-cli.html", "https://learn.microsoft.com/en-us/azure/azure-monitor/essentials/activity-log", "https://cloud.google.com/logging/docs/audit"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Root-causing drift

A drift alert tells you **what** differs. Before reverting or accepting, find **who**
and **why**; otherwise it recurs.

## 1. Pin down the object and time window
From the refresh-only plan: address, cloud ID, attribute. Time window = last clean
plan to the drift detection.

## 2. Query audit logs
**AWS CloudTrail** (`lookup-events` covers management events from the last 90 days in the current Region):
```bash
aws cloudtrail lookup-events --region eu-west-1 \
  --lookup-attributes AttributeKey=ResourceName,AttributeValue=sg-0abc123 \
  --start-time 2026-10-17T00:00Z --max-results 50 \
  --query 'Events[].{t:EventTime,n:EventName,u:Username}' --output table
```
Only one lookup attribute (key/value pair) is allowed per call; `ResourceName` is a valid
key. Open the event's `userIdentity` (`type`, `arn`, `sessionContext`) to see whether it was
a human role session, another pipeline's role, or an AWS service.

**Azure Activity Log** (events are retained 90 days unless you add a diagnostic setting):
```bash
az monitor activity-log list --resource-id <id> --start-time 2026-10-17T00:00:00Z
```
Read the caller and operation in the returned events.
**GCP Cloud Audit Logs**:
```bash
gcloud logging read 'protoPayload.resourceName:"instances/web-1" AND logName:"cloudaudit.googleapis.com%2Factivity"' \
  --freshness=2d --format='table(timestamp,protoPayload.methodName,protoPayload.authenticationInfo)'
```
Admin Activity audit logs (`cloudaudit.googleapis.com%2Factivity`) record API calls that
modify resource configuration and are always written.

## 3. Classify and fix the cause
| Who | Typical fix |
|---|---|
| Human in console | SCP/permission guardrails, break-glass process, codify the change |
| Another IaC stack / pipeline | Resolve double ownership; one stack owns the object |
| Cloud service (autoscaling, managed tags) | `lifecycle { ignore_changes = [...] }` on that attribute, for values that change after creation and should not affect the resource |
| Policy/remediation tool (Config rules, Azure Policy modify, security tooling) | Make Terraform config compliant so remediation is a no-op |
| Kubernetes controller/operator | Do not manage controller-owned fields in Terraform |

## 4. Then reconcile
Revert (normal apply) or accept (code change + `terraform plan -refresh-only`, Terraform
0.15.4 or later), referencing the audit evidence in the PR.

## Verify
- [ ] Actor and mechanism identified for each drifted attribute.
- [ ] Preventive change in place; next scheduled check is clean.

## Checked
- 2026-10-28. Confirmed against the AWS CloudTrail CLI page (`lookup-events`, 90 days, `--lookup-attributes` with one pair and `ResourceName`, `--start-time`), the CloudTrail userIdentity reference (`arn`, `sessionContext`, `AssumedRole`), the Azure Activity Log page (90-day retention, `az monitor activity-log list`), Google Cloud audit log docs (Admin Activity logs, `cloudaudit.googleapis.com%2Factivity`, `protoPayload.methodName`, `resourceName`, `authenticationInfo`), the Terraform lifecycle page (`ignore_changes`) and the plan page (`-refresh-only`), plus the command checker for all three CLI commands.
- Removed: service principal names such as `autoscaling.amazonaws.com`, the Azure `--query` field names and the `principalEmail` field (not in the fetched docs).
Method: documentation only; no commands were run.
