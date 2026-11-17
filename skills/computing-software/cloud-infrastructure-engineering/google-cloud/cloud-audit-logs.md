---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cloud-audit-logs
name: cloud-audit-logs
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-audit-logs, audit-logs, audit-logging, admin-activity-logs, data-access-logs, system-event-logs, policy-denied-logs, access-transparency, log-exemptions, auditconfig, protopayload, log-retention, compliance-logging, who-did-what]
level: practitioner
status: docs-checked
description: "Configure and read Cloud Audit Logs: enable Data Access logs org-wide with exemptions, rely on Admin Activity for compliance, and write queries that answer who changed what."
sources: ["https://cloud.google.com/logging/docs/audit", "https://cloud.google.com/logging/docs/audit/configure-data-access", "https://cloud.google.com/logging/docs/audit/understanding-audit-logs", "https://cloud.google.com/logging/quotas", "https://raw.githubusercontent.com/googleapis/googleapis/master/google/cloud/audit/audit_log.proto"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud Audit Logs

**Goal:** every control-plane change and every sensitive data read is recorded, retained
long enough for your compliance regime, and findable in under a minute.

## 1. The four log types
| Type | Log name suffix | Default |
|---|---|---|
| Admin Activity | `cloudaudit.googleapis.com%2Factivity` | always on, cannot disable |
| System Event | `.../system_event` | always on, cannot disable |
| Policy Denied | `.../policy` | on by default; cannot be disabled, but exclusion filters can stop it being stored; storage is charged |
| Data Access | `.../data_access` | **off** except some BigQuery services; enabling may incur extra log charges |

Data Access has three sub-types: `ADMIN_READ`, `DATA_READ`, `DATA_WRITE`. Admin Activity
already covers *writes* to config; Data Access covers reads of metadata/data and user-data writes.

## 2. Enable Data Access logs at org level
Edit the org IAM policy's `auditConfigs` (console: IAM → Audit Logs, or `gcloud`):
```bash
gcloud organizations get-iam-policy <ORG_ID> --format=yaml > policy.yaml
# add:
# auditConfigs:
# - service: allServices
#   auditLogConfigs:
#   - logType: ADMIN_READ
#   - logType: DATA_WRITE
#   - logType: DATA_READ
#     exemptedMembers: [serviceAccount:noisy-pipeline@<PROJECT>.iam.gserviceaccount.com]
gcloud organizations set-iam-policy <ORG_ID> policy.yaml
```
- Data Access volume can be large. Start with `ADMIN_READ` + `DATA_WRITE` everywhere and add
  `DATA_READ` only for services holding regulated data.
- Per-project config is the **union** with the org (and `allServices` with a per-service entry);
  a project cannot switch off what the org turned on.
- Exempt high-volume service accounts with `exemptedMembers` rather than disabling a service.

## 3. Reading an entry
`protoPayload` fields that matter (AuditLog proto):
- `authenticationInfo.principalEmail` — who; `serviceAccountDelegationInfo` shows impersonation chains.
- `authorizationInfo[].permission` and `.granted` — what was checked and whether it passed.
- `methodName`, `resourceName`, `request`, `response`.
- `requestMetadata.callerIp`, `requestMetadata.callerSuppliedUserAgent` — client tool.
- `status.code` is a `google.rpc.Status` code; non-zero is a failure.

## 4. Queries
Method names differ per service: copy them from a sample entry or the service's audit-log page.
```
# Admin Activity for one method
logName:"cloudaudit.googleapis.com%2Factivity"
protoPayload.methodName="<METHOD>"

# Data Access for one service
logName:"data_access" protoPayload.serviceName="<SERVICE>.googleapis.com"

# Policy Denied
logName:"cloudaudit.googleapis.com%2Fpolicy"
```
Use an org-level **aggregated sink** (`--include-children`) to a central log bucket so queries
cover every project; see `security-log-sinks-and-siem-export`.

## 5. Retention
The `_Default` bucket keeps 30 days (configurable 1 to 3650); `_Required` keeps Admin Activity and
System Event for 400 days, not configurable. For longer or for Data Access: route to a custom log
bucket with `--retention-days=<N>` and **lock** it (`gcloud logging buckets update --locked`).

## Gotchas
- Audit logs record the *API* call, so a Terraform apply shows the Terraform service account, not the engineer; use impersonation so `serviceAccountDelegationInfo` shows the human.
- Access Transparency provides logs of actions by Google Cloud staff on your content; it is separate from audit logs.
- A log entry is limited to 256 KiB (Logging quotas page).

## Verify
- [ ] `gcloud organizations get-iam-policy` shows the intended `auditConfigs` and new projects inherit them.
- [ ] Reading a test secret produces a `data_access` entry with your principal.
- [ ] A locked bucket refuses `gcloud logging buckets delete`.

## Checked
2026-10-28. Confirmed against the Cloud Audit Logs overview, Configure Data Access audit logs, the Logging quotas page and the audit_log.proto in googleapis: log types and defaults, union merge behaviour, `exemptedMembers`, AuditLog field names, the 256 KiB entry limit, `_Required` 400 days and the 1 to 3650 day bucket range. gcloud commands checked against the reference with check_commands.py. Removed: billable column, cost claims, example method names, the VPC-SC `violationReason` query, the Access Transparency log name and support-plan claim, truncation claim, Bucket Lock alternative.
Method: documentation only; no commands were run.
