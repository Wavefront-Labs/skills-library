---
id: computing-software.cloud-infrastructure-engineering.google-cloud.automatic-user-provisioning-from-entra-id-or-okta
name: automatic-user-provisioning-from-entra-id-or-okta
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-identity, scim-provisioning, automatic-user-provisioning, entra-id, azure-ad, okta, user-lifecycle]
level: practitioner
status: docs-checked
description: "Provision and deprovision Cloud Identity users and groups automatically from Microsoft Entra ID or Okta, including UPN mapping and scoping."
sources: ["https://cloud.google.com/architecture/identity/federating-gcp-with-azure-ad-configuring-provisioning-and-single-sign-on", "https://cloud.google.com/architecture/identity/okta-provisioning-and-single-sign-on", "https://support.google.com/a/answer/7365072"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Automatic user provisioning from Entra ID or Okta

Federation (SAML SSO) handles sign-in; provisioning makes sure the Cloud Identity user and group
objects exist and are suspended when people leave. Without it you get orphaned accounts that keep
IAM grants. Provisioning alone does not let users sign in: configure SSO as well.

## Entra ID
1. In the Admin console create a dedicated provisioning user, e.g. `azuread-provisioning@example.com`.
   Make it a super-admin if Entra must manage all users including admins; a delegated administrator
   (custom admin role) is enough for non-admin users only, and cannot manage other delegated admins
   or super-admins.
2. Entra admin center, Enterprise applications, **Google Cloud/G Suite Connector by Microsoft**
   (a Microsoft product, not supported by Google), Provisioning Mode: Automatic, authorise with that user.
3. Mappings: `primaryEmail`, `name.familyName`, `name.givenName` and `suspended` must be mapped.
   `userPrincipalName` needs a `Replace(...)` expression when the UPN domain differs from the
   Cloud Identity domain.
4. Scope: "Sync only assigned users and groups" when user assignment is configured; assigning a
   group provisions all its members.
5. The connector cannot set email aliases or assign licences (use automatic licensing for OUs).

## Okta
Google Cloud application, Provisioning: enable Create users, Update users and Deactivate users;
use the Push groups tab for the groups you need in Google. The okta-provisioning user must be a super-admin.

## Gotchas
- IAM grants to deleted users become `deleted:user:...` entries; clean them up.
- Test with one user before widening scope.

## Verify
- [ ] A test user appears in Cloud Identity; disabling it in the IdP suspends it.
- [ ] Group membership in `gcloud identity groups memberships list --group-email=<G>` matches the IdP.

## Checked
2026-10-28. Confirmed against the Entra and Okta provisioning pages: provisioning user privileges, connector name and
unsupported-support note, required mappings, UPN Replace expression, scope option, no aliases or licences, Okta
Deactivate users and Push groups. Removed (not in the sources): 40-minute cycle, Provision on demand, nested-group
behaviour, lifecycle table, GCDS and consumer-account claims.
Method: documentation only; no commands were run.
