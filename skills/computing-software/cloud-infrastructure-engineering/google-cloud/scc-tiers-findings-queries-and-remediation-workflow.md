---
id: computing-software.cloud-infrastructure-engineering.google-cloud.scc-tiers-findings-queries-and-remediation-workflow
name: scc-tiers-findings-queries-and-remediation-workflow
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, security-command-center, scc-tiers, scc-activation, gcloud-scc-findings, scc-findings-api, scc-remediation, finding-remediation, mute-rules, notifications]
level: practitioner
status: docs-checked
description: "Choose and activate a Security Command Center tier, query findings with gcloud scc, mute noise with rules, stream findings to Pub/Sub and run a ticketed remediation workflow."
sources: ["https://docs.cloud.google.com/security-command-center/docs/service-tiers", "https://docs.cloud.google.com/security-command-center/docs/how-to-api-list-findings", "https://docs.cloud.google.com/security-command-center/docs/how-to-notifications", "https://securitycenter.googleapis.com/$discovery/rest?version=v2"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SCC: tiers, findings queries and remediation workflow

## 1. Tier
| Tier | Adds |
|---|---|
| Standard | Basic security and compliance posture management for Google Cloud only; no extra charge. Organization-level activation. |
| Premium | Everything in Standard plus advanced posture management, attack paths, threat detection and compliance monitoring, Google Cloud only. Project or organization activation. |
| Enterprise (deprecated) | Multi-cloud CNAPP (Google Cloud, AWS, Azure); shuts down 2027-05-21, when organizations move to Premium. Organization-level activation only. |
Security Health Analytics is not supported with new Standard-tier activations. See the service-tiers page for the full service-by-tier
table and the pricing page for costs.

## 2. Query findings
```bash
gcloud scc findings list organizations/<ORG_ID> --location=global \
  --filter='state="ACTIVE" AND mute!="MUTED" AND (severity="CRITICAL" OR severity="HIGH")' \
  --format='table(finding.category,finding.resourceName,finding.severity,finding.eventTime)'
gcloud scc findings list organizations/<ORG_ID> --location=global \
  --filter='category="PUBLIC_BUCKET_ACL" AND state="ACTIVE"' --format=json
```
Group by category and project for triage and route findings to resource owners.

## 3. Reduce noise
```bash
gcloud scc muteconfigs create mute-sandbox --organization=<ORG_ID> --location=global \
  --description="low severity noise" \
  --filter='severity="LOW"' --type=dynamic
```
A mute config has a `type` (`STATIC` or `DYNAMIC`), a `filter` and an optional `expiryTime`. Mute by scope and category with a
reason; never mute CRITICAL broadly. Use the mute-findings docs for the filter fields that scope a rule to a folder or project.

## 4. Stream and remediate
```bash
gcloud scc notifications create high-findings --organization=<ORG_ID> --location=global \
  --pubsub-topic=projects/<SEC_P>/topics/scc-high --filter='state="ACTIVE" AND (severity="HIGH" OR severity="CRITICAL")'
```
Subscriber (for example a Cloud Run function) creates or updates a ticket in the owning team's queue with the finding
name, resource and remediation text (`nextSteps`), with an SLA by severity agreed with the owners. Finding `state` is `ACTIVE`
or `INACTIVE`; severity values are `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`; `mute` is `MUTED`, `UNMUTED` or `UNDEFINED`.
Auto-remediate only safe classes.

## Gotchas
- Make ticket creation idempotent on the finding name.
- Use `--location` consistently with your activation (data residency).

## Verify
- [ ] Open HIGH/CRITICAL count and mean time to remediate reported weekly.
- [ ] A test public bucket produces a ticket.

## Checked
2026-10-28. Confirmed against the SCC service-tiers page and the Security Command Center API v2 discovery document (Finding `state`, `mute`,
`severity`, `nextSteps`; MuteConfig `type`, `filter`, `expiryTime`). Commands verified against the gcloud reference. Removed: per-tier service
lists not on the tiers page, SLA hours, folder-scoped mute filter, `findings update --state` command, dedup/notification-behaviour gotchas.
Method: documentation only; no commands were run.
