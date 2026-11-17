---
id: computing-software.cloud-infrastructure-engineering.google-cloud.scc-custom-sha-and-etd-modules
name: scc-custom-sha-and-etd-modules
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, security-command-center, scc-custom-modules, custom-sha-modules, event-threat-detection, cel]
level: advanced
status: docs-checked
description: "Write Security Command Center custom Security Health Analytics modules in CEL and custom Event Threat Detection modules, test them, and roll them out at org or folder level."
sources: ["https://docs.cloud.google.com/security-command-center/docs/custom-modules-sha-overview", "https://docs.cloud.google.com/security-command-center/docs/custom-modules-sha-code", "https://docs.cloud.google.com/security-command-center/docs/custom-modules-etd-overview", "https://docs.cloud.google.com/sdk/gcloud/reference/scc/custom-modules/sha/create"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SCC custom SHA and ETD modules

The SCC docs mark the Enterprise tier as deprecated (shutting down 2027-05-21, organizations move to Premium): check your tier.

## 1. Custom Security Health Analytics module (posture)
`bucket-no-retention.yaml`:
```yaml
severity: MEDIUM
description: "Audit-log buckets must have a retention policy"
recommendation: "Set a retention policy of at least 365 days"
resource_selector:
  resource_types: [storage.googleapis.com/Bucket]
predicate:
  expression: >
    resource.name.contains("audit-") &&
    (!has(resource.retentionPolicy) || int(resource.retentionPolicy.retentionPeriod) < 31536000)
custom_output:
  properties:
  - name: retention_seconds
    value_expression: {expression: "has(resource.retentionPolicy) ? resource.retentionPolicy.retentionPeriod : '0'"}
```
```bash
gcloud scc custom-modules sha simulate --organization=<ORG> --custom-config-from-file=bucket-no-retention.yaml \
  --resource-from-file=sample-bucket.yaml          # test against a sample resource
gcloud scc custom-modules sha create --organization=<ORG> --display-name=bucket_audit_retention \
  --enablement-state=ENABLED --custom-config-from-file=bucket-no-retention.yaml
```
- `resource_selector` takes one to five resource types, each at most once; CEL properties must exist in the API definition of every selected type.
- A finding is created when the predicate resolves to TRUE.
- A new module is used after the next batch scan, which can take up to 24 hours.

## 2. Custom Event Threat Detection module (threats)
Template-based module types, e.g. `CONFIGURABLE_BAD_IP` (VPC flow logs, Firewall Rules logs) or
`CONFIGURABLE_ALLOWED_COMPUTE_ENGINE_REGION` (Admin Activity audit logs). Enabled modules run in real-time mode, scanning
whenever new logs are created, so the source logs must be enabled. The `gcloud scc custom-modules etd` commands are
alpha-track only (`--custom-config-from-file`): check `gcloud alpha scc custom-modules etd create --help` before use.

## Gotchas
- The default quota for creating custom SHA modules is 100 (increase on the Quotas page); prefer one module per control.
- Always simulate with a positive and a negative sample resource before creating the module.

## Verify
- [ ] Simulate returns a finding for the bad sample and none for the good; after the next scan the expected findings appear.

## Checked
2026-10-28. Confirmed against the SCC custom SHA overview and code pages, the ETD custom modules overview and the gcloud reference:
YAML fields, one to five resource types, TRUE triggers a finding, quota 100, up to 24 hours to first scan, ETD module types and real-time mode.
`etd create` flag was wrong (`--custom-config-file`) and the command is alpha only. Removed: 6-12 h scan interval, folder/project inheritance,
billing claim, ETD JSON example, `findings list` filter.
Method: documentation only; no commands were run.
