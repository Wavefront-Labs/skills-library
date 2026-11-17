---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.identity-federation
name: identity-federation
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, identity-architecture, identity-federation, sso, saml, oidc, scim, iam-identity-center, entra-id, cloud-identity, workforce-identity-federation, permission-sets]
level: practitioner
status: draft
description: "Federate workforce access to clouds from one IdP: SSO via SAML/OIDC, SCIM provisioning, group-to-role mapping, MFA and session policies, and removing local cloud users."
sources: ["https://docs.aws.amazon.com/singlesignon/latest/userguide/what-is.html", "https://learn.microsoft.com/azure/cloud-adoption-framework/ready/landing-zone/design-area/identity-access", "https://cloud.google.com/iam/docs/workforce-identity-federation"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Workforce identity federation and SSO

## Design
1. **One authoritative IdP** (Entra ID, Okta, Google Workspace, Ping) for all humans.
2. Federate each cloud:
   - AWS: IAM Identity Center with external IdP (SAML 2.0 + SCIM), **permission sets** assigned
     to groups per account. Avoid per-account IAM users.
   - Azure: Entra ID is the native directory; use groups + RBAC at management group/subscription
     scope; B2B for guests.
   - GCP: Cloud Identity / Google Workspace synced from the IdP (Google Cloud Directory Sync or
     SCIM), or **Workforce Identity Federation** to use the external IdP without syncing users.
3. **SCIM provisioning** so leavers lose access automatically.
4. **Groups → roles mapping** as code (Terraform for permission set assignments / role bindings),
   named by job function and environment (`payments-dev-readonly`, `platform-prod-admin`).
5. MFA enforced at the IdP (phishing-resistant for privileged); session length limits shorter for admin roles.
6. Eliminate long-lived local users and access keys for humans; CLI uses SSO (`aws sso login`,
   `az login`, `gcloud auth login`).

## Gotchas
- IdP outage = no cloud access → break-glass accounts outside federation.
- Nested group support varies (SCIM sync of nested groups often unsupported) — flatten.
- Default Identity Center session duration and permission set session duration are separate settings.

## Verify
- [ ] Zero IAM users with console passwords (except break-glass).
- [ ] Disabling a user in the IdP removes cloud access within the SCIM sync interval.
