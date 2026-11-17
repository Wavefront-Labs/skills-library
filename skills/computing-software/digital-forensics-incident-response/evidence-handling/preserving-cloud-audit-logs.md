---
id: computing-software.digital-forensics-incident-response.evidence-handling.preserving-cloud-audit-logs
name: preserving-cloud-audit-logs
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [cloud-log-preservation, cloudtrail, cloud-evidence, log-export, legal-hold, dfir]
level: practitioner
status: docs-checked
description: "Preserve cloud audit logs as evidence: CloudTrail log file integrity validation, Entra diagnostic settings endpoints, and Google Cloud log sinks, with custody records."
sources: ["https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-log-file-validation-intro.html", "https://learn.microsoft.com/en-us/entra/identity/monitoring-health/concept-diagnostic-settings-logs-options", "https://cloud.google.com/logging/docs/export/configure_export_v2"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Preserving cloud audit logs

**Goal:** copy the relevant cloud logs into controlled, integrity-protected storage early in the
incident. Look up current retention for each source in the provider's own documentation; the
cited pages do not state retention periods.

## AWS CloudTrail: integrity validation
- Log file integrity validation uses SHA-256 hashing and SHA-256 with RSA signing, so modifying,
  deleting or forging log files without detection is computationally infeasible.
- With validation enabled, CloudTrail hashes every delivered log file and each hour delivers a
  signed digest file that references the last hour's files and their hashes. Each digest holds the
  signature of the previous digest. Digests go to the same S3 bucket, in a folder separate from
  the logs; key pairs differ per Region.
- Enabling it only makes CloudTrail deliver digests; it does not validate anything. Validate
  afterwards with the AWS CLI (works where CloudTrail delivered the files) or your own tooling if
  you moved the logs elsewhere.
- Validation can also assert that no log files were delivered in a given period.
- Store logs and digests in S3 or Glacier for as long as needed; S3 MFA Delete can harden the
  digest files.

## Microsoft Entra: diagnostic settings
- Diagnostic settings route activity logs to endpoints for long-term retention: a Log Analytics
  workspace, a storage account, an event hub, or a partner solution. Creating or editing a
  setting needs a Security Administrator for the tenant.
- Categories include AuditLogs (changes to applications, groups, users, licences), SignInLogs
  (interactive), NonInteractiveUserSignInLogs, ServicePrincipalSignInLogs,
  ManagedIdentitySignInLogs, ProvisioningLogs, RiskyUsers, UserRiskEvents and
  MicrosoftGraphActivityLogs (all HTTP requests to tenant resources via Graph, useful to trace
  a compromised account; route them to the same workspace as SignInLogs to cross-reference).
- Custom security attribute audit logs need the Attribute Log Reader role to view, and Attribute
  Log Administrator plus Security Administrator to route.

## Google Cloud: log sinks
- A sink routes matching log entries to a destination: a log bucket, a BigQuery dataset, a Cloud
  Storage bucket (long-term storage, stored as JSON files), or another project. Sinks belong to a
  project, folder, organisation or billing account; aggregated sinks cover children.
- Sinks need authorisation to write to the destination (automatic for a log bucket in the same
  project; otherwise a service account with the required permissions). Creating a sink needs
  Logs Configuration Writer.
- New sinks to Cloud Storage can take several hours to start routing; they are processed hourly.
- The `_Default` sink does not route Admin Activity or System Event entries; those go to
  `_Required`.
- BigQuery destinations must be write-enabled, not a linked dataset.

## Integrity and custody
Hash each exported file; record the query or setting, time range, account and tool version; store
read-only. Prefer provider-native integrity (CloudTrail digest files) where available.

## Verify
CloudTrail validation reports the files valid; the sink or diagnostic setting shows data arriving
at the destination.

## Checked

Date 2026-11-08. Pages read in full: CloudTrail log file integrity validation intro, Entra diagnostic settings log options, Google Cloud configure sinks (grepped for destinations, limits and roles in the 43k-character page, not read line by line). Removed as not on the pages: the default retention table (all rows), `aws cloudtrail validate-logs` syntax, Graph endpoints, `Search-UnifiedAuditLog` limits, `gcloud logging read`, Workspace Admin SDK, the Object Lock advice, and the filtering and truncation gotchas.

Method: docs-only read of cited pages, 2026-11-08
