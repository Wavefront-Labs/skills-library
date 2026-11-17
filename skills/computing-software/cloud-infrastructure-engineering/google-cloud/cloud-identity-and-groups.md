---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cloud-identity-and-groups
name: cloud-identity-and-groups
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-identity, google-groups, groups, super-admin, workforce-identity-federation, identity-federation, google-cloud-directory-sync, gcds, saml-sso, 2sv, two-step-verification, security-keys, domain-verification, organization-creation, group-based-iam, workspace-identity]
level: practitioner
status: draft
description: "Stand up identity for a GCP organization: verify the domain, create Cloud Identity, protect super admins with hardware keys, sync or federate users, and grant all IAM through groups."
sources: ["https://cloud.google.com/identity/docs/set-up-cloud-identity-admin", "https://cloud.google.com/architecture/identity/best-practices-for-planning", "https://cloud.google.com/architecture/identity/federating-gcp-with-active-directory-introduction", "https://cloud.google.com/iam/docs/workforce-identity-federation", "https://cloud.google.com/resource-manager/docs/super-admin-best-practices"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cloud Identity and groups

**Goal:** a Google Cloud organization whose users come from your identity provider, whose
super admins are few and hardware-key protected, and whose IAM bindings reference groups only.

## 1. Create the organization
- A GCP organization resource is created automatically the first time a **Cloud Identity**
  or Google Workspace account with a verified domain creates a project. Verify the domain
  (TXT record) in the Admin console first; `example.com` plus secondary domains all map to the
  same organization.
- Cloud Identity Free is enough for the infrastructure org; Premium adds device management
  and more audit.
- Check: `gcloud organizations list` shows the org ID; `gcloud resource-manager folders list --organization=<ORG_ID>`.

## 2. Super-admin hygiene (the step people skip)
- Super admin (Workspace/Cloud Identity) is *not* the same as `roles/resourcemanager.organizationAdmin`,
  but it can recover it, so treat it as root.
- Keep 2-3 dedicated super-admin accounts (`gcp-superadmin-1@`), not daily-use mailboxes,
  with **security keys** enforced (Admin console → Security → 2-Step Verification → *Only security key*).
- Separate the super-admin group from the Org Admin IAM group; log in to super admin only for break-glass.
- Enrol the break-glass accounts in a separate OU with its own 2SV policy; store recovery codes offline.

## 3. Bring users in
Pick one:
| Method | When | Notes |
|---|---|---|
| **Google Cloud Directory Sync (GCDS)** + SAML SSO | on-prem AD/LDAP is source of truth | GCDS provisions users/groups into Cloud Identity; IdP (ADFS/Okta/Entra) handles login via SAML. Users exist as Google identities. |
| **Entra ID / Okta provisioning (SCIM)** | cloud IdP | Same result as GCDS with less to run. |
| **Workforce Identity Federation** | you do not want Google identities at all | Users federate at login with no Cloud Identity user object; some products (e.g. a few consoles, BigQuery sharing cases) still have gaps — check the supported-products list before committing. |

Always keep **at least one non-federated admin** account so an IdP outage cannot lock the org.

## 4. Groups-only IAM
- Create groups in Cloud Identity (or sync them) named for the role they confer:
  `gcp-org-admins@`, `gcp-billing-admins@`, `gcp-network-admins@`, `gcp-<team>-developers@`.
- Grant IAM to `group:gcp-network-admins@example.com`, never to `user:`. Enforce with an
  org policy `iam.allowedPolicyMemberDomains` (restrict members to your customer ID) and a
  custom constraint denying `user:` bindings.
- Google Groups security settings: *who can join* = only invited; *who can post* = managers;
  disable external members for IAM-bearing groups. `gcloud identity groups memberships add --group-email=... --member-email=...`.
- Nested groups work for IAM but Policy Analyzer makes them harder to reason about; keep nesting to one level.

## Gotchas
- A user who made a project with a personal gmail before the org existed owns a "No organization"
  project; migrate it with `gcloud projects move --organization=<ORG_ID>` (requires the user as owner and
  `resourcemanager.projects.move` on the org).
- Deleting a user in the IdP and re-creating them yields a *new* Google identity: old IAM bindings
  show as `deleted:user:...?uid=` and must be re-granted. Suspend instead of delete when possible.
- `iam.allowedPolicyMemberDomains` also blocks `allUsers` on public buckets and Cloud Run; add exceptions
  per project via tags, not by lifting the org policy.

## Verify
- [ ] Admin console shows ≥2 super admins, all with security-key-only 2SV, none used for daily work.
- [ ] `gcloud organizations get-iam-policy <ORG_ID>` has no `user:` members.
- [ ] A new IdP user appears in Cloud Identity within the sync interval and can log in via SSO.
- [ ] Break-glass account login works with the IdP disabled (test in a maintenance window).
