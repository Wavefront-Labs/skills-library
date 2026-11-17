---
id: computing-software.cybersecurity-defensive.security-operations.cloud-control-plane-hunting
name: cloud-control-plane-hunting
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [cloud-hunting, threat-hunting, cloudtrail, azure-activity-log, gcp-audit-logs, cloud-security, iam]
level: advanced
status: docs-checked
description: "Hunt cloud control planes (AWS CloudTrail, Azure Activity and Entra audit, GCP Audit Logs) for persistence, privilege escalation, defence evasion and data access."
sources: ["https://attack.mitre.org/matrices/enterprise/cloud/", "https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-concepts.html", "https://learn.microsoft.com/en-us/azure/azure-monitor/fundamentals/activity-log-schema", "https://learn.microsoft.com/en-us/entra/identity/monitoring-health/reference-audit-activities", "https://docs.cloud.google.com/logging/docs/audit", "https://docs.cloud.google.com/iam/docs/reference/rest/v1/projects.serviceAccounts.keys/create"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Cloud control-plane hunting

The control plane is the set of management operations on cloud resources. In AWS, CloudTrail management events are those operations ("control plane operations"); data events are resource operations such as S3 object reads and are "data plane". The hypotheses below are analyst heuristics; the API operation names were checked against the AWS service models.

## Hypotheses (AWS examples)
1. **Persistence via new credentials**: IAM `CreateAccessKey`, `CreateLoginProfile`, `UpdateAssumeRolePolicy` (trust added for an outside account), new users, `CreateRole` whose `AssumeRolePolicyDocument` trusts an unknown principal.
2. **Privilege escalation**: `AttachUserPolicy` or `PutUserPolicy` granting broad permissions, `CreatePolicyVersion` with `SetAsDefault` true. Pass-role abuse is an IAM permission rather than an API call, so hunt for the resources created with the role (new function or instance) instead.
3. **Defence evasion**: CloudTrail `StopLogging`, `DeleteTrail`, `PutEventSelectors` that narrow what is logged; GuardDuty `DeleteDetector`; Security Hub `DisableSecurityHub`.
4. **Discovery bursts**: many read-style calls from one principal in a short time, especially with access-denied errors (enumeration with stolen keys).
5. **Data access**: volume spikes of S3 `GetObject` (needs data events), Secrets Manager `GetSecretValue` from new principals, EC2 `ModifySnapshotAttribute` adding `createVolumePermission` for another account.
6. **Unusual geography, network or user agent** for long-lived keys.

## Azure and Entra
- Azure Activity Log: events carry a `category` (the Administrative category covers control-plane operations), the `caller` (user UPN or service principal) and an `operationName`. The schema "isn't strictly enforced across all data sources", so expect variations across tenants.
- Entra audit log activities worth alerting on include "Add service principal credentials", "Add app role assignment to service principal" and "Consent to application".

## GCP
- Admin Activity audit logs record user-driven calls that modify configuration, such as creating VM instances or changing IAM permissions; they are always written and cannot be disabled or excluded. Data Access audit logs cover reads of configuration and user data, and are stored in the `_Default` bucket unless routed elsewhere; the Logs Viewer role alone cannot see them there (Private Logs Viewer can).
- Hunt for IAM policy changes (`SetIamPolicy`) that add outside members and for service account key creation (the IAM `projects.serviceAccounts.keys.create` method).

## Method
Baseline principal behaviour (count by principal and API), review rare combinations, check against change records, and convert confirmed patterns into detections. Set thresholds from your own baseline.

## Gotchas
- CloudTrail trails and event data stores log management events by default, not data events or Insights events; data events are not logged by default and you must add each resource type explicitly (they carry extra charges). Know what you lack before concluding something did not happen.
- An organization trail delivers events for the management account and all member accounts to one S3 bucket, CloudWatch Logs and EventBridge, giving one logging strategy; put its destination in a security account.

## Verify
Hunt report: hypotheses, queries, time range, accounts covered, findings, and new detections created.

## Checked
2026-11-08. Confirmed: CloudTrail concepts page (management vs data events, defaults, organization trails); AWS service models via botocore for `CreateAccessKey`, `CreateLoginProfile`, `UpdateAssumeRolePolicy`, `CreateRole`, `AttachUserPolicy`, `PutUserPolicy`, `CreatePolicyVersion` (`SetAsDefault`), `StopLogging`, `DeleteTrail`, `PutEventSelectors`, `DeleteDetector`, `DisableSecurityHub`, `GetSecretValue`, `ModifySnapshotAttribute` (`createVolumePermission`); the Azure Activity Log schema page (category, caller, operationName, schema caveat); the Entra audit activities page (the three activities named); the GCP audit logs page (Admin Activity and Data Access behaviour) and the IAM `serviceAccounts.keys.create` reference. Removed as unconfirmed: the Athena SQL example (table and column names), the `*:*` policy claim, VPC flow log deletion, Azure `roleAssignments/write`, `listKeys`, Key Vault read and diagnostic-setting operation names, the GCP `google.iam.admin.v1.CreateServiceAccountKey` audit method name and logging-sink deletion, and the "attacker cannot delete" claim for organization trails. The MITRE cloud matrix page was read as background only.
Method: documentation only; no commands were run.
