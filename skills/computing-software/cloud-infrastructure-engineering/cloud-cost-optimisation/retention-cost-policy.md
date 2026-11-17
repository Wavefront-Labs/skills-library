---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.retention-cost-policy
name: retention-cost-policy
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, finops-policy-governance, finops-governance, retention-policy, data-lifecycle, storage-cost-optimisation]
level: practitioner
status: draft
description: "Set data retention cost policy: retention classes per data type, legal and compliance minimums, default expiry for logs, backups and snapshots, and enforcement."
sources: ["https://www.finops.org/framework/capabilities/policy-governance/", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html", "https://learn.microsoft.com/en-us/azure/storage/blobs/lifecycle-management-overview"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Data retention cost policy

Storage grows silently: logs, snapshots, backups and old datasets are kept "just in case" and
billed forever. A retention policy turns "just in case" into an explicit, costed decision.

## Retention classes (example)
| Class | Examples | Hot | Archive | Delete after |
|---|---|---|---|---|
| Operational logs | app/debug logs | 14-30 days | none | 30 days |
| Security/audit logs | CloudTrail, sign-in logs | 90 days | 1-7 years | per regulation |
| Backups | DB backups, snapshots | 7-35 days | monthly copies 1 year | per RPO policy |
| Analytics raw | event landing zone | 90 days | 1-2 years | 2 years |
| Regulated records | financial, health | per law | per law | legal minimum |

## Steps
1. **Inventory** big storage consumers (object buckets, log analytics workspaces, snapshot counts,
   backup vaults) and their current retention, from the cost data grouped by usage type.
2. **Get the minimums** from legal/compliance (e.g. financial records, sector regulations); the
   policy sets defaults, legal holds override.
3. **Define classes and defaults**; a resource without a class tag gets the shortest default
   (opt-in to keep longer, not opt-out).
4. **Enforce in platform**: S3/Blob/GCS lifecycle rules, log group retention (CloudWatch Logs
   default is never-expire; set it), Log Analytics table retention, AWS Backup / Azure Backup
   policies, snapshot lifecycle (Amazon Data Lifecycle Manager).
5. **Guardrails**: policy-as-code checks (Cloud Custodian, AWS Config rule
   `cw-loggroup-retention-period-check`, Azure Policy) flag never-expire logs and untagged buckets.
6. **Report** storage growth and policy compliance monthly.

## Gotchas
- Archive tiers have minimum storage durations and retrieval fees; short-lived data should expire,
  not archive.
- Deleting data under legal hold is a serious incident; integrate legal-hold flags first.
- Versioned buckets keep noncurrent versions forever unless a noncurrent-version rule exists.

## Verify
- [ ] No log group or workspace table with unlimited retention outside approved exceptions.
- [ ] Storage growth rate falls after enforcement, and legal holds are untouched.
