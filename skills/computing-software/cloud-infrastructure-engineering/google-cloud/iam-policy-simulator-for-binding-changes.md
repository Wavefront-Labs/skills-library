---
id: computing-software.cloud-infrastructure-engineering.google-cloud.iam-policy-simulator-for-binding-changes
name: iam-policy-simulator-for-binding-changes
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, iam, iam-policy-simulator, simulate-iam-policy, policy-simulator, policy-intelligence, access-change-preview, replay-access-logs, gcloud-policy-intelligence-simulate, iam-change-safety, pre-change-check]
level: practitioner
status: docs-checked
description: "Preview the impact of an IAM allow-policy change with Policy Simulator: replay 90 days of access logs against the proposed policy and read the access changes first."
sources: ["https://cloud.google.com/policy-intelligence/docs/iam-simulator-overview", "https://cloud.google.com/policy-intelligence/docs/troubleshoot-access", "https://policysimulator.googleapis.com/$discovery/rest?version=v1"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IAM Policy Simulator for binding changes

**Goal:** before removing Editor from a service account or tightening a folder policy, know
exactly which real requests from the past 90 days would start failing.

## 1. What it does
Policy Simulator takes a **proposed allow policy** for any resource that accepts allow policies and replays the access
attempts from the last 90 days in the access logs of the nearest project or organisation, once with the current and
once with the proposed policy, taking inherited and descendant allow policies into account. It reports the differences as
access changes (API enum `accessChange`: `NO_CHANGE`, `UNKNOWN_CHANGE`, `ACCESS_REVOKED`, `ACCESS_GAINED`,
`ACCESS_MAYBE_REVOKED`, `ACCESS_MAYBE_GAINED`). It only evaluates allow policies; deny, organisation-policy and
principal-access-boundary changes have their own simulators.

Results are unknown when the caller cannot read role details, the policies involved or group membership, or when a binding
uses a condition (Policy Simulator does not support conditions).

## 2. Run it with gcloud
```bash
gcloud projects get-iam-policy <PROJECT_ID> --format=json > current.json
# edit to the proposed state → proposed.json (e.g. remove roles/editor from the SA)
```
The gcloud reference documents `gcloud policy-intelligence simulate` only for organisation policies
(`simulate orgpolicy`), so run the allow-policy simulation from the console or the REST API:
`POST v1/{parent}/replays` on `policysimulator.googleapis.com` (parent `projects|folders|organizations/<ID>/locations/global`) returns a
long-running operation; `replays.get` reads the result, and each Replay is kept at least 7 days. Pay attention to
`ACCESS_MAYBE_REVOKED`: the principal's access under one of the two policies is unknown.

## 3. Use it in the change workflow
1. Export current policy, produce proposed policy from the IAM-as-code repo (`terraform plan` output → policy JSON for the resource).
2. Simulate; attach `report.json` summary (counts by principal) to the PR.
3. Any `ACCESS_REVOKED` for a service account = a workload that will break; add the granular replacement role, re-simulate until only intended revocations remain.
4. Apply in business hours; keep `current.json` as the rollback copy.

## 4. Limits worth knowing
- 90-day window; quarterly/annual jobs are invisible — check their logs separately.
- A simulation replays at most 5,000 access logs; with more in the window the simulation fails.
- Supported resource types are limited (Cloud Storage buckets, Pub/Sub snapshots/subscriptions/topics, Cloud SQL, Spanner, Compute Engine instances, and Resource Manager folders/organizations/projects at the time of reading); permissions of unsupported types are listed but not simulated.
- Not a replacement for Policy Troubleshooter (which explains *why* one access is denied now).

## Gotchas
- Each Replay is available for at least 7 days; store the report yourself.
- Credential Access Boundary downscoped tokens are not evaluated against changes to the token broker's permissions.

## Verify
- [ ] Simulation report attached to the IAM change PR with zero unexpected `ACCESS_REVOKED`.
- [ ] After applying, 48 h of logs show no `PERMISSION_DENIED` for principals the report cleared.
- [ ] Rollback policy file stored next to the applied one.

## Checked

- Date: 2026-10-27
- Confirmed against the Policy Simulator for allow policies overview (90-day replay, allow policies only, result types and unknown reasons, 5,000-log maximum, supported resource types, Credential Access Boundary note), the Policy Simulator API v1 discovery document (`replays.create`/`replays.get`, parent pattern, `accessChange` enum, replays kept at least 7 days), and the gcloud `policy-intelligence simulate` reference (organisation policies only).
- Removed: the `gcloud policy-intelligence simulate iam policy` command (not in the gcloud reference; the group page says simulate is for organisation policies), the `jq` filter, the permission and role names, the "Data Access logs must be enabled" and full-policy/etag/service-agent claims, and the dead source URLs.

Method: documentation only; no commands were run.
