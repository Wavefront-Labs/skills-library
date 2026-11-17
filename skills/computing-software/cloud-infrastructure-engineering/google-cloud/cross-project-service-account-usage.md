---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cross-project-service-account-usage
name: cross-project-service-account-usage
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, service-accounts, cross-project-service-accounts, service-account-user-role, disablecrossprojectserviceaccountusage, actas, central-sa-project, sa-lien, iam-serviceaccountuser, resource-in-other-project, shared-service-accounts]
level: advanced
status: docs-checked
description: "Attach a service account from one project to resources in another: actAs, the disableCrossProjectServiceAccountUsage constraint, the automatic lien, and service agent grants."
sources: ["https://docs.cloud.google.com/iam/docs/attach-service-accounts", "https://docs.cloud.google.com/resource-manager/docs/organization-policy/restricting-service-accounts"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cross-project service account usage

**Goal:** when a workload in project B must run as a service account owned by project A, do it
deliberately with the right constraint and grants, and know why one service account per workload
in its own project is usually simpler.

## 1. Scope
Granting a service account from A a role on a resource in B is ordinary IAM. This skill is about
**attaching** A's service account to a resource in project B.

## 2. Steps (from the "Attach service accounts to resources" page)
1. The person creating the resource needs `roles/iam.serviceAccountUser` (permission `iam.serviceAccounts.actAs`) on the service account.
2. In the project that **owns the service account** (A), make sure the boolean constraint `iam.disableCrossProjectServiceAccountUsage` is not enforced. It controls whether a service account can be attached to a resource in another project, is enforced by default (on by default for organizations created on or after May 3, 2024, per the constraint page) and can only be configured at the project level, not folder or organization. Tags cannot be used to enforce it conditionally.
3. Find the service agent email of the service that owns the resource type in B (different services use different agents). Some services (Dataflow, Google Kubernetes Engine and similar) also depend on Compute Engine, so you need both agents.
4. Grant each service agent `roles/iam.serviceAccountTokenCreator` on the service account:
```bash
gcloud iam service-accounts add-iam-policy-binding <SA_NAME>@<PROJECT_ID>.iam.gserviceaccount.com \
  --member=serviceAccount:<SERVICE_AGENT_EMAIL> --role=roles/iam.serviceAccountTokenCreator
```
Then create the resource in B and attach the service account as usual.

## 3. The automatic lien
When the constraint is not enforced, IAM adds a project lien (origin
`iam.googleapis.com/cross-project-service-accounts`) that prevents deleting the project. Google
strongly discourages removing it. Enforcing `iam.restrictCrossProjectServiceAccountLienRemoval`
means only principals with `resourcemanager.projects.updateLiens` at the organization level can
remove the lien (by default anyone with it on the project can).

## 4. When to use it
Reasonable for a central project that owns pipeline or deployer service accounts. For ordinary
application runtimes keep the service account in the workload's project: otherwise A's IAM admins
control identities used in B, and deleting or moving A is entangled with B.

## Gotchas
- Relaxing the constraint on the resource's project (B) does nothing; it applies to the project containing the service account.
- The service agent grant is easy to forget: the user's `actAs` check passes but the deployment fails.

## Verify
- [ ] The constraint is unenforced only on the identity project.
- [ ] A test deploy in B with the A-owned service account succeeds.
- [ ] Deleting project A is blocked by the lien.

## Checked
2026-10-31. Confirmed against "Attach service accounts to resources" (serviceAccountUser/actAs, project-level constraint enforced by default, service agents and Token Creator grant, lien origin) and the restricting-service-accounts page (May 3, 2024 default, lien removal constraint, tags not usable). Removed: the org-policy YAML recipe, specific service agent addresses, the Cloud Run serviceAccountUser grant to agents (the docs say Token Creator), audit queries, the Workload Identity and org-move gotchas and the FAILED_PRECONDITION error text (not confirmed in fetched pages).
Method: documentation only; no commands were run.
