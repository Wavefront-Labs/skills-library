---
id: computing-software.cloud-infrastructure-engineering.harbor.oidc-authentication
name: oidc-authentication
category: computing-software
field: cloud-infrastructure-engineering
product: harbor
tags: [oidc, sso, group-claim, cli-secret, harbor]
level: practitioner
status: docs-checked
description: "Configure Harbor OIDC login: provider prerequisites, client ID and secret, group claim and admin group, scopes, auto onboarding and the CLI secret."
sources:
  - https://goharbor.io/docs/main/administration/configure-authentication/oidc-auth/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
OIDC works like LDAP in one respect: you can switch from database mode only if no user other than `admin` exists. Self-registration, user creation and deletion and password changes are unavailable.

Provider prerequisites: the endpoint must serve the well-known configuration document; register Harbor as a client with Harbor callback URI as the `redirectURI`; OIDC roles are not mapped to Harbor roles. For groups, create a custom group claim and map it into the ID token.

Under Administration, Configuration, Authentication, set Auth Mode to OIDC and fill in:
- **OIDC Provider Name**, **OIDC Provider Endpoint**, **OIDC Client ID**, **OIDC Client Secret**
- **Group Claim Name** and **OIDC Group Filter** (a regular expression selecting which groups are added; it does not restrict login)
- **OIDC Admin Group**: one group only, must match the group value in the ID token
- **OIDC Scope**: comma-separated; must contain `openid`, usually `profile` and `email`, plus `offline_access` for refresh tokens
- **Verify Certificate**, **Automatic onboarding** (requires **Username Claim**; skips the username prompt on first login), **OIDC Session Logout**, **Primary Auth Mode**

Check that the Redirect URI shown at the bottom matches the provider, then **Test OIDC Server** and **Save**. Login uses the **LOGIN WITH** button; **LOGIN VIA LOCAL DB** is for the local administrator, also reachable at `/account/sign-in`.

Docker and Helm CLIs cannot follow OIDC redirects, so use the CLI secret from User Profile as the password: `docker login -u testuser -p cli_secret harbor.example.com`. One secret per user; a new one invalidates the old. It stays valid after ID token expiry only if the provider issues refresh tokens and refresh succeeds.

## Checked

2026-11-03. Mode-switch rule, provider prerequisites, every field, scopes, login buttons, `/account/sign-in` and CLI secret behaviour were read against the Harbor docs page for OIDC authentication. Removed: "Go" before regular expression (the page says only regular expression).

Method: documentation only; no commands were run.
