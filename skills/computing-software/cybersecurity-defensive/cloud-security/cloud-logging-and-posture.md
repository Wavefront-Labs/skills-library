---
id: computing-software.cybersecurity-defensive.cloud-security.cloud-logging-and-posture
name: cloud-logging-and-posture
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [cloud-security, aws, azure, gcp, cloudtrail, organization-trail, aws-config, guardduty, security-hub, azure-activity-log, entra-audit-logs, microsoft-defender-for-cloud, azure-policy, gcp-cloud-audit-logs, security-command-center, log-archive-account, cspm, cnapp, prowler, scoutsuite, cloud-detection, scp]
level: practitioner
status: draft
description: "Turn on org-wide audit logging in AWS, Azure and GCP into a locked log archive, add CSPM, and deploy the cloud detections that catch real attacks."
sources: ["AWS Security Reference Architecture and AWS CloudTrail User Guide - organization trails", "Microsoft Azure Monitor documentation - Activity Log and diagnostic settings", "Google Cloud Audit Logs documentation - aggregated sinks", "CIS Foundations Benchmarks for AWS, Azure and GCP"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cloud logging and posture — every account logged, every drift seen

**Goal:** make it impossible to create a cloud account/subscription/project that isn't
logged, store those logs where an attacker with admin in a workload account can't
delete them, and continuously check configuration against a baseline.

## 1. AWS
- **Organization trail** from the management (or delegated admin) account: all regions,
  management events read+write, delivered to an S3 bucket in a dedicated **Log
  Archive** account (AWS Control Tower sets this up). Enable log file validation,
  SSE-KMS, and S3 Object Lock (compliance mode) or at least a bucket policy denying
  `s3:DeleteObject` except a break-glass role.
- Data events (S3 object-level, Lambda) cost more — enable for sensitive buckets only.
- **SCP** denying `cloudtrail:StopLogging`, `DeleteTrail`, `UpdateTrail`,
  `guardduty:DeleteDetector`, `config:StopConfigurationRecorder` for everyone but a
  security role.
- Enable GuardDuty, AWS Config and Security Hub (CSPM; foundational best practices
  and CIS standards) with a delegated admin and auto-enable for new accounts.

## 2. Azure
- **Activity Log** is per subscription: use Azure Policy (`DeployIfNotExists`
  diagnostic settings) at the management group root to send it to a central Log
  Analytics workspace / Event Hub / storage in a security subscription.
- **Entra ID** sign-in and audit logs via tenant diagnostic settings (needs a P1/P2 licence for full retention/export).
- Resource logs (Key Vault, Storage, NSG flow / VNet flow logs) via the same policy approach.
- Microsoft Defender for Cloud: foundational CSPM is free; Defender CSPM and workload
  plans are paid. Lock the security subscription with resource locks and restricted RBAC.

## 3. GCP
- Admin Activity audit logs are always on; **Data Access** logs are off by default
  for most services — enable at org level for sensitive services (IAM, KMS, Storage).
- Create an **aggregated sink** at the organization (`--include-children`) to a
  BigQuery dataset or Cloud Storage bucket with a retention lock in a security project:
  `gcloud logging sinks create org-audit storage.googleapis.com/<BUCKET> --organization=<ORG_ID> --include-children --log-filter='logName:"cloudaudit.googleapis.com"'`
  then grant the sink's writer identity access to the bucket.
- Security Command Center (Standard/Premium/Enterprise tiers) for posture and threat detection.

## 4. Retention and SIEM
Keep at least 1 year searchable or restorable (check your regulatory requirement;
many choose 90 days hot + 1–7 years archive). Forward to the SIEM: CloudTrail via
S3 + SQS, Azure via Event Hub/native connectors, GCP via Pub/Sub.

## 5. CSPM
Run continuous posture checks against CIS Foundations Benchmarks (native tools above,
or open source Prowler / ScoutSuite / Steampipe, or a CNAPP). Prioritise:
public storage, internet-exposed management ports, root/global-admin usage and missing
MFA, over-privileged roles, unencrypted or public snapshots, disabled logging. Route
findings to account owners with SLAs; auto-remediate only safe cases.

## 6. Detections that matter
- Root user / break-glass sign-in (`userIdentity.type = Root`).
- Logging tampered: `StopLogging`, `DeleteTrail`, diagnostic setting deleted, sink deleted.
- New access keys for privileged users; `CreateUser` + `AttachUserPolicy` AdministratorAccess.
- `GetSecretValue` / Key Vault secret reads in bulk or from new principals.
- Snapshot or bucket made public / shared to an unknown account ID.
- Console login without MFA; sign-ins from unusual ASNs; impossible travel.
- Azure: role assignment Owner at subscription/MG scope; app registration given new credentials.
- GCP: `SetIamPolicy` granting `roles/owner` or to `allUsers`; service account key creation.

## Gotchas
- Logging accounts created *before* the org trail/policy existed — check every account, not just new ones.
- Global services (IAM, STS, CloudFront) log to us-east-1 in AWS; single-region trails miss them.
- Azure Activity Log does not include data-plane actions (e.g. blob reads); those are resource logs.
- An attacker with management-account admin can disable everything — protect it with
  phishing-resistant MFA, no workloads, minimal users.
- Cost surprises from data events or Data Access logs; scope first, then expand.

## Verify
- [ ] Every account/subscription/project appears in the central log store (count matches the org inventory).
- [ ] A workload-account admin cannot delete or alter archived logs (tested).
- [ ] Logging-disable actions are denied by SCP/policy and alert if attempted.
- [ ] CSPM runs continuously with findings routed to owners.
- [ ] Root/break-glass usage and logging-tamper detections fire in a test.
- [ ] Retention meets the documented requirement.

Related: computing-software.cybersecurity-defensive.splunk.spl-detection-searches
