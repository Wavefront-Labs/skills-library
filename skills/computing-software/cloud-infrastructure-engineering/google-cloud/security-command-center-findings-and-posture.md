---
id: computing-software.cloud-infrastructure-engineering.google-cloud.security-command-center-findings-and-posture
name: security-command-center-findings-and-posture
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, security-command-center, scc, security-posture, security-health-analytics, event-threat-detection, container-threat-detection, vm-threat-detection, web-security-scanner, findings, mute-rules, notification-configs, scc-bigquery-export, posture-management, cspm, attack-path-simulation, scc-enterprise, cloud-security-scanner, compliance-dashboard]
level: advanced
status: docs-checked
description: "Operate Security Command Center at org level: tiers, finding triage, mute rules for accepted risk, Pub/Sub and BigQuery export, posture templates, attack-path scores."
sources: ["https://docs.cloud.google.com/security-command-center/docs/security-command-center-overview", "https://docs.cloud.google.com/security-command-center/docs/service-tiers", "https://docs.cloud.google.com/security-command-center/docs/security-posture-overview", "https://docs.cloud.google.com/security-command-center/docs/how-to-mute-findings", "https://docs.cloud.google.com/sdk/gcloud/reference/scc/muteconfigs/create", "https://securitycenter.googleapis.com/$discovery/rest?version=v1"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Security Command Center findings and posture

**Goal:** one queue of misconfigurations, vulnerabilities and threats across the org,
ranked by exploitability, routed to owners, with accepted risks muted on purpose and evidence exported.

## 1. Tiers and what turns on
- Tiers: Standard-legacy and Standard (basic security and compliance posture for Google Cloud), Premium (adds advanced posture management, attack paths, threat detection and compliance monitoring; activated at project or organisation level) and Enterprise (multicloud CNAPP).
- **The Enterprise tier is deprecated and shuts down on 21 May 2027**; organisations still on it move to Premium on or after that date. Plan for Premium, not Enterprise.
- Standard is free; Premium and Enterprise have their own pricing: see the SCC pricing page.
- Security Health Analytics is not supported for new Standard activations (a subset remains for organisations migrated from Standard-legacy).
- Services are built-in (for example Security Health Analytics, Event Threat Detection, Container Threat Detection, Virtual Machine Threat Detection, Web Security Scanner, attack path simulation), integrated (for example Cloud Armor, Sensitive Data Protection) or third party. The service tier comparison page lists which tier includes each service; check it rather than relying on a summary here.
- Activate at organisation level where you can: the Enterprise tier needs it, and some services need organisation-level activation. Activating only on single projects leaves the rest unmonitored.

## 2. Findings model
Fields on a finding: `category`, `severity` (CRITICAL, HIGH, MEDIUM, LOW), `findingClass` (THREAT, VULNERABILITY, MISCONFIGURATION, OBSERVATION, SCC_ERROR, POSTURE_VIOLATION, TOXIC_COMBINATION, SENSITIVE_DATA_RISK, CHOKEPOINT, EXTERNAL_EXPOSURE, SECRET), `state` (ACTIVE or INACTIVE), `mute` (MUTED, UNMUTED, UNDEFINED), `resourceName`, `sourceProperties`, `securityMarks` and `attackExposure` (which has a `score`).
```bash
gcloud scc findings list organizations/<ORG_ID> --source=- \
  --filter='state="ACTIVE" AND severity="CRITICAL" AND NOT mute="MUTED"' --page-size=50
gcloud scc findings set-mute <FINDING_ID> --organization=<ORG_ID> --source=<SOURCE_ID> --mute=MUTED   # one-off
```
Suggested triage order: THREAT findings, then TOXIC_COMBINATION or high attack exposure, then CRITICAL misconfigurations on internet-exposed resources, then the rest by owner.

## 3. Mute rules (accepted risk as code)
```bash
gcloud scc muteconfigs create accepted-public-assets --organization=<ORG_ID> \
  --description="Static site buckets are intentionally public (RISK-123)" \
  --filter='category="<CATEGORY>" AND resource.project_display_name="<PROJECT_DISPLAY_NAME>"'
```
`--type` is `static` (default) or `dynamic` and cannot be changed after creation; `--expiry-time` applies only to dynamic configs, and when it passes the config is removed from all findings it muted. With data residency enabled, mute configs live in the location you pick (`--location`, default `global`). Keep filters in version control with the risk-acceptance ID in the description and review them regularly. Never mute by severity alone.

## 4. Route and export
- **Notification config** to Pub/Sub: `gcloud scc notifications create crit-to-pubsub --organization=<ORG_ID> --pubsub-topic=projects/P/topics/scc --filter='severity="CRITICAL" AND state="ACTIVE"'`, then a subscriber (for example a Cloud Run service) forwards to chat or ticketing.
- **Continuous export to BigQuery**: `gcloud scc bqexports create scc-bq --organization=<ORG_ID> --dataset=projects/P/datasets/scc --filter='state="ACTIVE"'` for dashboards and audit evidence. One-time exports to Cloud Storage (JSON, JSONL or CSV) are also available; filters on data-residency-controlled properties are rejected for those.
- Security marks (`gcloud scc findings update-marks`) tag findings or assets with ownership or ticket IDs.

## 5. Posture and exposure
- **Security posture**: deploy a posture at organisation, folder or project level. A posture is a set of policy sets of preventative (organisation policy) and detective (Security Health Analytics detectors, including custom modules) policies, and drift from it is surfaced. Predefined templates include `secure_by_default_essential`, `secure_by_default_extended`, `secure_ai_essential`, `big_query_essential`, `cloud_storage_essential`, `vpc_networking_essential`, `cis_2_0` and `nist_800_53`; "extended" templates must be customised before deployment. Commands: `gcloud scc postures create` and `gcloud scc posture-deployments create`.
- **Attack path simulation** assigns each finding an attack exposure `score` (state `CALCULATED` or `NOT_CALCULATED`) based on paths to your high-value resources, which you define with resource value configs. Sort by score to fix what matters first.

## Gotchas
- The Enterprise shutdown date above is the main planning risk; confirm your tier on the overview page.
- Which detectors a tier includes changes over time: re-read the service tier comparison before promising coverage.
- Export findings to BigQuery before any tier change.

## Verify
- [ ] The Findings page shows detectors enabled at organisation level and new projects inherit within a day.
- [ ] Create a public bucket in a sandbox: a finding appears, a Pub/Sub message arrives, and the finding goes INACTIVE after the fix.
- [ ] A mute rule hides the accepted finding from the default view; it remains queryable with `mute="MUTED"`.
- [ ] The BigQuery export has current rows.

## Checked
2026-10-28. Confirmed against the SCC overview and service tier pages (tier descriptions, Enterprise deprecation and 21 May 2027 shutdown, Standard free, SHA note, activation levels), the posture overview (policy sets, template names, extended-template customisation), the gcloud references for `muteconfigs create`, `bqexports create` and `notifications create` (flags, `--type` values, expiry behaviour, location), the one-time export page, and the SCC v1 discovery document (`Finding` fields and enums, `AttackExposure.score`/`state`). Removed: the per-tier feature table (the fetched table loses its tier columns, so it is not checkable), IAM role names for responders, sample category names, scan frequency, history deletion, form-submission and detector-specific log dependencies, and the compliance benchmark list.
Method: documentation only; no commands were run.
