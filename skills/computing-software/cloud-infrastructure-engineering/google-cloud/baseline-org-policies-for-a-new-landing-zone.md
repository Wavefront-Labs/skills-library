---
id: computing-software.cloud-infrastructure-engineering.google-cloud.baseline-org-policies-for-a-new-landing-zone
name: baseline-org-policies-for-a-new-landing-zone
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, landing-zone, baseline-org-policies, secure-by-default-org-policies, org-policy, security-baseline]
level: practitioner
status: docs-checked
description: "Apply a baseline set of organization policy constraints to a new Google Cloud landing zone, with dry-run rollout, tag-based exceptions and secure-by-default policies."
sources: ["https://cloud.google.com/resource-manager/docs/secure-by-default-organizations", "https://cloud.google.com/resource-manager/docs/organization-policy/org-policy-constraints"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Baseline org policies for a new landing zone

Organizations created on or after May 3, 2024 get the Google Cloud security baseline constraints enforced (SA key creation and upload disabled, no Editor on default SAs, `iam.allowedPolicyMemberDomains`, `essentialcontacts.managed.allowedContactDomains`, protocol-forwarding restriction, `storage.uniformBucketLevelAccess`); some organizations created February to April 2024 have them too. Older orgs need the baseline applied explicitly; check what applies with *Viewing organization policies*. The baseline lists the managed form `iam.managed.disableServiceAccountKeyCreation` for key creation. Set at the org root; grant exceptions on folders/projects via tags.

## Baseline (enforce)
| Constraint | Why |
|---|---|
| `iam.disableServiceAccountKeyCreation` / `iam.disableServiceAccountKeyUpload` | keyless by default |
| `iam.automaticIamGrantsForDefaultServiceAccounts` | no Editor on default SAs |
| `iam.allowedPolicyMemberDomains` (customer IDs) | no external principals |
| `storage.uniformBucketLevelAccess`, `storage.publicAccessPrevention` | no ACLs/public buckets |
| `compute.vmExternalIpAccess` (deny all) | no public VMs |
| `compute.requireOsLogin`, `compute.disableSerialPortAccess` | central SSH control |
| `compute.skipDefaultNetworkCreation` | no default VPC with open rules |
| `compute.restrictXpnProjectLienRemoval` | protect Shared VPC hosts |
| `sql.restrictPublicIp`, `sql.restrictAuthorizedNetworks` | private databases |
| `gcp.resourceLocations` | data residency |
| `essentialcontacts.allowedContactDomains` | contacts in your domain |
| `compute.requireShieldedVm` | integrity |
| `iam.serviceAccountKeyExposureResponse` = DISABLE_KEY | auto-disable leaked keys |

## Rollout
1. Write all as code (policy YAML under version control, applied with `gcloud org-policies set-policy` or your IaC tool).
2. Where the constraint supports it, apply as `dryRunSpec` first and review the audit-logged violations (see Test organization policies for which constraints support dry run). Test the rest on a sandbox folder.
3. Promote to `spec`. Create exception tags (a tag key and value you define, matched with `resource.matchTag`) and conditional
   rules rather than per-project overrides.
4. Document each exception with owner and expiry.

## Gotchas
- `skipDefaultNetworkCreation` applies when a project is created, so set it before creating projects.
- `allowedPolicyMemberDomains` limits sharing to your organization or customer IDs; plan exceptions (see the domain-restricted sharing skill).
- Service-specific constraints (for example Cloud Run `run.allowedIngress`): add per platform later.

## Verify
- [ ] `gcloud org-policies list --organization=<ORG_ID>` shows every baseline constraint.
- [ ] A test project cannot create a public IP VM or SA key.

## Checked
2026-10-31. Confirmed against "Manage baseline constraints" (secure-by-default organizations) and the organization policy constraints reference: the May 3, 2024 and February-April 2024 dates, the seven automatically enforced constraints including the managed key-creation form, and the constraint names in the baseline table (all found in the reference), and `skipDefaultNetworkCreation` behaviour. `gcloud org-policies list` checked against the gcloud reference. Removed: Terraform/Fabric FAST resource names, the placeholder tag name, the detailed dry-run support list, and the existing-default-network and `allUsers` remarks (not stated on the pages read).
Method: documentation only; no commands were run.
