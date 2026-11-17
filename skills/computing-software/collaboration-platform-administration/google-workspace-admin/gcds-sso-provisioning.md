---
id: computing-software.collaboration-platform-administration.google-workspace-admin.gcds-sso-provisioning
name: gcds-sso-provisioning
category: computing-software
field: collaboration-platform-administration
product: google-workspace-admin
tags: [gcds-sso-provisioning]
level: advanced
status: draft
description: Sync from LDAP/AD and set up SAML SSO with auto-provisioning.
sources: ['https://support.google.com/a/', 'https://cloud.google.com/learn/certification/google-workspace-administrator']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Directory sync (GCDS) and SSO
**Goal:** Sync from LDAP/AD and set up SAML SSO with auto-provisioning.

- Google Cloud Directory Sync (GCDS) syncs users, groups and OUs one-way from LDAP/AD; run a simulation first.
- SAML SSO: Security > Authentication > SSO with third-party IdP; set sign-in page URL, verification certificate.
- Use Entra ID or Okta app galleries for Google Workspace automated provisioning where possible (reference IAM products).
- Keep a non-SSO super admin for recovery.

## Gotchas
- Always run the GCDS simulation to avoid mass suspensions or deletions.
- SSO with 2SV: decide whether Google 2SV applies after SSO.

## Self-check
A test user signs in via the IdP; GCDS simulation shows only expected changes.
