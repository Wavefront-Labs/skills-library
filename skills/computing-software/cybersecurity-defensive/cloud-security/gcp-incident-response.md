---
id: computing-software.cybersecurity-defensive.cloud-security.gcp-incident-response
name: gcp-incident-response
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [gcp-incident-response, cloud-audit-logs, security-command-center, gce-forensics, service-account-key-compromise, cloud-incident-response]
level: advanced
status: draft
description: "Respond to incidents in Google Cloud: audit logs to query, SCC findings, containing compromised service accounts and VMs, disk snapshot forensics and org policy guardrails."
sources: ["https://cloud.google.com/logging/docs/audit", "https://cloud.google.com/security-command-center/docs/concepts-security-command-center-overview", "https://cloud.google.com/architecture/security-foundations/detective-controls", "https://cloud.google.com/compute/docs/disks/create-snapshots"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# GCP incident response

## Prepare
- Org-level aggregated log sink of Admin Activity, Data Access (enable for critical services), System Event and Policy Denied audit logs to a locked logging project (bucket retention lock / BigQuery).
- Security Command Center (Premium/Enterprise) with Event Threat Detection, Container Threat Detection, VM Threat Detection.
- Pre-provisioned IR group with `roles/iam.securityReviewer`, `roles/logging.privateLogViewer`, `roles/compute.instanceAdmin` in a break-glass process; forensic project.

## Investigate
```
gcloud logging read 'protoPayload.authenticationInfo.principalEmail="svc-app@proj.iam.gserviceaccount.com"
  AND timestamp>="2026-10-17T00:00:00Z"' --organization=123456789 --format=json
```
Key events: `google.iam.admin.v1.CreateServiceAccountKey`, `SetIamPolicy` (project/org), `compute.instances.insert` in unusual regions (mining), `storage.objects.get` bulk (Data Access logs), `GenerateAccessToken` (impersonation chains).

## Contain
| Scenario | Action |
|---|---|
| Service account key leaked | Disable key (`gcloud iam service-accounts keys disable`), then delete; review all actions by the SA; org policy `iam.disableServiceAccountKeyCreation` |
| Compromised user | Suspend in Workspace/Cloud Identity, revoke sessions and OAuth tokens, remove IAM bindings |
| Compromised VM | Firewall policy deny with secure tag / network tag "quarantine", remove SA from the instance (requires stop) or remove its IAM roles, snapshot disks |
| Rogue projects/resources | Org policy constraints (resource locations, VM external IP deny), quotas |

## Forensics
`gcloud compute snapshots create case123-disk --source-disk=vm1 --source-disk-zone=europe-west2-a` then
share to the forensic project; create a disk and attach read-only to an analysis VM. Serial port output and
guest attributes may hold evidence.

## Gotchas
- Data Access logs are off by default for most services - without them, data reads are invisible.
- Deleting a service account breaks forensics trails and dependent workloads; disable first.

## Verify
- [ ] Logging sink and retention lock confirmed.
- [ ] Tabletop of a leaked SA key exercised with the runbook.
