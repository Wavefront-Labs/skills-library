---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.audit-logging
name: audit-logging
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, detection-and-response, audit-logging, cloudtrail-organization-trail, activity-log, cloud-audit-logs, data-events, log-integrity, object-lock, tamper-evident-logs, log-archive-account]
level: practitioner
status: docs-checked
description: "Build a tamper-evident cloud audit trail: org-wide control-plane logs, selective data-plane logging, integrity validation, protected archive and access separation."
sources: ["https://docs.aws.amazon.com/awscloudtrail/latest/userguide/creating-trail-organization.html", "https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-log-file-validation-intro.html", "https://learn.microsoft.com/azure/azure-monitor/essentials/activity-log", "https://cloud.google.com/logging/docs/audit"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tamper-evident audit trail

## Steps
1. **Org-wide control-plane logging**:
   - AWS: an organization trail, created from the management account or a delegated
     administrator, logs events for the management account and all member accounts. Member
     accounts see the trail but cannot delete it, turn logging on or off or change event types.
     A multi-Region trail is created in each enabled Region of each member account. Enable
     **log file integrity validation**: CloudTrail hashes every log file (SHA-256) and delivers
     an hourly signed digest file (SHA-256 with RSA) to the trail's S3 bucket, using different key
     pairs per Region. Enabling it does not itself validate anything; run validation with the AWS CLI.
   - Azure: the activity log is kept for 90 days at no charge; create a diagnostic setting to
     send entries elsewhere for longer retention. Resource logs (data plane operations such as
     reading a Key Vault secret) are not collected by default and need a diagnostic setting.
   - GCP: Admin Activity and System Event audit logs are always written and cannot be disabled
     or excluded; Data Access audit logs must be enabled (they are stored in the `_Default`
     bucket unless routed elsewhere). Route org, folder or billing-account logs with aggregated sinks.
     Audit log entries written by Cloud Audit Logs are immutable.
2. **Data events selectively**: enable data-plane logging (Azure resource logs, GCP Data Access
   logs) where the data is sensitive; Google notes Data Access logs help its Customer Care
   troubleshoot, so it recommends keeping them enabled.
3. **Protect the archive**: store CloudTrail logs and digest files in S3 or Glacier; use S3 MFA
   Delete to harden digest files.
4. **Separation of duties**: restrict who can read the sensitive logs, for example the GCP
   Private Logs Viewer role is needed for Data Access logs, which the Logs Viewer role cannot read.
5. **Retention**: set per your regulation; check each provider's retention page (see the
   Google Logging retention periods page and the Azure diagnostic settings page).

## Verify
- [ ] New account automatically included in org trail/sink.
- [ ] CloudTrail integrity validation via the AWS CLI passes for a sample period.
- [ ] A member-account admin cannot stop or delete the organization trail.

## Checked
2026-11-08. Confirmed against the four cited pages: CloudTrail organization trail behaviour, log file integrity validation (SHA-256, SHA-256 with RSA, hourly digest, per-Region keys, MFA Delete, S3 or Glacier storage), Azure activity log (90 days, diagnostic setting, resource logs not default) and Google Cloud Audit Logs (Admin Activity and System Event always written, Data Access _Default bucket, immutable entries, viewer roles, aggregated sinks). Removed: CloudTrail Lake, Entra ID log destinations, Object Lock compliance mode, SCP and Azure Policy deny rules, retention figures (1 year / 7 years), data event types and costs.
Method: documentation only; no commands were run.
