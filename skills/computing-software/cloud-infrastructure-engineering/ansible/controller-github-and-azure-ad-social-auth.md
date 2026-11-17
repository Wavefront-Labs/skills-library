---
id: computing-software.cloud-infrastructure-engineering.ansible.controller-github-and-azure-ad-social-auth
name: controller-github-and-azure-ad-social-auth
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, awx, automation-controller, social-auth, azure-ad-auth, github-auth, entra-id, oauth2, organization-map, team-map, platform-gateway]
level: advanced
status: docs-checked
description: "Configure GitHub (org/team) and Azure AD / Entra ID login for AWX and automation controller, with organization and team maps so access follows IdP groups."
sources: ["https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html-single/access_management_and_authentication/", "https://github.com/redhat-cop/infra.aap_configuration"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Controller GitHub and Azure AD social auth

Goal: users log in with their GitHub or Microsoft Entra ID (Azure AD) account, land in the right
organizations and teams automatically, and lose access when removed in the IdP.

## Azure AD / Entra ID
1. Entra admin center → App registrations → New: redirect URI (Web) — use the callback URL shown
   when you create the authenticator in the platform gateway (AAP 2.5).
2. Certificates & secrets → client secret (note expiry; put a renewal reminder in the calendar).
3. Token configuration → add `groups` claim (Security groups) so group membership arrives in the token.
4. In AAP 2.5 create an Azure AD authenticator (Authentication → Authenticators) with the
application's client ID/secret, and add **maps**: organization, team and superuser/auditor maps
whose condition matches the Entra group claim. For group-based team mapping prefer the generic
OIDC or SAML authenticator when you need `groups` claims; check the map semantics below.

## GitHub
- OAuth app (GitHub → Settings → Developer settings → OAuth Apps); register the callback URL the
  authenticator configuration shows.
- In AAP 2.5 create a GitHub authenticator with the OAuth app's client ID/secret and add
  organization/team maps keyed on GitHub org or team membership (the same map semantics as
  Azure AD).

## Map semantics
- `users: true` adds every user who logs in through this backend; a list/regex restricts it.
- `remove_users: true` removes members who no longer match at their next login — without it, access is never revoked by the IdP.
- `admins` grants org admin; keep it to a tiny group.

## As code
`infra.aap_configuration` provides `gateway_authenticators` and `gateway_authenticator_maps` roles
(driving the `ansible.platform` modules) so authenticators and maps live in git, with secrets from vault.

## Gotchas
- Social-auth users are created on first login: you cannot pre-assign them to job templates by name before they log in; assign via teams.
- Username collisions between SSO and local users: external users are created on first login, so
  pre-assign access through teams, not user names.
- Expired client secret = nobody can log in except local admins; keep one break-glass local admin.

## Verify
- [ ] A test user in the mapped group logs in and lands in the expected org/team.
- [ ] Removing the user from the group (with Remove Users enabled on the map) removes the membership at next login.

## Checked

- 2026-10-31: authenticator types (LDAP, SAML, OIDC/Keycloak, GitHub, Azure AD, RADIUS, TACACS+), authenticator creation with maps (organization mapping, team mapping, remove-users behaviour and is_superuser handling) confirmed in AAP 2.5 Access management and authentication. `gateway_authenticators`/`gateway_authenticator_maps` role names confirmed in the redhat-cop infra.aap_configuration roles listing.
- Removed: the legacy `SOCIAL_AUTH_AZUREAD_OAUTH2_*`/`SOCIAL_AUTH_GITHUB_ORG_*` settings blocks, the old `/sso/complete/...` callback paths and the `SOCIAL_AUTH_USER_FIELDS`/`ansible.platform.authenticator` module names (legacy or unverifiable; replaced with the documented 2.5 authenticator/mapper model and confirmed role names).
Method: documentation only; no commands were run.
