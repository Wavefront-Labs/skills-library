---
id: computing-software.systems-network-administration.headscale.oidc-identity-caveats
name: oidc-identity-caveats
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, provider-identifier, usernames, switching-providers, claims, oidc-identity]
level: advanced
status: docs-checked
description: "OIDC identity pitfalls in Headscale: supported claims, username rules, mutable emails, provider identifiers in policy, and switching providers."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/oidc.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OIDC identity caveats

## Claims used

- `email`: synced only when verified (unless `email_verified_required: false`).
- `name`: display name. `preferred_username`: username. `picture`: profile picture URL.
- `iss` and `sub`: together form the provider identifier.
- `groups`: only for the allowed-groups filter.

## Username rules

At least two characters, start with a letter, contain only letters, digits, hyphens, dots, underscores and at most one `@`. In policy, `ssmith` is written `ssmith@`.

## Risk: mutable identifiers

Many identity providers let users update their own profile, so username or email may change; a policy might stop working or a user might gain access by hijacking an existing username or email. Use provider identifiers in policies when your provider lets users change their own usernames, e.g. via a group alias (append `@` if the identifier does not already contain one):

```json
{ "groups": { "group:alice": ["https://sso.example.com/oauth2/openid/59ac9125-c31b-46c5-814e-06242908cf57@"] } }
```

The provider identifier is currently only available from the API (the `/api/v1/user` endpoint, field `providerId`), the database, or directly from your identity provider.

## Switching providers

Headscale stores each user's provider identifier but supports one provider at a time. After switching, update the `provider_identifier` column of the `users` table by hand. It is built from `iss` and `sub`, for example `https://id.example.com/12340987`.

Expire a node immediately and force re-authentication with `headscale node expire -i <NODE_ID>` (from the node expiration section of the page).

## Checked

2026-11-04. Confirmed against the Headscale OIDC page (claims table, limitations username pattern, policy user references, provider identifier, switching providers). The `iss`/`sub` composition and the example identifier come from the page.

Method: documentation only; no commands were run.
