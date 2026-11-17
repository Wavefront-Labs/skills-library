---
id: computing-software.cybersecurity-defensive.cloud-security.gcp-organization-policies
name: gcp-organization-policies
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [iam-least-privilege, gcp-org-policy, organization-policy-constraints, domain-restricted-sharing, service-account-key-restriction, gcp-iam]
level: advanced
status: docs-checked
description: "Harden Google Cloud with organization policy constraints: block service account keys, Cloud SQL public IPs, default networks, enforce OS Login, with dry-run and tag exceptions."
sources: ["https://cloud.google.com/resource-manager/docs/organization-policy/overview", "https://cloud.google.com/resource-manager/docs/organization-policy/org-policy-constraints", "https://cloud.google.com/resource-manager/docs/organization-policy/dry-run-policy"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GCP organization policies

**Goal:** guardrails at the organization/folder level that prevent risky configurations regardless of project-level IAM.
An organization policy holds rules that say how and whether a constraint is enforced; rules can be conditional on
resource tags (for example enforce only on resources tagged `environment=development`).

## Baseline constraints (effects as documented)
| Constraint | Effect |
|---|---|
| `iam.disableServiceAccountKeyCreation` | Disables creation of service account external keys and Cloud Storage HMAC keys; part of the Google Cloud security baseline |
| `iam.managed.disableServiceAccountKeyCreation` | Blocks service account key creation (managed constraint form) |
| `iam.disableServiceAccountKeyUpload` | Disables uploading public keys to service accounts; part of the security baseline |
| `sql.restrictPublicIp` | Restricts Public IP on Cloud SQL instances; not retroactive for instances that already have it |
| `compute.requireOsLogin` | Enables OS Login on newly created projects and prevents metadata updates that disable it |
| `compute.skipDefaultNetworkCreation` | Skips creating the default network when a project is created |

Other constraints exist for domain-restricted sharing (`iam.allowedPolicyMemberDomains`), external IPs on
VMs (`compute.vmExternalIpAccess`), storage public access and resource locations; read each constraint's entry in
the constraints reference before enforcing.

## Apply
```
gcloud resource-manager org-policies enable-enforce iam.disableServiceAccountKeyCreation --organization=<ORG_ID>
gcloud org-policies set-policy policy.yaml
```
Google documents dry-run organization policies for testing a policy before enforcement (the policy file's
`dryRunSpec`); review the violations before enforcing. Handle exceptions with tag-based conditional rules.

## Verify
- [ ] `gcloud org-policies list --organization=<ORG_ID>` shows the baseline constraints enforced.
- [ ] Attempting the blocked action (for example creating a service account key) fails.

## Checked
2026-11-01. Confirmed on the Organization Policy overview, constraints reference and dry-run (test policies)
pages: rule and tag-conditional behaviour, the six constraint effects above (including not-retroactive for Cloud SQL),
dry-run policies. The three `gcloud` commands pass the CLI reference check. Removed (effect text not read on those
pages): effects for the other constraints, the claim that organizations created after 2024 get defaults, custom
constraints, `in:eu-locations`, Policy Intelligence, IAM Recommender, VPC Service Controls and SCC statements.
Method: documentation only; no commands were run.
