---
id: computing-software.systems-network-administration.immich.oauth-settings-and-claims
name: oauth-settings-and-claims
category: computing-software
field: systems-network-administration
product: immich
tags: [issuer-url, storage-quota-claim, auto-register, role-claim, storage-label]
level: practitioner
status: docs-checked
description: "Immich OAuth settings and defaults: scope, signing algorithms, role, storage label and quota claims, auto register, and how claims sync on login."
sources:
  - https://docs.immich.app/administration/oauth
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: configure Administration, Settings, OAuth correctly once the identity provider client exists.

Required: `issuer_url`, `client_id`, `client_secret`. Defaults for the rest:

- `scope`: `openid email profile` (space delimited).
- `id_token_signed_response_alg`: `RS256`.
- `userinfo_signed_response_alg`: `none`.
- `prompt`: empty (examples: `select_account`, `login`, `consent`).
- `end_session_endpoint`: empty.
- Request timeout: 30,000 ms.
- Storage Label Claim: `preferred_username`.
- Role Claim: `immich_role` (must return `user` or `admin`).
- Storage Quota Claim: `immich_quota`.
- Default Storage Quota (GiB): `0`; empty means unlimited.
- Button Text: "Login with OAuth".
- Auto Register: `true`, which creates the user at first sign-in.
- Auto Launch: `false`.

Quota claim values are GiB: `-1` for unlimited, `0` blocks uploads, a positive number sets a fixed quota.

Claims apply when a user is first registered. On later logins, claims present in the profile are synchronised to the Immich user; absent claims leave values unchanged. The storage label is the exception: with the default `preferred_username` claim it is only set at registration. To keep it synced from the provider, configure a different Storage Label Claim.

Authelia needs a custom claim and scope defined for `immich_quota`, then `Scope` set to `openid email profile immich_scope` and `Token Endpoint Auth Method` `client_secret_post`.

Do not set Auto Launch until sign-in works; you can bypass it later by using the browser back button on the login page.

## Checked

2026-11-03. Confirmed against the Immich docs (https://docs.immich.app/) by reading: administration/oauth (Enable OAuth settings table, Claim Options, Authelia Example).
Removed or reworded: nothing needed removal.
Method: documentation only; no commands were run.
