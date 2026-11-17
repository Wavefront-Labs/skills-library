---
id: computing-software.cloud-infrastructure-engineering.google-cloud.projects-iam-and-service-accounts
name: projects-iam-and-service-accounts
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, resource-hierarchy, organization, folders, projects, iam, predefined-roles, custom-roles, iam-conditions, service-accounts, service-account-keys, impersonation, workload-identity-federation, gke-workload-identity, org-policy, deny-policies, gcloud, policy-analyzer, iam-recommender, principal-access-boundary, vpc-service-controls]
level: practitioner
status: docs-checked
description: "Structure GCP org, folders and projects; bind predefined IAM roles to groups; run workloads as keyless service accounts via impersonation and workload identity federation."
sources: ["https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy", "https://cloud.google.com/iam/docs/workload-identity-federation", "https://cloud.google.com/iam/docs/deny-overview", "https://cloud.google.com/resource-manager/docs/organization-policy/restricting-service-accounts", "https://cloud.google.com/resource-manager/docs/organization-policy/org-policy-constraints"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Google Cloud projects, IAM and service accounts — keyless, group-based, inherited

**Goal:** a folder/project layout where IAM and org policies are set once and inherited,
humans get access through groups, and no workload ever needs a downloaded JSON key.

## 1. Lay out the hierarchy
Organization › folders (up to 10 levels; keep 2-3) › projects › resources.
IAM allow policies are **additive down the tree**: a grant on a folder applies to everything below it.
Restrict with deny policies or org policies instead.
- Typical: `fldr-common` (networking host projects, logging, security),
  `fldr-prod`, `fldr-nonprod`, `fldr-sandbox`, each holding one project per workload per env.
- Project is the unit of API enablement and the base level where resources live. Project IDs are globally unique and permanent
  after creation.

## 2. Bind roles to groups
- Avoid basic roles (`roles/owner`, `roles/editor`, `roles/viewer`) — Editor covers
  write on a large number of services. Use predefined roles (`roles/run.developer`,
  `roles/storage.objectViewer`); custom roles only when no predefined fits (and you
  then own their maintenance as permissions change).
- Bind to Google groups: `gcloud projects add-iam-policy-binding <PROJECT_ID> --member=group:app1-devs@example.com --role=roles/run.developer`.
- **IAM Conditions** for time-bound or resource-scoped grants, e.g.
  `--condition='expression=request.time < timestamp("2026-11-01T00:00:00Z"),title=temp'`
  or `resource.name.startsWith("projects/_/buckets/app1-")`.
- **Deny policies** (IAM v2) override allows: e.g. deny `iam.serviceAccountKeys.create`
  for everyone except a break-glass group. Not all permissions are deniable — check the list.
- Prefer `add-iam-policy-binding` / `remove-iam-policy-binding` over replacing a whole policy.

## 3. Service accounts without keys
- One SA per workload, named for its job (`sa-app1-api@<PROJECT_ID>.iam.gserviceaccount.com`).
  Never use the Compute Engine default SA (historically had Editor); the org policy
  `iam.automaticIamGrantsForDefaultServiceAccounts` stops that grant.
- Humans and tools **impersonate**: grant `roles/iam.serviceAccountTokenCreator` on the
  SA to a group, then use `--impersonate-service-account=<SA_EMAIL>` on gcloud commands.
- `roles/iam.serviceAccountUser` (actAs) on an SA lets someone deploy resources that run
  as it.
- **Workload Identity Federation** for GitHub/GitLab/AWS/Azure/OIDC: create a pool and
  provider with an `--attribute-condition` like `assertion.repository_owner=='example-org'`,
  then grant `roles/iam.workloadIdentityUser` to
  `principalSet://iam.googleapis.com/projects/<PROJECT_NUMBER>/locations/global/workloadIdentityPools/<POOL>/attribute.repository/example-org/app`.
  Direct resource access by federated principals (no SA) is also supported for many services.

## 4. Org policies as guardrails
Set at org/folder: `iam.disableServiceAccountKeyCreation`,
`iam.allowedPolicyMemberDomains` (domain-restricted sharing; accepts an organisation principal set or a Workspace customer ID),
`compute.vmExternalIpAccess`, `gcp.resourceLocations`, `storage.uniformBucketLevelAccess`,
`sql.restrictPublicIp`. Some constraints are enforced by default on newer organisations (for example
`iam.automaticIamGrantsForDefaultServiceAccounts` for organisations created on or after 2024-05-03); check which apply to yours.
Dry-run mode (`dryRunSpec`) exists for trialling a policy before enforcing it.

## Gotchas
- Google's best practices say to use attribute conditions when federating with GitHub or other multi-tenant providers; without one, any
  tenant of that issuer can present tokens to the provider.
- Access changes are eventually consistent (see the deny-overview page on access change propagation).
- Granting on a folder is invisible from `projects get-iam-policy`; use
  Policy Analyzer (`gcloud asset analyze-iam-policy`) to see effective access.
- Org policy changes are not retroactive: existing keys or public IPs remain until removed.

## Verify
- [ ] No basic roles bound at org or folder level; project basic roles only in sandboxes.
- [ ] `iam.disableServiceAccountKeyCreation` enforced; `gcloud iam service-accounts keys list --managed-by=user` empty across projects.
- [ ] CI authenticates via WIF with a restrictive attribute condition.
- [ ] All human bindings target groups; Policy Analyzer shows no unexpected individual users.
- [ ] IAM Recommender findings reviewed and over-grants removed.

Related: computing-software.cloud-infrastructure-engineering.cloud-architecture.multi-account-landing-zone

## Checked

- Date: 2026-10-27
- Confirmed against the resource hierarchy page (organisation required for folders), the folders guide (10 levels), the deny-overview page (deny checked before allow, eventual consistency), the constraints list (`iam.disableServiceAccountKeyCreation`, `iam.allowedPolicyMemberDomains`, `compute.vmExternalIpAccess`, `gcp.resourceLocations`, `storage.uniformBucketLevelAccess`, `sql.restrictPublicIp`), the Restricting service accounts page (`iam.automaticIamGrantsForDefaultServiceAccounts` enforced for organisations created on or after 2024-05-03), the domain-restriction page (customer ID or organisation principal set), the best-practices-for-WIF page and the IAM roles reference (`roles/iam.serviceAccountTokenCreator`, `roles/iam.workloadIdentityUser`).
- Removed: Shared VPC subnet advice, basic-role condition claim, whole-policy `set-iam-policy` etag detail, `gcloud config set auth/impersonate_service_account` and Terraform impersonation lines, GKE workload identity bullet, "Google now requires a condition" claim, SA recreation note and the propagation timings. Sources replaced with real URLs.

Method: documentation only; no commands were run.
