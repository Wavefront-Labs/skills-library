---
id: computing-software.systems-network-administration.headscale.oidc-filters
name: oidc-filters
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, allowed-domains, allowed-users, allowed-groups, email-verified, oidc-filters]
level: practitioner
status: docs-checked
description: "Limit who can sign in to Headscale via OIDC with allowed_domains, allowed_users and allowed_groups, plus email_verified_required behaviour."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/oidc.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OIDC access filters

```yaml
oidc:
  allowed_domains:
    - example.com
  allowed_users:
    - alice@example.com
    - bob@example.net
  allowed_groups:
    - headscale_users
  scope: ["openid", "profile", "email", "groups"]
```

- Filters are off by default.
- When several are set, a user must pass all of them.
- The groups filter uses the OIDC `groups` claim; the docs' example adds `groups` to `scope`.
- The domain and user filters need a verified email address unless email verification is disabled.

## Email verification

By default the profile uses the email only when the latest login reports `email_verified: true`; an absent, unverified or malformed email clears the stored address. With `email_verified_required: false` the latest login's email is stored without requiring verification (an absent or malformed email still clears it).

## Gotchas

- Microsoft Entra ID: use scope `["openid", "profile", "email"]` and reference groups by group ID (UUID), not name.
- Keycloak: needs a `groups` client scope with a Group Membership mapper (name and claim name `groups`) added to UserInfo, assigned with type `Default`. Group format depends on "Full group path": `/top/group1` enabled, `group1` disabled.
- Kanidm: group names use the full SPN, such as `headscale_users@sso.example.com`.
- These groups only filter sign-in; OIDC groups cannot be used in policy rules.

## Checked

2026-11-04. Confirmed against the Headscale OIDC page (authorize users with filters, email verification control, Keycloak, Kanidm and Microsoft Entra ID notes, limitations).

Method: documentation only; no commands were run.
